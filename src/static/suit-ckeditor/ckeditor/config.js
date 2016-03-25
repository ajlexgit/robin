/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
    // Define changes to default configuration here. For example:
    config.linkShowAdvancedTab = false;
    config.linkShowTargetTab = false;
    config.dataIndentationChars = '  ';
    config.tabSpaces = 2;

    config.format_tags = "p;h2;h3;h4";

    CKEDITOR.on('instanceReady', function(ev) {
        var blockTags = ['div', 'p', 'pre', 'ul', 'ol', 'li'];
        var rules = {
            indent: true,
            breakBeforeOpen: false,
            breakAfterOpen: true,
            breakBeforeClose: true,
            breakAfterClose: true
        };

        for (var i = 0; i < blockTags.length; i++) {
            ev.editor.dataProcessor.writer.setRules(blockTags[i], rules);
        }

        ev.editor.dataProcessor.writer.setRules('img', {
            indent: true,
            breakBeforeOpen: false,
            breakAfterOpen: false,
            breakBeforeClose: true,
            breakAfterClose: true
        });

        ev.editor.dataProcessor.writer.setRules('a', {
            indent: true
        });

        ev.editor.dataProcessor.writer.setRules('span', {
            indent: true,
            breakBeforeOpen: true,
            breakAfterOpen: false,
            breakBeforeClose: false,
            breakAfterClose: true
        });
    });
};
