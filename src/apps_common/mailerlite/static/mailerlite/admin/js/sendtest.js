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
            minWidth: 550,
            closeText: '',
            modal: true,
            resizable: false,
            show: {
                effect: "fadeIn",
                duration: 100
            },
            hide: {
                effect: "fadeOut",
                duration: 100
            },
            open: function() {
                var $form = $(this);
                var dialog = $form.dialog('instance');

                var $textareas = $form.find('textarea');
                if ($.fn.autosize) {
                    $textareas.autosize();
                    dialog._position();
                }
            },
            close: function() {
                $(this).dialog('destroy');
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
                        var $form = $(this);
                        var dialog = $form.dialog('instance');

                        if (dialog.uiDialog.hasClass('autopost-preload')) {
                            return
                        }

                        $.ajax({
                            url: $form.attr('action'),
                            type: $form.attr('method'),
                            data: $form.serialize(),
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
            ]
        });

        return false;
    });

})(jQuery);