(function($) {

    $(document).ready(function() {
        $('#seo-text .text').readmore({
            collapsedHeight: 85,
            heightMargin: 17,
            moreLink: '<a class="readmore" href="#">Read more</a>',
            lessLink: '<a class="readmore" href="#">Close</a>'
        });
    });

})(jQuery);