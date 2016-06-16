import argparse
from queue import Queue
from threading import Lock
from requests import Session
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, SplitResult
from concurrent.futures import ThreadPoolExecutor, wait


class LinkChecker:
    timeout = (5, 10)

    def __init__(self, url, proxy=None, verbosity=0):
        self._start_url = self.url_split(url)
        if not self._start_url.netloc:
            raise ValueError('Invalid URL')

        self.client = Session()
        self.client.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
        })

        if proxy:
            self.client.proxies = {
                'http': proxy,
                'https': proxy,
            }

        self._verbosity = verbosity
        self._pages = Queue()
        self._files = Queue()
        self._checked = set()
        self._checked_lock = Lock()

    def output(self, msg, verbosity=0):
        if verbosity <= self._verbosity:
            print(msg)

    def url_split(self, url, source_page=None):
        url = url.strip()
        if not url:
            raise ValueError('empty url')

        value = urlsplit(url, scheme='http')

        # Обработка относительных адресов
        path = value.path
        if not value.netloc:
            if not path.startswith('/'):
                path += (source_page and source_page.path) or '/'
        else:
            if not path:
                path = '/'

        return value._replace(path=path)

    def url_join(self, value, source_page=None):
        scheme = value.scheme or (source_page and source_page.scheme) or self._start_url.scheme
        netloc = value.netloc or (source_page and source_page.netloc) or self._start_url.netloc
        return SplitResult(
            scheme=scheme,
            netloc=netloc,
            path=value.path,
            query=value.query,
            fragment='',
        ).geturl()


    def queue_file(self, url, source_page=None):
        """ Помещаем путь к файлу в очередь """
        if not url:
            return

        splitted = self.url_split(url, source_page=source_page)

        url = self.url_join(splitted, source_page=source_page)
        with self._checked_lock:
            if url in self._checked:
                return
            else:
                self._checked.add(url)
                self.output(
                    "  Added file '%s'" % url,
                    verbosity=2
                )

        self._files.put((splitted, source_page))

    def queue_page(self, url, source_page=None):
        """ Помещаем путь к странице в очередь """
        if not url:
            return

        # Отсеиваем "mailto" и "tel"
        if url.startswith('mailto:') or url.startswith('tel:'):
            return

        splitted = self.url_split(url, source_page=source_page)

        # Отсеиваем не-HTTP схемы
        if splitted.scheme and splitted.scheme not in ('http', 'https'):
            return

        # Отсеиваем внешние страницы
        if splitted.netloc and splitted.netloc != self._start_url.netloc:
            return

        url = self.url_join(splitted, source_page=source_page)
        with self._checked_lock:
            if url in self._checked:
                return
            else:
                self._checked.add(url)
                self.output(
                    "  Added page '%s'" % url,
                    verbosity=2
                )

        self._pages.put((splitted, source_page))

    def check_file(self, splitted, source_page):
        """ Проверка существования файла """
        url = self.url_join(splitted)

        try:
            response = self.client.head(url, timeout=self.timeout)
        except Exception as e:
            self.output("ERROR on '%s': %s" % (url, e))
            return

        if not response.ok:
            source_url = self.url_join(source_page)
            self.output(
                "%s %s '%s' on '%s'" % (response.status_code, response.reason, url, source_url)
            )

    def parse_page(self, splitted, source_page):
        """ Проверка и парсинг страницы """
        # log
        if splitted.query:
            self.output(
                "Scan '%s?%s'" % (splitted.path, splitted.query),
                verbosity=1,
            )
        else:
            self.output(
                "Scan '%s'" % splitted.path,
                verbosity=1,
            )

        url = self.url_join(splitted)
        try:
            response = self.client.get(url, timeout=self.timeout)
        except Exception as e:
            self.output("ERROR on '%s': %s" % (url, e))
            return

        # Проверяем, что не было редиректа на внешний сайт
        final_url = self.url_split(response.url)
        if final_url.netloc != self._start_url.netloc:
            # TODO
            print('Redirected on %s' % url)
            return

        if response.ok:
            soup = BeautifulSoup(response.text, 'html5lib')
            try:
                self._parse_page_img(soup, source_page=splitted)
                self._parse_page_script(soup, source_page=splitted)
                self._parse_page_link(soup, source_page=splitted)
                self._parse_page_a(soup, source_page=splitted)
                self._parse_page_video(soup, source_page=splitted)
                self._parse_page_picture(soup, source_page=splitted)
            except Exception as e:
                self.output("ERROR on '%s': %s" % (url, e))
        else:
            source_url = self.url_join(source_page) if source_page else '-//-'
            self.output(
                "%s %s '%s' on '%s'" % (response.status_code, response.reason, url, source_url)
            )

    def _parse_page_img(self, soup, source_page):
        """ Тэги <img> """
        for img in soup.findAll('img'):
            src = img.get('src', '')
            self.queue_file(src, source_page=source_page)

            # srcset
            srcsets = img.get('srcset') or ''
            srcsets = map(str.strip, srcsets.split(','))
            srcsets = filter(bool, srcsets)
            for srcset in srcsets:
                url, *other = srcset.split()
                self.queue_file(url, source_page=source_page)

    def _parse_page_video(self, soup, source_page):
        """ Тэги <video> """
        for video in soup.findAll('video'):
            src = video.get('src', '')
            self.queue_file(src, source_page=source_page)

            # sources
            for source in video.findAll('source'):
                src = source.get('src', '')
                self.queue_file(src, source_page=source_page)

    def _parse_page_picture(self, soup, source_page):
        """ Тэги <picture> """
        for picture in soup.findAll('picture'):
            src = picture.get('src', '')
            self.queue_file(src, source_page=source_page)

            # sources
            for source in picture.findAll('source'):
                src = source.get('src', '')
                self.queue_file(src, source_page=source_page)

    def _parse_page_script(self, soup, source_page):
        """ Тэги <script> """
        for script in soup.findAll('script'):
            src = script.get('src', '')
            self.queue_file(src, source_page=source_page)

    def _parse_page_link(self, soup, source_page):
        """ Тэги <link> """
        for link in soup.findAll('link'):
            href = link.get('href', '')
            if link.get('itemprop'):
                self.queue_page(href, source_page=source_page)
            else:
                self.queue_file(href, source_page=source_page)

    def _parse_page_a(self, soup, source_page):
        """ Тэги <a> """
        for a in soup.findAll('a'):
            href = a.get('href', '')
            self.queue_page(href, source_page=source_page)

    def run(self, threads=10):
        self.queue_page(self.url_join(self._start_url))
        with ThreadPoolExecutor(max_workers=threads)as e:
            def task_queue():
                result = []
                while not self._files.empty():
                    file_task = self._files.get()
                    future = e.submit(self.check_file, *file_task)
                    result.append(future)

                while not self._pages.empty():
                    page_task = self._pages.get()
                    future = e.submit(self.parse_page, *page_task)
                    result.append(future)

                return result

            while True:
                futures = task_queue()
                wait(futures)
                if not futures:
                    break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url',
        action='store',
        type=str,
        help='Initial URL',
    )
    parser.add_argument('-t', '--threads',
        action='store',
        type=int,
        default=20,
        dest='threads',
        metavar='COUNT',
        help='Thread count',
    )
    parser.add_argument('-p', '--proxy',
        action='store',
        type=str,
        dest='proxy',
        metavar='HOST:PORT',
        help='Proxy server',
    )
    parser.add_argument('-v', '--verbosity',
        action='store',
        type=int,
        choices=[0, 1, 2],
        dest='verbosity',
        metavar='LEVEL',
        help='Verbosity',
    )

    args = parser.parse_args()
    checker = LinkChecker(args.url, proxy=args.proxy, verbosity=args.verbosity)
    checker.run(threads=args.threads)

