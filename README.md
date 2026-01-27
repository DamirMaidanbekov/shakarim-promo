# Shakarim Admission Portal 2026

Одностраничный промо-сайт для приемной кампании Shakarim University.
Стек: Django 5, TailwindCSS, Alpine.js, SQLite.

## Функционал
- Мультиязычность (RU/KZ)
- Каталог образовательных программ с поиском
- Просмотр и скачивание буклетов (PDF)
- Календарь событий абитуриента
- Форма онлайн-консультации (сбор лидов в БД)
- Админ-панель для управления контентом

## Установка и запуск

1. **Клонировать репозиторий**
   ```bash
   git clone https://github.com/your-repo/shakarim-promo.git
   cd shakarim-promo
   ```

2. **Создать и активировать виртуальное окружение**
   Windows:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
   Mac/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Установить зависимости**
   ```bash
   pip install -r requirements.txt
   ```

4. **Применить миграции**
   ```bash
   python manage.py migrate
   ```

5. **Создать суперпользователя (для админки)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Запустить сервер**
   ```bash
   python manage.py runserver
   ```

## Администрирование
Админка доступна по адресу: `http://127.0.0.1:8000/admin/`

**Что нужно заполнить:**
1. **Programs**: Добавить образовательные программы и загрузить PDF буклеты.
2. **Calendar Events**: Добавить важные даты (ЕНТ, Гранты).
3. **Tuition Fees**: Установить цены.
4. **Grant Benefits**: Добавить пункты о преимуществах/грантах.
5. **FAQs**: Заполнить частые вопросы.
6. **Site Config**: Указать телефон, email, ссылки на WhatsApp/Telegram и тест профориентации.

## Деплой
Для запуска на внешнем IP (например, 95.58.221.165):
```bash
python manage.py runserver 0.0.0.0:8000
```
Убедитесь, что в `settings.py` `ALLOWED_HOSTS = ['*']` и порт 8000 открыт в брандмауэре.
