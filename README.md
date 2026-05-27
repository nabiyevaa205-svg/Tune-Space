Tune Space

## Жобаны іске қосу

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Не дайын
- 2 app: `books`, `users`
- `base.html` (header/footer)
- HTML + CSS + JS
- Adaptive layout
- Media upload (`Book.cover`)
- Template inheritance, cycle/condition
- Book list + detail
- Login/Register/Logout
- Кіру кезінде username көрінеді

## Admin
`/admin` арқылы Book қосуға болады.
