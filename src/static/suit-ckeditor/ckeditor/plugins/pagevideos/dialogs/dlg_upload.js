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