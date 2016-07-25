(function($) {

    var $form;

    $(document).ready(function() {
        $form = $('#autopost-dialog').find('form').detach();
    });

    $(document).on('click', '.social-share-btn', function() {
        if (!$form.length) {
            return false;
        }

        var $dialog_form = $form.clone();
        $dialog_form.get(0).reset();
        $dialog_form.attr('id', 'autopost-form');
        $dialog_form.dialog({
            title: gettext('Share to social networks'),
            width: 550,
            closeText: '',
            show: {
                effect: "fadeIn",
                duration: 100
            },
            hide: {
                effect: "fadeOut",
                duration: 100
            },
            modal: true,
            draggable: false,
            resizable: false,
            position: {
                my: "center center",
                at: "center center",
                of: window
            },
            buttons: [
                {
                    text: "Cancel",
                    "class": 'btn',
                    icons: {
                        primary: "ui-icon-cancel"
                    },
                    click: function() {
                        $(this).dialog("close");
                    }
                },
                {
                    text: "Ok",
                    "class": 'btn btn-info',
                    icons: {
                        primary: "ui-icon-check"
                    },
                    click: function() {
                        var $this = $(this);
                        var dialog = $this.dialog('instance');

                        if (dialog.uiDialog.hasClass('autopost-preload')) {
                            return
                        }

                        $.ajax({
                            url: $this.attr('action'),
                            type: $this.attr('method'),
                            data: $this.serialize(),
                            beforeSend: function() {
                                dialog.uiDialog.addClass('autopost-preload');
                            },
                            success: function() {
                                dialog.close();
                            },
                            error: function(xhr) {
                                if (xhr.statusText == 'abort') {
                                    return
                                }

                                if (xhr.responseText) {
                                    try {
                                        var response = $.parseJSON(xhr.responseText + "");
                                        var errors = [];
                                        for (var field in response.errors) {
                                            if (response.errors.hasOwnProperty(field)) {
                                                errors.push(response.errors[field][0])
                                            }
                                        }

                                        alert(errors.join('\n'));
                                    } catch (err) {
                                        // ответ - не JSON
                                        alert(gettext('Undefined server error'))
                                    }
                                } else {
                                    alert(xhr.responseText);
                                }
                            },
                            complete: function() {
                                dialog.uiDialog.removeClass('autopost-preload');
                            }
                        });
                    }
                }
            ],
            open: function() {
                var $this = $(this);
                var dialog = $this.dialog('instance');
                var $textarea = $this.find('textarea');
                if ($.fn.autosize) {
                    $textarea.autosize({
                        callback: function() {
                            if (dialog.widget().outerHeight() < $.winHeight()) {
                                dialog._position();
                            }
                        }
                    });
                }
            },
            close: function() {
                $(this).dialog('destroy');
            }
        });

        return false;
    });

})(jQuery);