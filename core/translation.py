from modeltranslation.translator import register, TranslationOptions
from .models import Program, CalendarEvent, TuitionFee, GrantBenefit, FAQ, SiteConfig

@register(Program)
class ProgramTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'tags', 'brochure')

@register(CalendarEvent)
class CalendarEventTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'date_display')

@register(TuitionFee)
class TuitionFeeTranslationOptions(TranslationOptions):
    fields = ('level', 'study_format', 'price') # Price might have text like "400 000 KZT"

@register(GrantBenefit)
class GrantBenefitTranslationOptions(TranslationOptions):
    fields = ('text',)

@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')

@register(SiteConfig)
class SiteConfigTranslationOptions(TranslationOptions):
    fields = ('address',)
