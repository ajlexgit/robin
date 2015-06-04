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
					container = editor.getSelection().getStartElement();

				// Вставка родительского контейнера
				if (!container.hasClass(CKEDITOR.config.pagevideos.classname)) {
                    container = editor.document.createElement('p');
                    container.addClass(CKEDITOR.config.pagevideos.classname);
					editor.insertElement(container)
                }

				$(container).oembed(url, {
                    onEmbed: function(e) {
						// Вставка HTML-кода
						var element = $(container.$),
							video = element.find('iframe');

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
								element.html(e.code)
							}
						} else if (typeof e.code[0].outerHTML === 'string') {
							if (video.length) {
								video.replaceWith(e.code[0].outerHTML)
							} else {
								element.html(e.code[0].outerHTML)
							}
						} else {
							alert(gettext('Incorrect URL'))
						}

                        // Youtube size
                        var info = $.fn.oembed.getOEmbedProvider(url);

                        if (info.name == 'youtube') {
                            var key = info.templateRegex.exec(url)[1];
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

						element.attr('data-url', url).data('url', url);
						CKEDITOR.dialog.getCurrent().hide()
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