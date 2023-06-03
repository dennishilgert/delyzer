# Delyzer
Statistical aevaluation of delays in the Vvs network.
Delyzer is an application to observe the line you need so that you can set your alarm as late as possible.
Late (high risk) is counted as a delay > 3 minutes.
## Contributors
- Matthias Schneider  -   {{MatrikelNummerHier}}
    - Data retrieval
    - graphic representation
- Samuel Matzeit      -   {{MatrikelNummerHier}}
    - Data preparation
    - REST-Backend
- Dennis Hilgert      -   {{MatrikelNummerHier}}
    - Django setup
    - Data Collection

## Setup
### Installation

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

### Collect data

```bash
python manage.py collect_data [--observe-station <station-id> OR --observe-line <line-name>] [--clear True]

# Please note that you have to lookup the station id of the target station with the following command first or observe a line
python manage.py find_station_id --station-name Stadtmitte
# If you want to observe a station and collect the departure data of e.g. Stadtmitte, then use
python manage.py collect_data --observe-station 5006056
# If you want to observe all stations of a line and collect the departure data of e.g. S1, then use
python manage.py collect_data --observe-line S1
# If you want to clear your database before collecting new data, then add the argument --clear True to your command
```

### Start Backend
```bash
. .venv/bin/activate                  # Unix - Activate virtual python 
```
```bash
python manage.py runserver            # Start the Server
```

### Start Frontend
- tkinter is required

```bash
python frontend/app.py                # Start frontend
```

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

