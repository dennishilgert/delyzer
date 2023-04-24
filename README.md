# Delyzer

## Guidelines

- Follow the naming conventions for python projects
    - Use snake_case for files, functions and variables
    - Use PascalCase for classes
- Use single quotes (except doc-strings)
- Comments and doc strings have to be written in english
- Everything that will be displayed to the user has to be written in german

## Tech-stack

- Django
- djangorestframework
- Pandas
- vvspy
- pylint

## Useful commands

```bash
python3 -m venv .venv                 # Create virtual python environment
```
```bash
. .venv/bin/activate                  # Unix - Activate virtual python environment
. .venv/Scripts/activate.bat          # Windows

deactivate                            # Deactivate virtual python environment
```
```bash
pip install -r requirements.txt       # Create the superuser account for /admin login
```
```bash
python manage.py createsuperuser      # Create the superuser account for /admin login
```
```bash
python manage.py runserver            # Run development server
```
```bash
python manage.py makemigrations       # Generate migrations from models
```
```bash
python manage.py migrate              # Migrate database
```
