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
