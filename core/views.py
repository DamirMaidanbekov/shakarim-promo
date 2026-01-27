from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils.translation import gettext as _
from .models import Program, CalendarEvent, TuitionFee, GrantBenefit, FAQ, SiteConfig, Lead
import json

class LandingView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['programs'] = Program.objects.all()
        context['calendar_events'] = CalendarEvent.objects.all()
        # Sort calendar in python or DB. DB is better.
        context['tuition_fees'] = TuitionFee.objects.all()
        context['benefits'] = GrantBenefit.objects.all()
        context['faqs'] = FAQ.objects.all()
        context['config'] = SiteConfig.objects.first()
        return context

def submit_lead(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            lead = Lead.objects.create(
                name=data.get('name'),
                phone=data.get('phone'),
                email=data.get('email', ''),
                level=data.get('level', ''),
                program=data.get('program', ''),
                comment=data.get('comment', '')
            )
            # Here we could add Zoho integration task
            return JsonResponse({'status': 'success', 'message': _('Application received!')})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

