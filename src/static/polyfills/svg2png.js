(function() {

    var background_url = /url\((.*\.svg)\)/i;
    var svg = /\.svg/i;


    // получение абсолютного пути по относительному
    function absolute(base, relative) {
        var stack = base.split("/"),
            parts = relative.split("/");

        if (parts[0] == '') {
            return relative
        }

        // remove current file name (or empty string)
        stack.pop();

        for (var i=0; i<parts.length; i++) {
            if (parts[i] == ".")
                continue;
            if (parts[i] == "..")
                stack.pop();
            else
                stack.push(parts[i]);
        }
        return stack.join("/");
    }


    function doMatched(rules) {
        var style_content = '';

        // добавление fallback-стиля в текст
        var add_new_style = function(selectors, new_url, base) {
            if (base) {
                new_url = absolute(base, new_url);
            }

            style_content += selectors + '{background-image: url(' + new_url + ');}\n';
        };

        // замена SVG на PNG
        rules.each(function(rule) {
            var declarations = rule.getDeclaration();
            var match, new_url;

            if ('background' in declarations) {
                match = background_url.exec(declarations['background']);
                if (match) {
                    new_url = match[1].replace(svg, '.png');
                    add_new_style(rule.getSelectors(), new_url, rule.getUrl());
                }
            } else if ('background-image' in declarations) {
                new_url = declarations['background-image'].replace(svg, '.png');
                add_new_style(rule.getSelectors(), new_url, rule.getUrl());
            }
        });

        // добавление тега style
        var head = document.head || document.getElementsByTagName('head')[0];
        var style = document.createElement('style');
        style.type = 'text/css';
        if (style.styleSheet){
          style.styleSheet.cssText = style_content;
        } else {
          style.appendChild(document.createTextNode(style_content));
        }
        head.appendChild(style);
    }

    Polyfill({
        declarations:["background-image:*\\.svg\\)", "background:*\\.svg\\)*"]
    }).doMatched(doMatched)

})();