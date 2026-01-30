from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin
from .models import Program, CalendarEvent, TuitionFee, GrantBenefit, FAQ, SiteConfig, Lead

@admin.register(Program)
class ProgramAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'level', 'code')
    search_fields = ('title', 'code')
    list_filter = ('level',)
    # fieldsets = ...  Letting auto-discovery work to ensure fields are detected

@admin.register(CalendarEvent)
class CalendarEventAdmin(TranslationAdmin):
    list_display = ('title', 'date_display', 'sort_date')

@admin.register(TuitionFee)
class TuitionFeeAdmin(TranslationAdmin):
    list_display = ('level', 'study_format', 'price')

@admin.register(GrantBenefit)
class GrantBenefitAdmin(TranslationAdmin):
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

