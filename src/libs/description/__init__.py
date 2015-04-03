from .description import strip_tags_except, description

"""
    strip_tags_except(html, valid_tags=())
        Удаление HTML-тэгов, кроме перечисленных в valid_tags
    
    description(text, minlen, maxlen)
        Собираем параграфы до достижения заданной длины.
        Если недобрали - добираем предложениями из следующего параграфа.
        Принимает текст, разделенный на параграфы символом перевода строки.
        
    Шаблонные фильтры:
        <!-- удалит из текста все тэги, кроме <a> и <p>, обрежет до наилучшего результата
             длиной от 100 до 150 символов, превратит переносы строки в <br> -->
        {{ text|strip_tags_except:"a, p"|description:"100, 150"|safe|linebreaks }}
"""