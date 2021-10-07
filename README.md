 # Platform for online learning
This will be the platform for online learning with its own content management system (Content
Management System, CMS)

## Current features

* Creation of fixtures for models
* Model inheritance
* Implementation of your own model field
* Using class handlers and mixins
* Working with sets of forms
* Controlling access to site content using groups and permissions
* CMS creation
* Creation of handlers for showing course content to students
* Adding a user registration system
* Management of student participation in courses
* Formation of the type of course content depending on the type
* Creation of RESTful API
* Authentication and restricting access to API handlers
* Creation of sets of handlers and routers

# Instructions

1. ## Installations

Make sure to have python version 3 install on you pc or laptop.
<br>
**Clone repository**
<br>
`https://github.com/OleksiiMartseniuk/Education.git`

2. ## Installing dependencies

It will install all required dependies in the project.
<br>
`pip install -r requirements.txt`

2. ## Migrations

To run migrations.
<br>
`python manage.py migrate`

3. ## Create superuser
   
To create super user run.
<br>
`python manage.py createsuperuser`
<br>
After running this command it will ask for username, password. You can access admin panel from
<br>
`localhost:8000/admin/`

4. ## Running locally

To run at localhost. It will run on port 8000 by default.
<br>
`python manage.py runserver`
