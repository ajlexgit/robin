from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Campaign


def preview_campaign(request, campaign_id):
    from premailer import Premailer
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    content = campaign.render_html(request, test=True)
    content = Premailer(content, strip_important=False).transform()
    return HttpResponse(content)


def preview_campaign_plain(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    content = campaign.render_plain(request, test=True)
    return HttpResponse('<pre>%s</pre>' % content.strip())
