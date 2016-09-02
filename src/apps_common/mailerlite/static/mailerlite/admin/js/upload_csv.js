(function($) {

    $(document).ready(function() {

        var $button = $('.upload-csv');
        Uploader($button, {
            url: $button.data('url'),
            fileName: 'csv',
            multiple: false,
            max_size: '40mb',
            mime_types: [
                {title: "CSV files", extensions: "csv"}
            ],
            prevent_duplicates: false,
            onFileAdded: function() {
                $('<h3>').text(
                    gettext('Please, wait...')
                ).dialog({
                    dialogClass: 'upload-csv-dialog',
                    modal: true,
                    draggable: false,
                    resizable: false,
                    closeOnEscape: false,
                    open: function(event, ui) {
                        $(".ui-dialog-titlebar-close", ui.dialog | ui).hide();
                    }
                });
            },
            onUploadComplete: function() {
                location.reload();
            }
        });

    });

})(jQuery);
