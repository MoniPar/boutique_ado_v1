# Overview

This is a walkthrough project which aims to build a Full-Stack site based on business logic used to control a centrally-owned dataset.  It has an authentication mechanism and provides paid access to the site's data and other activities based on the dataset like the purchase of a product.

______

# Deployment

## Setup

* Create a new GitHub repository using the Code Institute's GitPod Full Template which pre-installs all of the tools you need to get started.  If you do not have access to this, you need to pre-install Python and all requirements into your IDE.
* Click the GitPod button on the top left to create a new workspace in GitPod. If this button is not visible, make sure your GitPod extension is enabled in your browser or you can download it [here](https://www.gitpod.io/docs/configure/user-settings/browser-extension). 
* Enter the following commands in your IDE's terminal to install Django and supporting libraries.
    * `pip3 install Django==3.2 gunicorn` - installs Django 3.2 and the server [gunicorn](https://gunicorn.org/) used to run the project on Heroku. 
    * `pip3 install dj_database_url==0.5.0 	psycopg2` - installs the [postgreSQL](https://www.postgresql.org/) relational database management system along with [psycopg2](https://www.psycopg.org/docs/) an adapter for Python.
    * `pip3 freeze --local > requirements.txt` - creates the requirements.txt file and adds Django and the installed supporting libraries to it. 
* Create a new Django project and give it the name of the website. `django-admin startproject boutique_ado .` - Don't forget the (.) dot to create the project in the current directory.
* Create a basic .gitignore file `touch .gitignore` (you might already have it if using the CI's GitPod Full Template).  Then add:
    * `*.sqlite3` - to ignore the development database file.
    * `.pyc` and `__pycache__` - to ignore compiled Python code not needed in version control. 
* Run the project to make sure everything is working properly by typing `python3 manage.py runserver` and exposing port 8000.  You should get the "Install worked successfully" page below.
![Django Successful Installation Page]()
* Stop the server `ctrl + c` and run the initial migrations by typing `python3 manage.py migrate` in the terminal. 
* Create a superuser so that you can log in to the Admin panel. `python3 manage.py createsuperuser` and enter your username, email and password. The skeleton of the project is now complete. 

## First Deployment

With the skeleton of the project up and running locally, it's best to prepare it for deployment to Heroku at this early stage.

### Create the Heroku App

* Login to [Heroku](https://www.heroku.com/) and click on the top right button ‘New’ on the dashboard. 
* Click ‘Create new app’.
* Give your app a unique name and select the region closest to you. 
* Click on the ‘Create app’ button.

### Create the postgreSQL Database

Since the database provided by Django is only accessible within Gitpod, a new database suitable for production needs to be created in order for Heroku to be able to access it.  The following steps create a new postgreSQL database instance, hosted on [ElephantSQL](https://www.elephantsql.com/).

* Login to ElephantSQL and click on the top right button ‘Create New Instance’.
* Give your plan the name of the project and select the Tiny Turtle (Free) plan.  The ‘Tags’ field can be left empty.  
* Click on ‘Select Region’.  
Select a data centre near you.  Choose another region if there is none in your region yet. Click ‘Review’.   
* Make sure your plan is correct and click ‘Create Instance’. 
* Return to the dashboard and click on this project’s instance you just created. This will open up the 'Details' page where the link to the URL is displayed.  This needs to be added to the env.py file in the project’s directories as well as to the Heroku Config Vars so keep this tab open.

### Create an env.py file

With the database created, it now needs to be connected with the project.  Certain variables need to be kept private and should not be published to GitHub.  In order to keep these variables hidden, it is important to create an env.py file and add it to .gitignore.  
* Typing the following command in the terminal, will create the env.py file.
`touch env.py`
* Import os and set the DATABASE_URL variable using the `os.environ` method and add the URL copied from instance created above to it here, like so:
`os.environ[“DATABASE_URL”] = ”ElephantSQLcopiedURL”`
* The Django application requires a SECRET_KEY to encrypt session cookies.  Set this variable to any string you like or generate a secret key on this [MiniWebTool](https://miniwebtool.com/django-secret-key-generator/).
`os.environ[“SECRET_KEY”] = ”longSecretString”`

### Modify settings.py

It is important to make the Django project aware of the env.py file and to connect the workspace to the new database. 
* Open up the settings.py file and add the following code. The if statement acts as a safety net for the application in case it is run without the env.py file.
```
import os
import dj_database_url

if os.path.isfile(‘env.py’):
    import env
```
* Remove the insecure secret key provided by Django further down and reference the variable in the env.py file, like so:
```
SECRET_KEY = os.environ.get(‘SECRET_KEY’)
```
* Hook up the database using the dj_database_url import added above.  Comment out the original DATABASES variable provided by Django which connects the Django application to the created db.sqlite3 database within your repo.  This database is not suitable for production so add the following code instead:
```
DATABASES = {
    ‘default’: dj_database_url.parse(os.environ.get('DATABASE_URL'))
} 
```
Note: If you prefer to work with the db.sqlite3 one in development then use the following code to use it if the external database is not yet hooked up.
```
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```
* Save and migrate this database structure to the newly connected postgreSQL database.  Run the migrate command `python3 manage.py migrate` in your terminal.
* To make sure the application is now connected to the remote database hosted on ElephantSQL, head over to your ElephantSQL dashboard and select the newly created database instance. Select the ‘Browser’ tab on the left and click on ‘Table queries’.  This displays a dropdown field with the database structure which has been populated from the Django migrations. If you select 'auth_user' and click on the 'Execute' button on the right, you should be able to see your superuser details displayed.  This confirms your tables have been created and you can add data to your database. 

### Connect the database to Heroku

* Open up the Heroku dashboard, select the project’s app and click on the ‘Settings’ tab.
* Click on ‘Reveal Config Vars’ and add the DATABASE_URL with the value of the copied URL (without quotation marks) from the database instance created on ElephantSQL. 
* Also add the SECRET_KEY with the value of the secret key added to the env.py file. 
* If using GitPod another key needs to be added in order for the deployment to succeed.  This is PORT with the value of 8000.
* To help get the project deployed without static files you need to add one more temporary variable.  This needs to be removed before deploying the full project.  Use DISABLE_COLLECTSTATIC as the key and ‘1’ as the value.

### Set Up the Templates Directory

* In settings.py scroll down to the TEMPLATES variable to Instruct Django to store the root templates directory in the DIRS setting, like so:
```
'DIRS' = [
    os.path.join(BASE_DIR, ‘templates’),
]
```
This is were the custom allauth directory will also be set.  

### Add Heroku Host Name

* In settings.py scroll to ALLOWED_HOSTS and the Heroku host name.  This should be the Heroku app name created earlier followed by `.herokuapp.com`.  Add in `’localhost’` so that it can be run locally.
```
ALLOWED_HOSTS = [‘heroku-app-name.herokuapp.com’, ‘localhost’]
```

### Create (the directories and) the Process file

* (Create the media, static and templates directories at the top level next to the manage.py file.) 
* At the top level next to the manage.py file, create a new file called ‘Procfile’ with a capital ‘P’.  This tells Heroku how to run this project.  Add the following code, including the name of your project directory. 
```
web: gunicorn boutique_ado.wsgi:application
```
‘web’ tells Heroku that this a process that should accept HTTP traffic.
‘gunicorn’ is the server used
‘wsgi’, stands for web services gateway interface and is a standard that allows Python services to integrate with web servers

### First Deployment

Make sure everything is saved and pushed to GitHub before continuing on.
* Go back to the Heroku dashboard and click on the ‘Deploy’ tab.  
* For deployment method, select ‘GitHub’ and search for the project’s repository from the list. 
* Select and then click on ‘Deploy Branch’.  
* When the build log is complete it should say that the app has been successfully deployed. 
* Click on the ‘Open App’ button to view it and the Django “The install worked successfully!” page, should be displayed.

_____

![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome Monique Parnis,

This is the Code Institute student template for Gitpod. We have preinstalled all of the tools you need to get started. It's perfectly ok to use this template as the basis for your project submissions.

You can safely delete this README.md file, or change it for your own project. Please do read it at least once, though! It contains some important information about Gitpod and the extensions we use. Some of this information has been updated since the video content was created. The last update to this file was: **September 1, 2021**

## Gitpod Reminders

To run a frontend (HTML, CSS, Javascript only) application in Gitpod, in the terminal, type:

`python3 -m http.server`

A blue button should appear to click: _Make Public_,

Another blue button should appear to click: _Open Browser_.

To run a backend Python file, type `python3 app.py`, if your Python file is named `app.py` of course.

A blue button should appear to click: _Make Public_,

Another blue button should appear to click: _Open Browser_.

In Gitpod you have superuser security privileges by default. Therefore you do not need to use the `sudo` (superuser do) command in the bash terminal in any of the lessons.

To log into the Heroku toolbelt CLI:

1. Log in to your Heroku account and go to *Account Settings* in the menu under your avatar.
2. Scroll down to the *API Key* and click *Reveal*
3. Copy the key
4. In Gitpod, from the terminal, run `heroku_config`
5. Paste in your API key when asked

You can now use the `heroku` CLI program - try running `heroku apps` to confirm it works. This API key is unique and private to you so do not share it. If you accidentally make it public then you can create a new one with _Regenerate API Key_.

------

## Release History

We continually tweak and adjust this template to help give you the best experience. Here is the version history:

**September 1 2021:** Remove `PGHOSTADDR` environment variable.

**July 19 2021:** Remove `font_fix` script now that the terminal font issue is fixed.

**July 2 2021:** Remove extensions that are not available in Open VSX.

**June 30 2021:** Combined the P4 and P5 templates into one file, added the uptime script. See the FAQ at the end of this file.

**June 10 2021:** Added: `font_fix` script and alias to fix the Terminal font issue

**May 10 2021:** Added `heroku_config` script to allow Heroku API key to be stored as an environment variable.

**April 7 2021:** Upgraded the template for VS Code instead of Theia.

**October 21 2020:** Versions of the HTMLHint, Prettier, Bootstrap4 CDN and Auto Close extensions updated. The Python extension needs to stay the same version for now.

**October 08 2020:** Additional large Gitpod files (`core.mongo*` and `core.python*`) are now hidden in the Explorer, and have been added to the `.gitignore` by default.

**September 22 2020:** Gitpod occasionally creates large `core.Microsoft` files. These are now hidden in the Explorer. A `.gitignore` file has been created to make sure these files will not be committed, along with other common files.

**April 16 2020:** The template now automatically installs MySQL instead of relying on the Gitpod MySQL image. The message about a Python linter not being installed has been dealt with, and the set-up files are now hidden in the Gitpod file explorer.

**April 13 2020:** Added the _Prettier_ code beautifier extension instead of the code formatter built-in to Gitpod.

**February 2020:** The initialisation files now _do not_ auto-delete. They will remain in your project. You can safely ignore them. They just make sure that your workspace is configured correctly each time you open it. It will also prevent the Gitpod configuration popup from appearing.

**December 2019:** Added Eventyret's Bootstrap 4 extension. Type `!bscdn` in a HTML file to add the Bootstrap boilerplate. Check out the <a href="https://github.com/Eventyret/vscode-bcdn" target="_blank">README.md file at the official repo</a> for more options.

------

## FAQ about the uptime script

**Why have you added this script?**

It will help us to calculate how many running workspaces there are at any one time, which greatly helps us with cost and capacity planning. It will help us decide on the future direction of our cloud-based IDE strategy.

**How will this affect me?**

For everyday usage of Gitpod, it doesn’t have any effect at all. The script only captures the following data:

- An ID that is randomly generated each time the workspace is started.
- The current date and time
- The workspace status of “started” or “running”, which is sent every 5 minutes.

It is not possible for us or anyone else to trace the random ID back to an individual, and no personal data is being captured. It will not slow down the workspace or affect your work.

**So….?**

We want to tell you this so that we are being completely transparent about the data we collect and what we do with it.

**Can I opt out?**

Yes, you can. Since no personally identifiable information is being captured, we'd appreciate it if you let the script run; however if you are unhappy with the idea, simply run the following commands from the terminal window after creating the workspace, and this will remove the uptime script:

```
pkill uptime.sh
rm .vscode/uptime.sh
```

**Anything more?**

Yes! We'd strongly encourage you to look at the source code of the `uptime.sh` file so that you know what it's doing. As future software developers, it will be great practice to see how these shell scripts work.

---

Happy coding!
