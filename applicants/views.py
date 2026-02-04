from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ApplicantProfile, AdmissionApplication, Document
from core.models import CareerProfile, Program
from .proftest_data import QUESTIONS
import json

# Helper to force translation evaluation
def force_str_recursive(obj):
    if isinstance(obj, dict):
        return {k: force_str_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [force_str_recursive(v) for v in obj]
    else:
        return str(obj)

def career_test_view(request):
    # 1. Get Profiles Data
    profiles = CareerProfile.objects.all()
    profiles_data = {
        p.code: {
            'title': p.title,
            'description': p.description,
        } for p in profiles
    }

    # 2. Get Programs grouped by Profile
    # We fetch ALL programs that have a profile assigned.
    # You will assign them manually in Admin, so we just read what's there.
    programs = Program.objects.filter(career_profile__isnull=False).select_related('career_profile')
    
    programs_by_profile = {code: [] for code in ['A', 'B', 'C', 'D', 'E', 'F']}
    
    for prog in programs:
        code = prog.career_profile.code
        if code in programs_by_profile:
            programs_by_profile[code].append({
                'id': prog.id,
                'title': prog.title,
                'code': getattr(prog, 'code', ''), # explicit code field
                'url': '#', # Placeholder, logic to link to program detail can be added
            })
    
    # Limit to 6 programs per profile for display
    for code in programs_by_profile:
        programs_by_profile[code] = programs_by_profile[code][:6]

    # 3. Process Questions
    # We convert the PROFTEST_DATA structure into JSON, forcing translation evaluation
    resolved_questions = force_str_recursive(QUESTIONS)

    context = {
        'profiles_json': json.dumps(profiles_data),
        'programs_json': json.dumps(programs_by_profile),
        'questions_json': json.dumps(resolved_questions),
    }
    return render(request, 'applicants/career_test.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('applicants:dashboard')
        
    if request.method == 'POST':
        iin = request.POST.get('iin')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Simple Validation
        if not iin or not password:
            messages.error(request, "Заполните все обязательные поля")
            return render(request, 'applicants/register.html')
            
        if password != password_confirm:
            messages.error(request, "Пароли не совпадают")
            return render(request, 'applicants/register.html')
            
        if User.objects.filter(username=iin).exists():
            messages.error(request, "Пользователь с таким ИИН уже существует")
            return render(request, 'applicants/register.html')
        
        try:
            # Create User
            user = User.objects.create_user(username=iin, password=password)
            
            # Create Profile
            ApplicantProfile.objects.create(user=user, iin=iin, phone=phone)
            
            # Login immediately
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('applicants:dashboard')
        except Exception as e:
            messages.error(request, f"Ошибка при регистрации: {str(e)}")
            return render(request, 'applicants/register.html')

    return render(request, 'applicants/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('applicants:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('applicants:dashboard')
        else:
            return render(request, 'applicants/login.html', {'form': {'errors': True}})
            
    return render(request, 'applicants/login.html')

def logout_view(request):
    logout(request)
    return redirect('applicants:login')

@login_required(login_url='applicants:login')
def dashboard_view(request):
    # Retrieve summary data for dashboard
    profile = request.user.applicant_profile
    applications = profile.applications.all()
    # Check for latest draft
    latest_draft = applications.filter(status='DRAFT').order_by('-updated_at').first()
    
    documents = profile.documents.all()
    
    # Calculate stats
    docs_uploaded = documents.count()
    # Assuming 8 required docs as per template placeholder
    docs_required = 8 

    # Fetch latest career test result
    from .models import CareerTestResult
    test_result = CareerTestResult.objects.filter(user=request.user).order_by('-created_at').first()
    
    context = {
        'applications': applications,
        'latest_draft': latest_draft,
        'docs_uploaded': docs_uploaded,
        'docs_required': docs_required,
        'docs_missing': max(0, docs_required - docs_uploaded),
        'test_result': test_result,
    }
    return render(request, 'applicants/dashboard.html', context)

@login_required(login_url='applicants:login')
def profile_edit_view(request):
    profile = request.user.applicant_profile
    
    if request.method == 'POST':
        # User fields
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()
        
        # Profile fields
        profile.patronymic = request.POST.get('patronymic')
        profile.phone = request.POST.get('phone')
        profile.gender = request.POST.get('gender')
        profile.address = request.POST.get('address')
        
        birth_date = request.POST.get('birth_date')
        if birth_date:
            profile.birth_date = birth_date
            
        profile.save()
        messages.success(request, "Профиль обновлен")
        return redirect('applicants:profile_edit')
        
    return render(request, 'applicants/profile_edit.html')

@login_required(login_url='applicants:login')
def application_list_view(request):
    applications = request.user.applicant_profile.applications.all().order_by('-created_at')
    return render(request, 'applicants/application_list.html', {'applications': applications})

@login_required(login_url='applicants:login')
def application_create_view(request):
    from core.models import Program
    
    if request.method == 'POST':
        program_id = request.POST.get('program')
        study_language = request.POST.get('study_language')
        
        if program_id:
            program = Program.objects.get(id=program_id)
            # Create as SUBMITTED directly as per "Send Application" button
            AdmissionApplication.objects.create(
                applicant=request.user.applicant_profile,
                program=program,
                study_language=study_language,
                status='SUBMITTED' 
            )
            messages.success(request, "Заявка успешно отправлена")
            return redirect('applicants:application_list')
            
    programs = Program.objects.all()
    return render(request, 'applicants/application_form.html', {'programs': programs})

@login_required(login_url='applicants:login')
def application_detail_view(request, pk):
    application = get_object_or_404(AdmissionApplication, pk=pk, applicant=request.user.applicant_profile)
    return render(request, 'applicants/application_detail.html', {'app': application})

@login_required(login_url='applicants:login')
def document_list_view(request):
    documents = request.user.applicant_profile.documents.all().order_by('-uploaded_at')
    return render(request, 'applicants/document_list.html', {'documents': documents})

@login_required(login_url='applicants:login')
def document_upload_view(request):
    if request.method == 'POST':
        doc_type = request.POST.get('doc_type')
        uploaded_file = request.FILES.get('file')
        
        if doc_type and uploaded_file:
            Document.objects.create(
                applicant=request.user.applicant_profile,
                doc_type=doc_type,
                file=uploaded_file
            )
            messages.success(request, "Документ загружен")
            return redirect('applicants:document_list')
        else:
            messages.error(request, "Выберите файл и тип документа")
            
    return render(request, 'applicants/document_form.html')

@login_required(login_url='applicants:login')
def dormitory_request_view(request):
    from .models import DormitoryRequest
    
    # Check if already applied
    existing = DormitoryRequest.objects.filter(applicant=request.user.applicant_profile).first()
    
    if request.method == 'POST':
        needs_dorm = request.POST.get('needs_dorm') == 'on'
        comment = request.POST.get('comment')
        
        if existing:
            existing.needs_dorm = needs_dorm
            existing.comment = comment
            existing.save()
            messages.success(request, "Заявка на общежитие обновлена")
        else:
            DormitoryRequest.objects.create(
                applicant=request.user.applicant_profile,
                needs_dorm=needs_dorm,
                comment=comment
            )
            messages.success(request, "Заявка на общежитие подана")
        return redirect('applicants:dashboard')
        
    return render(request, 'applicants/dormitory_form.html', {'request_obj': existing})

