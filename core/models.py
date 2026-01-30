from django.db import models

class Program(models.Model):
    LEVEL_CHOICES = (
        ('BACHELOR', 'Bachelor'),
        ('MASTER', 'Master'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='BACHELOR')
    tags = models.CharField(max_length=255, blank=True, help_text="e.g. 'UNT: Math+Physics'")
    brochure = models.FileField(upload_to='brochures/', blank=True, null=True)

    # Brochure Fields
    code = models.CharField(max_length=50, blank=True, verbose_name="Код ОП")
    main_info = models.TextField(blank=True, verbose_name="Негізгі ақпарат / Основная информация")
    unt_subjects = models.CharField(max_length=255, blank=True, verbose_name="ҰБТ бейіндік пәндері / Профильные предметы ЕНТ")
    
    # Languages
    lang_kaz = models.BooleanField(default=False, verbose_name="Оқыту тілі: Қазақ")
    lang_rus = models.BooleanField(default=False, verbose_name="Оқыту тілі: Русский")
    lang_eng = models.BooleanField(default=False, verbose_name="Оқыту тілі: English")

    usp = models.TextField(blank=True, verbose_name="Уникалды сауда ұсынысы / УТП")
    slogan = models.CharField(max_length=500, blank=True, verbose_name="Слоган")
    
    advantage_1 = models.TextField(blank=True, verbose_name="Артықшылығы 1 / Преимущество 1")
    advantage_2 = models.TextField(blank=True, verbose_name="Артықшылығы 2 / Преимущество 2")
    advantage_3 = models.TextField(blank=True, verbose_name="Артықшылығы 3 / Преимущество 3")

    target_audience = models.TextField(blank=True, verbose_name="Бұл бағдарлама кімге арналған? / Для кого эта программа?")
    career_track = models.TextField(blank=True, verbose_name="Мансап жолы / Карьерный трек")

    profession_1 = models.CharField(max_length=255, blank=True, verbose_name="Лауазым 1 / Профессия 1")
    profession_2 = models.CharField(max_length=255, blank=True, verbose_name="Лауазым 2 / Профессия 2")
    profession_3 = models.CharField(max_length=255, blank=True, verbose_name="Лауазым 3 / Профессия 3")
    profession_4 = models.CharField(max_length=255, blank=True, verbose_name="Лауазым 4 / Профессия 4")
    profession_5 = models.CharField(max_length=255, blank=True, verbose_name="Лауазым 5 / Профессия 5")

    partners = models.TextField(blank=True, verbose_name="Практика өтетін ұйымдар / Компании партнеры", help_text="Список")
    salary_start = models.CharField(max_length=255, blank=True, verbose_name="Орташа бастапқы жалақы / Средняя зарплата на старте")
    
    what_will_learn = models.TextField(blank=True, verbose_name="Не үйретеміз? / Чему научим?")
    hard_skills = models.TextField(blank=True, verbose_name="Hard Skills")
    soft_skills = models.TextField(blank=True, verbose_name="Soft Skills")
    
    interesting_subjects = models.TextField(blank=True, verbose_name="Қызықты пәндер / Интересные дисциплины", help_text="Список")
    social_proof = models.TextField(blank=True, verbose_name="Әлеуметтік дәлел / Социальное доказательство")
    
    star_graduates = models.TextField(blank=True, verbose_name="Табысты түлектер / Звездные выпускники", help_text="Список")
    star_teachers = models.TextField(blank=True, verbose_name="Белгілі оқытушылар / Звездные преподаватели", help_text="Список")
    
    media_links = models.TextField(blank=True, verbose_name="Медиа-контент (Instagram Links)", help_text="Гиперссылки на инстаграмм")
    photo_video_links = models.TextField(blank=True, verbose_name="Фото/видео сілтеме", help_text="Гиперссылки на инстаграмм")

    def __str__(self):
        return f"{self.title} ({self.level})"

class CalendarEvent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_display = models.CharField(max_length=100, help_text="Text representation of date, e.g. '20-25 Jan'")
    sort_date = models.DateField(help_text="For sorting purposes", blank=True, null=True)
    event_type = models.CharField(max_length=50, blank=True, help_text="INTERVIEW/DEADLINE/OPENDAY")

    class Meta:
        ordering = ['sort_date']

    def __str__(self):
        return self.title

class TuitionFee(models.Model):
    level = models.CharField(max_length=100, help_text="Bachelor/Master")
    study_format = models.CharField(max_length=100, help_text="Full-time/Part-time")
    price = models.CharField(max_length=100, help_text="Price per year")

    def __str__(self):
        return f"{self.level} - {self.study_format}"

class GrantBenefit(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question

class SiteConfig(models.Model):
    # Contacts
    phone = models.CharField(max_length=50, default="+7 (777) 777-77-77")
    email = models.EmailField(default="info@shakarim.edu.kz")
    address = models.CharField(max_length=255, default="Semey, ...")
    whatsapp_link = models.URLField(blank=True)
    telegram_link = models.URLField(blank=True)
    
    # Career Test
    career_test_link = models.URLField(blank=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return "Site Configuration"

class Lead(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    level = models.CharField(max_length=50, blank=True)
    program = models.CharField(max_length=255, blank=True) # Text storage to avoid complex FK issues if programs change
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"
