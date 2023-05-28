# Delyzer

## Guidelines

- Follow the naming conventions for python projects
    - Use snake_case for files, functions and variables
    - Use PascalCase for classes
- Use single quotes (except doc-strings)
- Declare private variables with __variable
- Use self-explainatory naming for functions and variables
- Comments and doc strings have to be written in english
- Everything that will be displayed to the user has to be written in german

## Tech-stack

- Django
- djangorestframework
- Pandas
- vvspy
- pylint
- matplotlib
- tkinter

## Installation

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
python manage.py migrate              # Migrate database
```
```bash
python manage.py createsuperuser      # Create the superuser account for /admin login
```

## Collect data

```bash
python manage.py collect_data [--observe-station <station-id> OR --observe-line <line-name>] --clear <true|false>
```


## Useful commands
- tkinter is required

```bash
python frontend/app.py                # Start frontend
```
```bash
python manage.py runserver            # Run server 
```
```bash
python manage.py makemigrations       # Generate migrations after making changes on models
python manage.py migrate              # Apply changes to the database
```

