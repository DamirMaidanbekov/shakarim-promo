from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils.translation import gettext as _
from .models import Program, CalendarEvent, TuitionFee, GrantBenefit, FAQ, SiteConfig, Lead, CareerProfile
from applicants.proftest_data import QUESTIONS
import json

def force_str_recursive(obj):
    if isinstance(obj, dict):
        return {k: force_str_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [force_str_recursive(v) for v in obj]
    else:
        return str(obj)

class LandingView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Standard Data
        context['programs'] = Program.objects.select_related('unt_combination', 'career_profile').all()
        context['calendar_events'] = CalendarEvent.objects.all()
        context['tuition_fees'] = TuitionFee.objects.all()
        context['benefits'] = GrantBenefit.objects.all()
        context['faqs'] = FAQ.objects.all()
        context['config'] = SiteConfig.objects.first()

        # Check for existing test result for logged-in user
        if self.request.user.is_authenticated:
            from applicants.models import CareerTestResult
            try:
                last_result = CareerTestResult.objects.filter(user=self.request.user).latest('created_at')
                scores = last_result.scores
                if isinstance(scores, str):
                    try:
                        scores = json.loads(scores)
                    except json.JSONDecodeError:
                        scores = {}
                context['user_test_result'] = json.dumps(scores)
            except CareerTestResult.DoesNotExist:
                context['user_test_result'] = 'null'
        else:
            context['user_test_result'] = 'null'

        # Career Test Data
        # 1. Profiles
        profiles = CareerProfile.objects.all()
        profiles_data = {
            p.code: {
                'title': p.title,
                'description': p.description,
            } for p in profiles
        }
        context['profiles_json'] = json.dumps(profiles_data)

        # 2. Programs for Test Results
        programs_with_profile = [p for p in context['programs'] if p.career_profile]
        programs_by_profile = {code: [] for code in ['A', 'B', 'C', 'D', 'E', 'F']}
        
        for prog in programs_with_profile:
            code = prog.career_profile.code
            if code in programs_by_profile:
                programs_by_profile[code].append({
                    'id': prog.id,
                    'title': prog.title,
                    'code': getattr(prog, 'code', ''),
                    'profile_code': code,
                    'level': prog.get_level_display(), 
                    'salary': prog.salary_start,
                    'hard_skills': prog.hard_skills,
                    'soft_skills': prog.soft_skills,
                    'slogan': prog.slogan,
                    'main_info': prog.main_info,
                    'what_learn': prog.what_will_learn,
                    'career_track': prog.career_track,
                    'star_graduates': prog.star_graduates,
                    'star_teachers': prog.star_teachers,
                    'brochureUrl': prog.brochure.url if prog.brochure else '',
                    'advantages': [
                        prog.advantage_1,
                        prog.advantage_2,
                        prog.advantage_3
                    ],
                    'languages': {
                        'kaz': prog.lang_kaz,
                        'rus': prog.lang_rus,
                        'eng': prog.lang_eng
                    },
                    'description': prog.description,
                    'unt_combination': str(prog.unt_combination) if prog.unt_combination else '',
                    'unt_subjects': prog.unt_subjects,
                })
        
        # Limit to 6
        for code in programs_by_profile:
            programs_by_profile[code] = programs_by_profile[code][:6]
            
        context['programs_json'] = json.dumps(programs_by_profile)

        # 3. Questions
        resolved_questions = force_str_recursive(QUESTIONS)
        context['questions_json'] = json.dumps(resolved_questions)

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


from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
import json

@require_POST
@login_required
def save_test_result(request):
    try:
        data = json.loads(request.body)
        scores = data.get('scores')
        
        if not scores:
            return JsonResponse({'status': 'error', 'message': 'No scores provided'}, status=400)

        from core.models import CareerProfile

        # Determine winner
        top_profile = None
        if scores and len(scores) > 0:
            # Sort by score desc
            sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
            if sorted_scores:
                winner_code = sorted_scores[0][0]
                top_profile = CareerProfile.objects.filter(code=winner_code).first()

        # Save new result
        CareerTestResult.objects.create(
            user=request.user,
            scores=scores,
            top_profile=top_profile
        )
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
