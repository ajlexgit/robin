(function($) {

    CKEDITOR.dialog.add("pagevideos", function (editor) {
        var lang = editor.lang.pagevideos;
        return {
            title: lang.dialogTitle,
            minWidth: 500,
            minHeight: 150,
            contents: [{
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [
                    {
                        type: 'html',
                        id: 'oembedHeader',
                        html: lang.dialogLabel
                    },
                    {
                        type: 'text',
                        id: 'embedCode',
                        label: 'URL',
                        title: lang.dialogLabel
                    }
                ]
            }],

            onShow: function() {
                var element = editor.getSelection().getStartElement();
                var embedCode = this.getContentElement('tab-basic', 'embedCode').getInputElement();

                if (element.hasClass('page-video')) {
                    embedCode.setValue(element.data('url'));
                }

                embedCode.focus(true);
            },

            onOk: function() {
                var element = editor.getSelection().getStartElement();
                var url = this.getValueOf('tab-basic', 'embedCode');
                var provider = $.fn.oembed.getOEmbedProvider(url);
                var dialog = this;

                // Вставка родительского контейнера
                if (!element.hasClass('page-video')) {
                    element = editor.document.createElement('p');
                    element.addClass('page-video');
                    editor.insertElement(element);
                }

                element.addClass(provider.name);
                var $element = $(element.$);

                // Fix for instagram
                if (provider.name == 'instagram') {
                    var code = /\/p\/([^\/]+)/g.exec(url);
                    if (!code || (code.length < 2)) {
                        alert('Wrong instagram url');
                        return
                    }

                    $element.attr('data-url', url).data('url', url);

                    var iframe = editor.document.createElement('iframe');
                    var $iframe = $(iframe.$).attr({
                        src: 'https://instagram.com/p/' +code[1] + '/embed/captioned/?v=4',
                        width: 480,
                        height: 600,
                        frameborder: 0,
                        scrolling: 'no',
                        allowtransparency: ''
                    });
                    $element.html($iframe);

                    var script = editor.document.createElement('script');
                    var $script = $(script.$).attr({
                        src: '//platform.instagram.com/en_US/embeds.js'
                    });
                    $element.append($script);

                    dialog.hide();
                    return
                }

                $element.oembed(url, {
                    embedMethod: 'editor',
                    onEmbed: function(e) {
                        if (typeof e.code === 'string') {
                            $element.html(e.code);
                        } else if (typeof e.code[0].outerHTML === 'string') {
                            // Вставка HTML-кода
                            var video = $element.find('iframe');

                            // rel=0 for youtube
                            if (e.code[0].src.indexOf('?') >= 0) {
                                e.code[0].src += '&rel=0';
                            } else {
                                e.code[0].src += '?rel=0';
                            }

                            if (typeof e.code === 'string') {
                                if (video.length) {
                                    video.replaceWith(e.code)
                                } else {
                                    $element.html(e.code)
                                }
                            } else if (typeof e.code[0].outerHTML === 'string') {
                                if (video.length) {
                                    video.replaceWith(e.code[0].outerHTML)
                                } else {
                                    $element.html(e.code[0].outerHTML)
                                }
                            } else {
                                alert(gettext('Incorrect URL'))
                            }

                            // Youtube size
                            if (provider.name == 'youtube') {
                                var key = provider.templateRegex.exec(url)[1];
                                var apikey = editor.config.YOUTUBE_APIKEY;
                                $.ajax({
                                    url: 'https://www.googleapis.com/youtube/v3/videos?id=' + key + '&key=' + apikey + '&part=player',
                                    dataType: "jsonp",
                                    success: function (data) {
                                        if (!data.items || !data.items.length) {
                                            return
                                        }

                                        var item = data.items[0];
                                        var code = item.player && item.player.embedHtml;
                                        if (!code) {
                                            return
                                        }

                                        var $code = $(code);
                                        var width = /width="(\d+)"/i.exec(code);
                                        var height = /height="(\d+)"/i.exec(code);
                                        if (width && height) {
                                            width = parseInt(width[1]);
                                            height = parseInt(height[1]);
                                            $code.attr({
                                                width: 425,
                                                height: Math.ceil((height / width) * 425) + 25
                                            });
                                        }

                                        $(element.$).find('iframe').replaceWith($code);
                                    }
                                });
                            }
                        } else {
                            alert(lang.unknown);
                        }

                        $element.attr('data-url', url).data('url', url);
                        dialog.hide();
                    }
                })
            }
        }
    })

})(jQuery);
