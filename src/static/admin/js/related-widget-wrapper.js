(function($){
    /*
        Пофиксенная версия встроенного JS,
        позволяющая обрабатывать не только select-тэги.
     */

    function updateLinks() {
        var $this = $(this);
        var siblings = $this.nextAll('.change-related, .delete-related');
        if (!siblings.length) return;
        var value = $this.val();
        if (value) {
            siblings.each(function(){
                var elm = $(this);
                elm.attr('href', elm.attr('data-href-template').replace('__fk__', value));
            });
        } else siblings.removeAttr('href');
    }

    $.attachRelatedWidgetSupport = function(selector) {
        var $doc = $(document);
        $doc.on('change', '.related-widget-wrapper ' + selector, updateLinks);
        $doc.find('.related-widget-wrapper ' + selector).each(updateLinks);
    };

    $(document).ready(function() {
        $.attachRelatedWidgetSupport('select');
        $(document).on('click', '.related-widget-wrapper-link', function() {
            if (this.href) {
                showRelatedObjectPopup(this);
            }
            return false;
        });
    });

})(jQuery);
