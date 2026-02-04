from django.core.management.base import BaseCommand
from core.models import CareerProfile, Program
from django.utils.translation import activate

class Command(BaseCommand):
    help = 'Update Career Profiles and Tag Programs'

    def handle(self, *args, **options):
        # 1. Update Career Profiles
        profiles_data = [
            {
                'code': 'A',
                'title_ru': 'IT и цифровые технологии',
                'title_kk': 'IT және цифрлық технологиялар',  # Assuming modeltranslation adds title_kk
                'description_ru': 'Программирование, кибербезопасность, работа с данными, искусственный интеллект.',
                'description_kk': 'Бағдарламалау, киберқауіпсіздік, деректермен жұмыс, жасанды интеллект.',
            },
            {
                'code': 'B',
                'title_ru': 'Инженерно-технические и STEM',
                'title_kk': 'Инженерлік-техникалық және STEM',
                'description_ru': 'Инженерия, энергетика, строительство, технологии производства.',
                'description_kk': 'Инженерия, энергетика, құрылыс, өндіріс технологиялары.',
            },
            {
                'code': 'C',
                'title_ru': 'Бизнес, экономика, менеджмент',
                'title_kk': 'Бизнес, экономика, менеджмент',
                'description_ru': 'Управление, финансы, маркетинг, предпринимательство.',
                'description_kk': 'Басқару, қаржы, маркетинг, кәсіпкерлік.',
            },
            {
                'code': 'D',
                'title_ru': 'Педагогика, психология, социальная работа',
                'title_kk': 'Педагогика, психология, әлеуметтік жұмыс',
                'description_ru': 'Обучение, воспитание, психологическая помощь, социальная поддержка.',
                'description_kk': 'Оқыту, тәрбиелеу, психологиялық көмек, әлеуметтік қолдау.',
            },
            {
                'code': 'E',
                'title_ru': 'Аграрные, экология, биология',
                'title_kk': 'Аграрлық, экология, биология',
                'description_ru': 'Сельское хозяйство, ветеринария, экология, биотехнологии.',
                'description_kk': 'Ауыл шаруашылығы, ветеринария, экология, биотехнология.',
            },
            {
                'code': 'F',
                'title_ru': 'Гуманитарные науки, языки, журналистика',
                'title_kk': 'Гуманитарлық ғылымдар, тілдер, журналистика',
                'description_ru': 'Филология, история, международные отношения, медиа.',
                'description_kk': 'Филология, тарих, халықаралық қатынастар, медиа.',
            }
        ]

        activate('ru') # Set default context for creation if needed, though we set specific fields
        
        for p_data in profiles_data:
            # We use update_or_create. 
            # Note: django-modeltranslation registers fields like title_ru, title_kk on the model dynamically
            # We assume title_kk exists if 'kk' is in LANGUAGES settings.
            
            defaults = {
                'title': p_data['title_ru'], # Default/Fallback
                'description': p_data['description_ru'],
                'title_ru': p_data['title_ru'],
                'description_ru': p_data['description_ru'],
            }
            # Check if title_kk exists (it should via modeltranslation)
            # We pass it in defaults.
            defaults['title_kk'] = p_data['title_kk']
            defaults['description_kk'] = p_data['description_kk']

            profile, created = CareerProfile.objects.update_or_create(
                code=p_data['code'],
                defaults=defaults
            )
            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} Profile {profile.code}"))

        # 2. Tag Programs (Heuristic)
        # Reset current links? Maybe not, just fill empty ones.
        programs = Program.objects.filter(career_profile__isnull=True)
        keywords = {
            'A': ['IT', 'Информа', 'Вычисли', 'Software', 'Computer', 'Cyber', 'Матема'], 
            'B': ['Инженер', 'Техн', 'Физик', 'Строит', 'Механ', 'Электр', 'Тепло', 'Транспорт'],
            'C': ['Эконом', 'Финан', 'Учет', 'Менедж', 'Маркет', 'Бизнес', 'Гос', 'Туризм'],
            'D': ['Педагог', 'Психолог', 'Учитель', 'Музык', 'Физкульт', 'Начальн'],
            'E': ['Агро', 'Ветер', 'Биолог', 'Эколог', 'Лес', 'Почв', 'Зоо'],
            'F': ['Филолог', 'Язык', 'Истор', 'Журналист', 'Перевод', 'Право', 'Юрис'],
        }

        for prog in programs:
            title = prog.title.lower()
            assigned = False
            for code, tags in keywords.items():
                if any(tag.lower() in title for tag in tags):
                    profile = CareerProfile.objects.get(code=code)
                    prog.career_profile = profile
                    prog.save()
                    self.stdout.write(f"Assigned {prog.title} -> {code}")
                    assigned = True
                    break
            
            if not assigned:
                self.stdout.write(self.style.WARNING(f"Could not classify: {prog.title}"))

