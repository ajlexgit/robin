(function($) {

    /*
        Требует:
            jquery.fitvids.js

        Для автоматического ресайза Instagram нужно подключить скрипт:
            <script async="" defer="" src="//platform.instagram.com/en_US/embeds.js"></script>
    */

    $(document).ready(function() {
        // Видео на всю ширину с сохранение пропорций
        $('.page-video').fitVids();
    });

})(jQuery);