# AfricaRelais

## Pre-requis

Python >= 3.8
Django >= 3.2

## Stack

- Python et Django pour le backend
- Bootstrap pour le frontend

## Tester le projet en local

Installer les packages

```bash
pipenv install --skip-lock
```

Modifier les configurations

```bash
cp delivery_management/local_settings.example delivery_management/local_settings.py
```

Lancer les migrations

```bash
python manage.py migrate
```

Lancer le serveur Python

```bash
python manage.py runserver
```
