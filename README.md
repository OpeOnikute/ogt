# OGT README #

OGT stands for Ope's Graphic Tool (Kent blame me)

This is a dashboard application, ~~i'm~~ I was building to manage my graphic design work. 

It currently runs on Django 1.9 and Python 2.7.

The goal ~~is~~ was to be able to do all the administrative stuff from the dashboard. i.e. Talk to clients, generate invoices, send emails etc.

It's ~~not~~ open source now, so it can be used as a reference for building a dashboard with Django.

## How to use
- Clone the repository to your system using the `git clone` command.
- Go into the folder/directory named `ogt` and setup your virtual environment using instructions from [here](https://docs.python-guide.org/dev/virtualenvs/) or using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) (highly recommended).
- In that environment, run pip install. This would install all the packages specified in the `requirements.text` file.

## Environment variables
In your virtualenv, create an environment variable OGT_EMAIL_PASSWORD. If you're using virtualenvwrapper, you can use instructions from [this question](https://stackoverflow.com/questions/9554087/setting-an-environment-variable-in-virtualenv).

