from core.models import CareerProfile

profiles = [
    {
        "code": "A",
        "title_ru": "IT и цифровые технологии",
        "title_kk": "IT және цифрлық технологиялар"
    },
    {
        "code": "B",
        "title_ru": "Инженерно-технические и STEM направления",
        "title_kk": "Инженерлік-техникалық және STEM бағыттары"
    },
    {
        "code": "C",
        "title_ru": "Бизнес, экономика, менеджмент, маркетинг",
        "title_kk": "Бизнес, экономика, менеджмент, маркетинг"
    },
    {
        "code": "D",
        "title_ru": "Педагогика, психология, социальная работа",
        "title_kk": "Педагогика, психология, әлеуметтік жұмыс"
    },
    {
        "code": "E",
        "title_ru": "Аграрные, экологические, биологические направления",
        "title_kk": "Аграрлық, экология, биология бағыттары"
    },
    {
        "code": "F",
        "title_ru": "Гуманитарные, языковые, журналистика, переводы",
        "title_kk": "Гуманитарлық, тілдер, журналистика, аударма"
    }
]

for p in profiles:
    profile, created = CareerProfile.objects.update_or_create(
        code=p["code"],
        defaults={
            "title_ru": p["title_ru"],
            "title_kk": p["title_kk"]
        }
    )
    print(f"Processed: {profile.code}")
