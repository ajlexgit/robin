(function($) {

	CKEDITOR.dialog.add("pagevideos", function (editor) {
		return {
            title: gettext('Insert video'),
            minWidth: 600,
            minHeight: 400,
            contents: [{
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [
					{
						type: 'html',
						id: 'oembedHeader',
						html: gettext('Input URL containing video (YouTube, Flickr, Vimeo etc)')
					},
					{
						type: 'text',
						id: 'embedCode',
						label: 'URL',
						title: gettext('Input URL containing video (YouTube, Flickr, Vimeo etc)')
					}
				]
            }],

			onShow: function() {
				var container = editor.getSelection().getStartElement(),
					element = $(container.$);

				if (container.hasClass(CKEDITOR.config.pagevideos.classname)) {
					this.setValueOf('tab-basic', 'embedCode', element.data('url'))
				}
			},

			onOk: function() {
				var url = this.getValueOf( 'tab-basic', 'embedCode' ),
                    provider = $.fn.oembed.getOEmbedProvider(url),
					container = editor.getSelection().getStartElement();

				// Вставка родительского контейнера
				if (!container.hasClass(CKEDITOR.config.pagevideos.classname)) {
                    container = editor.document.createElement('p');
                    container.addClass(CKEDITOR.config.pagevideos.classname);
					editor.insertElement(container)
                }

                container.addClass(provider.name);
                var $container = $(container.$);

                // Fix for instagram
                if (provider.name == 'instagram') {
                    var code = /\/p\/([^\/]+)/g.exec(url);
                    if (!code || (code.length < 2)) {
                        alert('Wrong instagram url');
                        return
                    }

                    $container.attr('data-url', url).data('url', url);

                    var iframe = editor.document.createElement('iframe');
                    var $iframe = $(iframe.$).attr({
                        src: 'https://instagram.com/p/' +code[1] + '/embed/captioned/?v=4',
                        width: 480,
                        height: 600,
                        frameborder: 0,
                        scrolling: 'no',
                        allowtransparency: ''
                    });
                    $container.html($iframe);

                    var script = editor.document.createElement('script');
                    var $script = $(script.$).attr({
                        src: '//platform.instagram.com/en_US/embeds.js'
                    });
                    $container.append($script);

                    var dialog = CKEDITOR.dialog.getCurrent();
                    if (dialog) {
                        dialog.hide();
                    }
                    return
                }

                $container.oembed(url, {
                    onEmbed: function(e) {
                        if (typeof e.code === 'string') {
                            $container.html(e.code);
                        } else if (typeof e.code[0].outerHTML === 'string') {
                            // Вставка HTML-кода
                            var video = $container.find('iframe');

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
                                    $container.html(e.code)
                                }
                            } else if (typeof e.code[0].outerHTML === 'string') {
                                if (video.length) {
                                    video.replaceWith(e.code[0].outerHTML)
                                } else {
                                    $container.html(e.code[0].outerHTML)
                                }
                            } else {
                                alert(gettext('Incorrect URL'))
                            }

                            // Youtube size
                            if (provider.name == 'youtube') {
                                var key = provider.templateRegex.exec(url)[1];
                                $.ajax({
                                    url: 'https://www.googleapis.com/youtube/v3/videos?id=' + key + '&key=AIzaSyB4CphiSoXhku-rP9m5-QkXE9U11OJkOzg&part=player',
                                    dataType: "jsonp",
                                    success: function (data) {
                                        if (data.items && data.items.length) {
                                            var item = data.items[0];
                                            var code = item.player && item.player.embedHtml;
                                            if (code) {
                                                var width = /width="(\d+)"/i.exec(code);
                                                var height = /height="(\d+)"/i.exec(code);

                                                if (width && height) {
                                                    width = parseInt(width[1]);
                                                    height = parseInt(height[1]);

                                                    height = Math.ceil((height / width) * 425) + 25;
                                                    width = 425;

                                                    $(container.$).find('iframe').attr({
                                                        width: width,
                                                        height: height
                                                    });
                                                }
                                            }
                                        }
                                    }
                                });
                            }
                        } else {
                            alert('Unknown URL service');
                        }

                        $container.attr('data-url', url).data('url', url);
                        var dialog = CKEDITOR.dialog.getCurrent();
                        if (dialog) {
                            dialog.hide();
                        }
					},
					onError: function(externalUrl) {
						if (externalUrl.indexOf("vimeo.com") > 0) {
							alert(gettext('You can not share this video'))
						} else {
							alert(gettext('Video not found. Trying other mirror'))
						}
					},
					embedMethod: 'editor'
				})
			}
        }
	})

})(jQuery);