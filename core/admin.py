from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin
from .models import Program, UNTSubjectComb, CareerProfile, CalendarEvent, TuitionFee, GrantBenefit, FAQ, SiteConfig, Lead

@admin.register(CareerProfile)
class CareerProfileAdmin(TabbedTranslationAdmin):
    list_display = ('code', 'title')
    search_fields = ('code', 'title')

@admin.register(UNTSubjectComb)
class UNTSubjectCombAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Program)
class ProgramAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'level', 'code', 'unt_combination', 'passing_score', 'career_profile')
    search_fields = ('title', 'code')
    list_filter = ('level', 'unt_combination', 'career_profile')
    # fieldsets = ...  Letting auto-discovery work to ensure fields are detected

@admin.register(CalendarEvent)
class CalendarEventAdmin(TranslationAdmin):
    list_display = ('title', 'date_display', 'sort_date')

@admin.register(TuitionFee)
class TuitionFeeAdmin(TranslationAdmin):
    list_display = ('level', 'study_format', 'price')

@admin.register(GrantBenefit)
class GrantBenefitAdmin(TranslationAdmin):
    list_display = ('text', 'description')
    pass

@admin.register(FAQ)
class FAQAdmin(TranslationAdmin):
    list_display = ('question', 'order')

@admin.register(SiteConfig)
class SiteConfigAdmin(TranslationAdmin):
    def has_add_permission(self, request):
        return not SiteConfig.objects.exists()

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'program', 'created_at')
    readonly_fields = ('created_at',)

