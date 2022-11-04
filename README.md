
# Django challenge
## Stack
 1. Django 3.2.11
 2. Python 3.6.8
 3. MySQL  14.14

## GETTING STARTED
### Create virtualenv
```
pip install virtualenv
virtualenv -p /path/to/python3.6 virtualenv
```
or
```
sudo apt install python3.6-venv
python3.6 -m venv /path/to/new/virtual/environment
virtualenv -p /path/to/python3.6 virtualenv
```
### Install requirements
```
pip install -r requirements/base.txt
```
### Create .env file
An envirnoment  variables file can be found in the project: *.env.example*. This file shows env variables for settings in order to run project. For that purpose it was used [python-decouple](https://github.com/henriquebastos/python-decouple) package.
Fill variables with your own, then, on **_spy_agency/_** folder, copy *.env.example* file
```
cp .env.example .env
```
### Database
Once you have defined database settings in _.env_ file, then you have to run django migrations.
```
python manage.py migrate
```
### User
In order to start testing the project, it's necesary to have initial users. For testing purposes,  the project have a initial users file (fixture) to load in the database.

To load users and groups data from fixtures:
```
python manage.py loaddata core/fixtures/initial_users.json
```

To load relations from fixtures:
```
python manage.py loaddata core/fixtures/lackeys_managers.json
```

These steps will load users, groups (user roles) and relations between managers and lackeys:

(Password for all users is aaron.lopez (my name))

 - giuseppi@spyagency.com (bigboss)
	 - manager1@spyagency.com (manager)
		 - hitman1@spyagency.com (hitman)
		 - hitman2@spyagency.com (hitman)
		 - hitman3@spyagency.com (hitman)
	 - manager2@spyagency.com (manager)
		 - hitman4@spyagency.com (hitman)
		 - hitman5@spyagency.com (hitman)
		 - hitman6@spyagency.com (hitman)
	 - manager3@spyagency.com (manager)
		 - hitman7@spyagency.com (hitman)
		 - hitman8@spyagency.com (hitman)
		 - hitman9@spyagency.com (hitman)

### Run project
Once you have finished previous steps you can run project on local environment.
```
python manage.py runserver
```

Have a nice day!!
