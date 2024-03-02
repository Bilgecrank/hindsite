# hindsite
[![Pylint](https://github.com/Bilgecrank/hindsite/actions/workflows/pylint.yml/badge.svg?branch=development)](https://github.com/Bilgecrank/hindsite/actions/workflows/pylint.yml)

A SCRUM retrospective tool to empower teams.

## Currently in Progress as a School Capstone
![UMGC Logo](https://www.umgc.edu/content/experience-fragments/umgc/language-masters/en/header/master/_jcr_content/root/header_copy/image.coreimg.svg/1705606255029/umgc-logo-preferred-rgb.svg)
Hello! This project is currently a capstone project for a CMSC 495 course at the University of Maryland Global Campus. We are not accepting pull-requests outside our collaborative group so far, but after the assignment is submitted and graded, we can accept open-source collaboration after the fact.

## To run the project locally, you'll need to complete a few steps:

1. First, you need to set up a MySQL Database:
   -https://dev.mysql.com/doc/mysql-getting-started/en/

2. Next, you need to run `pip install -r requirements.txt` in the root directory of the project.

   -Note: this project was created with the latest version of Python 3. There are no version locks in the requirements.txt yet.
   -Reccomendation: Use a virtual environment to install the requirements, rather than your operating system.
   
3. Finally, you need a .env file in the root directory of the project folder with the following environment variables:
  
    `MYSQLUSER = ""
    
    MYSQL_ROOT_PASSWORD = ""
    
    MYSQL_HOST = ""
    
    MYSQL_PORT = ""
    
    MYSQL_DATABASE = ""
    
    SECRET_KEY = ""`

4. Finally, to run the server, the following command is run from the root directory of the app in the terminal:

  `gunicorn --timeout 600 --chdir app wsgi:app`
  
  If you want the app to reload the server whenever you save, I recommend you use the flag --reload at the end, so:
  
  `gunicorn --timeout 600 --chdir app wsgi:app --reload`

## Some tips:

Information for your local environment will go inside the double quotes. For example, the default port for MySQL is 3306, so:
  
    `MYSQL_PORT = "3306"`
  
  **MYSQL_HOST** is the hostname, so locally it will be localhost, or 127.0.0.1
  
  **MYSQL_DATABASE** is the name of the database that you'll have to create in your local MySQL server. The user is the user that has root permission to the database, which is why the root password is named as such.
  
  The codebase is set up to be portable between local environments and the railway server without publishing any secrets to GitHub, but python will automatically load from the .env file by first loading dotenv.
  
  **SECRET_KEY** is optional. If you look in config.py you'll see that it's randomly generated, but you can comment out the one that uses secrets.token_hex() to generate a random key every reboot and uncomment the line that uses the environment variable if you want sessions to persist through reloads.
  
  For the database, an empty MySQL database with the name that's in the environment variable will be populated when you run the command. You just have to make sure that you populate the .env files with the connection information to your MySQL server.
