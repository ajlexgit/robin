(function($) {

    /*
        Возвращает размеры canvas с учетом ограничений браузера.
        Параметры:
            img_width, img_height - исходные размеры картинки
            max_width, max_height - целевые ограничения
    */
    window.canvasSize = function(img_width, img_height, max_width, max_height) {
        var ratio = img_width / img_height;
        var width, height;

        // Размеры с учетом max_width/max_height
        if (!max_width) {
            if (max_height) {
                // max_width == 0
                height = Math.min(img_height, max_height);
                width = Math.round(height * ratio);
            } else {
                // max_width == 0 && max_height == 0
                width = img_width;
                height = img_height;
            }
        } else if (!height) {
            // max_height == 0
            width = Math.min(img_width, max_width);
            height = Math.round(width / ratio);
        }

        // Ограничение IE
        if (width > 4096) {
            width = 4096;
            height = Math.round(width / ratio);
        }
        if (height > 4096) {
            height = 4096;
            width = Math.round(height * ratio);
        }

        // Ограничение iOS
        if (width * height > 5000000) {
            width = Math.floor(Math.sqrt(5000000 * ratio));
            height = Math.floor(5000000 / Math.sqrt(5000000 * ratio));
        }

        return {
            width: width,
            height: height
        };
    };


    /*
        Создает Deferred-объект, который загружает картинку из файла.
    */
    $.fileReaderDeferred = function(file) {
        var df = $.Deferred();
        if (!window.FileReader) {
            return df.reject('FileReader not supported');
        }
        if (file instanceof Blob == false) {
            return df.reject('Not a file');
        }

        var reader = new FileReader();
        reader.onload = function(event) {
            df.resolve(event.target.result);
        };
        reader.onerror = function() {
            df.reject('can not read');
        };
        reader.readAsDataURL(file);
        return df.promise();
    };


    /*
        Создает Deferred-объект, который загружает картинку.
    */
    $.imageDeferred = function(src) {
        var df = $.Deferred();
        var img = new Image();
        img.onload = function() {
            df.resolve(this);
        };
        img.onerror = function() {
            df.reject('Not image');
        };
        img.src = src;
        return df.promise();
    };


    /*
        Возвращает canvas с картинкой с указанными ограничениями размеров.
        Можно не указывать размеры, или указать один из них.

        Уменьшение размера происходит очень быстро, но некачественно.

        Пример:
            $.fileReaderDeferred($('#test').prop('files').item(0)).done(function(src) {
                $.imageDeferred(src).done(function(img) {
                    var canvas = $.imageToCanvas(img, 360, 360);
                    $('#test').after(canvas);
                });
            });
    */
    $.imageToCanvas = function(source, max_width, max_height) {
        // Первое уменьшение до максимально возможного размера
        var canvas = document.createElement("canvas");
        $.extend(canvas, canvasSize(
            source.width, source.height, max_width, max_height
        ));
        var context = canvas.getContext && canvas.getContext('2d');
        if (!context) {
            console.error('Canvas not supported');
            return
        }
        context.drawImage(source, 0, 0, canvas.width, canvas.height);
        return canvas;
    };


    /*
        Возвращает Deferred-объект, который возвращает canvas с картинкой с
        указанными ограничениями размеров.
        Можно не указывать размеры, или указать один из них.

        Качество выше, чем у $.imageToCanvas, но всё равно не идеально.
        Для лучшего качества используете плагин pica: https://github.com/nodeca/pica

        Пример:
            $.fileReaderDeferred($('#test').prop('files').item(0)).done(function(src) {
                $.imageDeferred(src).done(function(img) {
                    $.imageToCanvasDeferred(img, 360, 360).done(function(canvas) {
                        $('#test').after(canvas);
                    });
                });
            });
    */
    $.imageToCanvasDeferred = function(source, max_width, max_height) {
        var df = $.Deferred();

        // Первое уменьшение. Максимальный размер
        var canvas = $.imageToCanvas(source);
        var source_size = {
            width: canvas.width,
            height: canvas.height
        };


        var context = canvas.getContext('2d');
        var target_size = canvasSize(canvas.width, canvas.height, max_width, max_height);
        var step_func = function(dim) {
            return Math.round(dim * 0.5);
        };

        // Последовательное уменьшение canvas
        var run;
        (run = function() {
            if (source_size.width <= target_size.width) {
                return df.resolve(canvas);
            }

            setTimeout(function() {

                if (step_func(source_size.width) <= target_size.width) {
                    // Последний шаг
                    var temp_canvas = document.createElement("canvas");
                    temp_canvas.width = target_size.width;
                    temp_canvas.height = target_size.height;
                    temp_canvas.getContext('2d').drawImage(canvas,
                        0, 0, source_size.width, source_size.height,
                        0, 0, temp_canvas.width, temp_canvas.height
                    );

                    canvas.src = 'about:blank';
                    canvas.width = 1;
                    canvas.height = 1;

                    canvas = temp_canvas;
                    source_size = target_size;
                } else {
                    context.drawImage(canvas,
                        0, 0, source_size.width, source_size.height,
                        0, 0, step_func(source_size.width), step_func(source_size.height));
                    source_size.width = step_func(source_size.width);
                    source_size.height = step_func(source_size.height);
                }

                run();
            }, 0);
        })();

        return df.promise();
    };

    /*
        Позиционирует $image внутри $container, чтобы показать центральную область картинки.
    */
    $.placeImage = function($container, $image, coords) {
        var container_w = $container.width();
        var container_h = $container.height();
        var container_ratio = container_w / container_h;
        var img_w = $image.prop('naturalWidth');
        var img_h = $image.prop('naturalHeight');
        var img_ratio = img_w / img_h;
        var coords_ratio, float_h, float_w, crop_top, crop_left;

        if (!coords) {
            coords = [0, 0, img_w, img_h];
            coords_ratio = img_ratio;
        } else {
            coords_ratio = coords[2] / coords[3];
        }

        if (img_ratio >= container_ratio) {
            float_h = (container_h * img_h) / coords[3];
            float_w = float_h * img_ratio;
            crop_top = (coords[1] * float_h) / img_h;
            crop_left = (coords[0] * float_w) / img_w;
            var crop_w = Math.round( container_h * coords_ratio );
            $image.css({
                width: Math.round( float_w ),
                height: Math.round( float_h ),
                left: -Math.round( crop_left + ((crop_w - container_w) / 2) ),
                top: -Math.round( crop_top )
            });
        } else {
            float_w = (container_w * img_w) / coords[2];
            float_h = float_w / img_ratio;
            crop_top = (coords[1] * float_h) / img_h;
            crop_left = (coords[0] * float_w) / img_w;
            var crop_h = Math.round( container_w / coords_ratio );
            $image.css({
                width: Math.round( float_w ),
                height: Math.round( float_h ),
                left: -Math.round( crop_left ),
                top: -Math.round( crop_top + ((crop_h - container_h) / 2) )
            });
        }
    };

})(jQuery);