(function($) {

    /*
        Требует:
            jquery.fitvids.js

        Для резиновости iframe интаграма нужно подключить скрипт:
            <script src="//platform.instagram.com/en_US/embeds.js"></script>
    */

    $(document).ready(function() {
        // Видео на всю ширину с сохранение пропорций
        $('.page-video').fitVids();
    });

})(jQuery);