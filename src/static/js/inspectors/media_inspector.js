(function($) {

    /*
        Инспектор, отслеживающий событие, когда ширина окна превысила
        некоторый лимит, либо опустилась ниже него.

        Не следует создавать экземпляры класса MediaInspector.
        Следует пользоваться уже созданным экземпляром $.mediaInspector.

        Требует:
            jquery.utils.js, inspector.js
     */

    var MediaInspector = Class(Inspector, function(cls, superclass) {
        cls.init = function() {
            this._list = [];
            this.STATE_DATA_KEY = 'mediainspector_state';
            this.OPTS_DATA_KEY = 'mediainspector_opts';
        };

        cls.prototype.getDefaultOpts = function() {
            return $.extend(superclass.prototype.getDefaultOpts(), {
                point: 0
            })
        };


        cls.prototype._check = function($element, opts) {
            return window.innerWidth >= opts.point;
        };
    });


    // Единственный экземпляр инспектора
    $.mediaInspector = MediaInspector.create();

    $(window).on('resize.media_inspector', $.rared(function() {
        $.mediaInspector.checkAll();
    }, 100));

})(jQuery);