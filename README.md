# udemy-python-postgres
1. [The Complete Python/PostgreSQL Course 2.](https://www.https://www.udemy.com/course/complete-python-postgresql-database-course/)
2. Used with Pylance extension to practice typed annotations with Python as well.
3. Install pipenv: `py -m pip install pipenv`
4. Create new pipenv project: `py -m pipenv --python 3.9`, temporary disable uwsgi and psycopg2 first
5. Update .vscode settings with virtualenv location
```
"python.analysis.extraPaths": [
    "C:\\Users\\Kaiser\\.virtualenvs\\udemy-python-postgres-vwQ2Z9lm\\Lib\\site-packages",
],
```
6. Install dependencies: `py -m pipenv install --dev`
7. Run pipenv: `py -m pipenv shell`
8. Check pipenv dependencies: `py -m pipenv graph`
9. Exit pipenv: `exit`
10. Run black formatting: `black .`


# sqlitebrowser
1. Download from [sqlitebrowser](https://sqlitebrowser.org/dl)

# PostgresSQL
1. [ElephantSQL](elephantsql.com)
2. Install locally (https://pysql.tecladocode.com/section05/lectures/02_how_to_install_postgresql/)
[Install Postgres](https://www.postgresqltutorial.com/install-postgresql/)
[Install HeidiSQL](https://www.heidisql.com/download.php)
- Make sure to create database and select the correct one in the startup.
- Connect using postgres://postgres:1234@localhost:5432/db_name
3. psycopg2 vs psycopg2-binary. psycopg2 need to be built. psycopg2-binary should just work but some specialized things might run into trouble.