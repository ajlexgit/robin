(function($) {

    $(document).ready(function() {
        $('#posts').fakeLink({
            itemSelector: '.post',
            linkSelector: '.title a'
        });
    });

})(jQuery);