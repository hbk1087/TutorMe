# TutorMe - Group A23

Group Members

Grant Sweeney - gcx8yv,
Harshita Tirumalapudi - ht3vd,
Janai Malone - jmm9ew


__Name:__ Grant Sweeney

__Computing ID:__ GCX8YV

__Installions:__ 
    Install Python, Pip3
    Install Django through virtual environment
        python3 -m venv env
        source env/bin/activate
    Install dependecies/libraries from requirements.txt
        pip install -r requirements.txt

To Create Django Folder
    Inside parent directory
    django-admin startproject mysite django-**********
    django-admin startproject CS3240 django-grantsweeney02
    Replace ***** with GH username
    Replace mysite with the name of the parent directory

To Run Server
    python3 manage.py runserver

To Create Directories
    python3 manage.py startapp name
        replace name with name of app

Create the tables for INSTALLED_APPS
    python3 manage.py migrate

Create the table mockUp for our models
    python3 manage.py makemigrations polls

Migrate into SQL TABLE - Prints table mock up
    python3 manage.py sqlmigrate polls 0001
        --run migration again to create the tables for new models--

To invoke python shell
    python3 manage.py shell

Creating an admin user
    python3 manage.py createsuperuser
    Enter username, email, password

Running test cases in tests.py
    python3 manage.py test polls


