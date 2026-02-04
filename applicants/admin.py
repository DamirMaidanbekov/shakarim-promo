from django.contrib import admin
from .models import ApplicantProfile, EducationInfo, AdmissionApplication, Document, CareerTestResult

class EducationInfoInline(admin.StackedInline):
    model = EducationInfo
    can_delete = False
    verbose_name_plural = 'Education Info'

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0

class ApplicationInline(admin.TabularInline):
    model = AdmissionApplication
    extra = 0

@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'iin', 'phone', 'created_at')
    search_fields = ('user__username', 'iin', 'phone')
    inlines = [EducationInfoInline, DocumentInline, ApplicationInline]

@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'program', 'status', 'created_at')
    list_filter = ('status', 'program')
    search_fields = ('applicant__user__username', 'applicant__iin')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'type', 'uploaded_at')
    list_filter = ('type',)

@admin.register(CareerTestResult)
class CareerTestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'top_profile', 'created_at')
    list_filter = ('top_profile',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    autocomplete_fields = ['top_profile']

    def save_model(self, request, obj, form, change):
        # Allow admin overrides, otherwise could calc from scores
        super().save_model(request, obj, form, change)
