# Scaner_Python with KALI LINUX

Створюємо віртуальне середовище 
$python -m venv venv_scan
заходимо до  віртуального середовища
$source venv_scan/bin/activat


завантажуємо всі потрібні пакети
$pip freeze > requirements.txt

Створити базу данних
___
$sudo python
>from blog import create_app
>app = create_app()
>from blog.models import db, Address, Svmap, Nmap, LogScan
>app.app_context().push()
>db.create_all()
>exit()
__

Запускаємо САЙТ 
$sudo python flsite.py  


Завершити роботу сайту 
CTRL+C
$deactivate
