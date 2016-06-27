from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Campaign


def preview_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    content = campaign.render_html(request)
    content = content.replace('{$url}', '#')
    content = content.replace('{$unsubscribe}', '#')
    content = content.replace('{$email}', 'john@smithmail.com')
    content = content.replace('{$name}', 'John')
    content = content.replace('{$last_name}', 'Smith')
    content = content.replace('{$company}', 'Microsoft')
    return HttpResponse(content)


def preview_campaign_plain(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    content = campaign.render_plain(request)
    content = content.replace('{$url}', '#')
    content = content.replace('{$unsubscribe}', '#')
    content = content.replace('{$email}', 'john@smithmail.com')
    content = content.replace('{$name}', 'John')
    content = content.replace('{$last_name}', 'Smith')
    content = content.replace('{$company}', 'Microsoft')
    return HttpResponse('<pre>%s</pre>' % content.strip())
