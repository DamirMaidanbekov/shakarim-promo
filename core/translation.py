from modeltranslation.translator import register, TranslationOptions
from .models import Program, UNTSubjectComb, CareerProfile, CalendarEvent, TuitionFee, GrantBenefit, FAQ, SiteConfig

@register(CareerProfile)
class CareerProfileTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Program)
class ProgramTranslationOptions(TranslationOptions):
    fields = (
        'title', 'description', 'tags', 'brochure',
        'main_info', 'unt_subjects', 'usp', 'slogan',
        'advantage_1', 'advantage_2', 'advantage_3',
        'target_audience', 'career_track',
        'profession_1', 'profession_2', 'profession_3', 'profession_4', 'profession_5',
        'partners', 'salary_start', 'what_will_learn',
        'hard_skills', 'soft_skills', 'interesting_subjects',
        'social_proof', 'star_graduates', 'star_teachers'
    )

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
