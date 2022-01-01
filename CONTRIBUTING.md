#How To Contribute
*We love your input!*  
We want to make contributing to this project as easy and transparent as possible

##First Setup
### 1. clone the development branch on your system

run:

`git clone -b development path/to/project`

> For each change, first make a new branch and make your changes to it ex. `git switch -f -c origin/issue1`

> Do not commit any changes to the main branches like development, master,...

### 2. run docker services

run:

`docker-compose up`


### 3. set up VENV

you could create project VENV with `make venv`  command.

or create with  `pip3.9 -m venv .venv`

we have two requirements file

`requirements.txt` for development purposes. this file has a link to the `requirements-prod.txt` file

`requirements-prod.txt` for production

### 4. create local settings
before running the app you need to create a file in the `src/core/settings/local.py` path. all settings from this file will be overridden to development or production settings. `src/core/settings/local.py` is in `.gitignore` So your changes will not be pushed.

### 5. run the web app

after activating your VENV run

`cd src` and `python manage.py runserver`

##Contribution
### Fixing a bug  
Discussing the current state of the code  
Proposing new features  
Becoming a maintainer  

### We Develop with Gitlab
We use github to host code, to track issues and feature requests, as well as accept pull requests.

We Use Github Flow, So All Code Changes Happen Through PullRequests
Pull requests are the best way to propose changes to the codebase (we use Github Flow). We actively welcome your pull requests:

Pull the repo and create your branch from develop.
If you've added code that should be tested, add tests.(We use pytest)
If you've changed APIs, make sure you follow Django documentations.
Ensure the test suite passes.
Make sure your code lints.

### Issue that pull request!
We use CI/CD for deploying the project, so use the CI/CD section in gitlab for merging the branches
After making sure that your code works, merge it with dev branch
Check if everything is ok in the develop branch in staging


### Commit Conventions:  
Use this convention to commit changes:  
type: subject  
-- a blank line --  
Body  

Type:

feat: A new feature  
fix: A bug fix  
docs: Changes in documentations  
style: Style changes, formatting, missing whitespaces  
refactor: Code changes that neither fixes a bug or adds a feature  
perf: Changes that improves performance  
test: Add missing tests  
chore: Changes the build process  


Subject:  
The subject contains a short description of the applied changes

Body (optional):  
Must begin after a blank line after the subject. Can provide additional contextual information.
For breaking changes, the body must start with "BREAKING CHANGES:"

### Look for exceptions after deploying  
Always check the project in Sentry for any exceptions

Use a Consistent Coding Style  
We use **PEP 8** -- Style Guide for Python Code. So make sure you follow it as well.  
We use **black** as styling tool. So make sure you run `black .` before every commit.

### Note
Check [README.md](README.md) for more info and see how things work.
