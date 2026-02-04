from django.db import models
from django.contrib.auth.models import User
from core.models import Program, CareerProfile

class ApplicantProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='applicant_profile')
    iin = models.CharField(max_length=12, unique=True, verbose_name="ИИН / ЖСН")
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество / Әкесінің аты")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения / Туған күні")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Пол / Жынысы")
    address = models.TextField(blank=True, verbose_name="Адрес проживания / Тұрғылықты мекенжайы")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.iin})"

    class Meta:
        verbose_name = "Профиль абитуриента"
        verbose_name_plural = "Профили абитуриентов"

class EducationInfo(models.Model):
    applicant = models.OneToOneField(ApplicantProfile, on_delete=models.CASCADE, related_name='education')
    school_name = models.CharField(max_length=255, verbose_name="Название учебного заведения / Оқу орнының атауы")
    graduation_year = models.IntegerField(verbose_name="Год окончания / Бітірген жылы")
    certificate_number = models.CharField(max_length=50, blank=True, verbose_name="Номер аттестата/диплома / Аттестат/диплом нөмірі")
    average_score = models.FloatField(null=True, blank=True, verbose_name="Средний балл / Орташа балл")

    class Meta:
        verbose_name = "Образование"
        verbose_name_plural = "Образование"

class CareerTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_results')
    scores = models.JSONField(verbose_name="Баллы", default=dict)
    top_profile = models.ForeignKey(CareerProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Результат (Профиль)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"

class AdmissionApplication(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Черновик / Қаралама'),
        ('SUBMITTED', 'Отправлено / Жіберілді'),
        ('UNDER_REVIEW', 'На рассмотрении / Қаралуда'),
        ('APPROVED', 'Одобрено / Мақұлданды'),
        ('REJECTED', 'Отклонено / Қабылданбады'),
    )
    
    LANGUAGE_CHOICES = (
        ('KZ', 'Қазақша'),
        ('RU', 'Русский'),
        ('EN', 'English'),
    )

    applicant = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE, related_name='applications')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name="Образовательная программа / Білім беру бағдарламасы")
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='KZ', verbose_name="Язык обучения / Оқу тілі")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT', verbose_name="Статус")
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.applicant} - {self.program}"

    class Meta:
        verbose_name = "Заявка на поступление"
        verbose_name_plural = "Заявки на поступление"

class Document(models.Model):
    TYPE_CHOICES = (
        ('ID_FRONT', 'Удостоверение личности (лиц.)'),
        ('ID_BACK', 'Удостоверение личности (обр.)'),
        ('CERTIFICATE', 'Аттестат/Диплом'),
        ('PHOTO', 'Фото 3x4'),
        ('MED_075', 'Справка 075у'),
        ('OTHER', 'Другое'),
    )

    applicant = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE, related_name='documents')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='OTHER', verbose_name="Тип документа")
    file = models.FileField(upload_to='applicant_docs/%Y/%m/', verbose_name="Файл")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant} - {self.get_type_display()}"

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
