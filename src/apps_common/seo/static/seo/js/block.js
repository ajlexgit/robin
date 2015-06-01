(function($) {

    $(document).ready(function() {
        $('.seo-text').on('click', '.short-text', function() {
            var $self = $(this);
            var $hidden = $self.closest('.seo-text').find('.hidden-text');
            if (!$hidden.length) {
                return;
            }

            var startHeight = $self.outerHeight();
            var endHeight = $hidden.outerHeight();
            $self.addClass('hidden-text').height('');
            $hidden.removeClass('hidden-text').height(startHeight).stop().animate({
                height: endHeight
            }, {
                duration: 800,
                complete: function () {
                    $hidden.height('');
                }
            });
        }).on('click', '.full-text', function () {
            var $self = $(this);
            var $hidden = $self.closest('.seo-text').find('.hidden-text');
            if (!$hidden.length) {
                return;
            }

            var startHeight = $self.outerHeight();
            var endHeight = $hidden.outerHeight();

            $self.height(startHeight).stop().animate({
                height: endHeight
            }, {
                duration: 800,
                complete: function () {
                    $hidden.removeClass('hidden-text');
                    $self.addClass('hidden-text').height('');
                }
            });
        });
    });

})(jQuery);