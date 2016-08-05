(function() {
    CKEDITOR.plugins.add("image_attrs", {
        requires: 'dialog',
        init: function (editor) {
            // ======================================
            //      Dialog
            // ======================================
            CKEDITOR.dialog.add("imageAttrsDialog", this.path + "dialogs/image_attrs.js");

            // ======================================
            //      Commandes
            // ======================================
            editor.addCommand('imageAttrs', new CKEDITOR.dialogCommand('imageAttrsDialog'));


            // ======================================
            //      Context Menu
            // ======================================
            if (editor.contextMenu) {
                editor.addMenuGroup('imageGroup', 110);
                editor.addMenuItem('imageAttrsItem', {
                    label: 'Edit image attributes',
                    icon: this.path + 'icons/image_attrs.png',
                    command: 'imageAttrs',
                    group: 'imageGroup'
                });

                editor.contextMenu.addListener(function(element) {
                    if (element && element.is('img') && !element.isReadOnly()) {
                        return {
                            imageAttrsItem: CKEDITOR.TRISTATE_OFF
                        }
                    }
                });
            }
        }
    })

})();
