# udemy-python-postgres
1. [The Complete Python/PostgreSQL Course 2.](https://www.https://www.udemy.com/course/complete-python-postgresql-database-course/)
Ebook [here](https://pysql.tecladocode.com/)
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


# Window functions examples
1. RANK
```
SELECT
  polls.title,
  COUNT(options.id),
  RANK() OVER(ORDER BY COUNT(options.id) DESC)
FROM polls
LEFT JOIN options
ON polls.id = options.poll_id
LEFT JOIN votes
ON options.id = votes.option_id
GROUP BY polls.title;
```
2. PARTITION BY
```
SELECT
	polls.title,
	options.option_text,
	COUNT(votes) AS vote_count,
	DENSE_RANK() OVER(PARTITION BY polls.title ORDER BY COUNT(votes) DESC)
FROM polls
LEFT JOIN options ON polls.id = options.poll_id
LEFT JOIN votes ON votes.option_id = options.id
GROUP BY polls.title, options.option_text
```
3. Distinct ON requires ORDER BY for consistency
```
SELECT
	DISTINCT ON (options.poll_id) poll_id,
	options.option_text,
	COUNT(options.option_text) AS option_count
FROM options
LEFT JOIN votes ON votes.option_id = options.id
GROUP BY options.poll_id, options.option_text
ORDER BY options.poll_id, option_count DESC
```
4. DISTINCT
```
SELECT DISTINCT name, country FROM cities; -- DISTINCT tuple (name, country)
```
5. HAVING - Filtering after aggregation, needs to be before (ORDER BY).
Have to use the full function, no performance lost.
```
SELECT
	DISTINCT ON (options.poll_id) poll_id,
	options.option_text,
	COUNT(options.option_text) AS option_count
FROM options
LEFT JOIN votes ON votes.option_id = options.id
GROUP BY options.poll_id, options.option_text
HAVING COUNT(options.option_text) > 2
ORDER BY options.poll_id, option_count DESC
```
6. Views
```
CREATE VIEW most_voted_options AS
    SELECT
        DISTINCT ON (options.poll_id) poll_id,
        options.option_text,
        COUNT(options.option_text) AS option_count
    FROM options
    LEFT JOIN votes ON votes.option_id = options.id
    GROUP BY options.poll_id, options.option_text
    ORDER BY options.poll_id, option_count DESC;

SELECT * FROM most_voted_options;
```
```
CREATE VIEW high_earners AS
    SELECT * FROM employees WHERE salary > 80000
    WITH LOCAL CHECK OPTION; -- Cannot INSERT Invalid data with the where clause

    WITH CASCADED CHECK OPTION; -- Also check against the FROM table
```
```
CREATE MATERIALZIED VIEW name AS ...
REFRESH MATERIALIZED VIEW name;
```

# Dates
1. Adding dates
```
today = datetime.datetime.now()
one_week = datetime.timedelta(days=7)

print(today + one_week)
```
2. UTC date
```
today = datetime.datetime.now(datetime.timezone.utc)
utc_local_time = datetime.datetime.now(tz=pytz.utc)
```
```
import datetime
import pytz

singapore = pytz.timezone('Asia/Singapore')
eastern = pytz.timezone('US/Eastern')

local_time = datetime.datetime.now()
singapore_time = singapore.localize(local_time)
eastern_time = singapore_time.astimezone(eastern)
```
Asking user for date:
```
import datetime
import pytz

eastern = pytz.timezone('US/Eastern')

user_date = eastern.localize(datetime.datetime.now(2020, 4, 15, 6, 0, 0))
utc_date = user_date.astimezone(pytz.utc)
```

# Composite primary keys
1. Create table
```
CREATE TABLE customer_details (
    account_number INTEGER,
    sort_code INTEGER,
    PRIMARY KEY (account_number, sort_code)
);

CREATE TABLE customer_details (
    account_number INTEGER,
    sort_code INTEGER,
    FOREIGN KEY (account_number, sort_code) REFERENCES accounts
    -- or
    FOREIGN KEY (account_number, sort_code) REFERENCES accounts (account_number, sort_code)
);
```

# Postgres user defined functions
1. Create function
```
CREATE FUNCTION delete_inactive(seconds NUMERIC) RETURNS void AS $$
    DELETE FROM users WHERE last_opened > seconds;
$$ LANGUAGE SQL; 

SELECT delete_inactive(5000); -- Runs the function

DROP FUNCTION delete_inactive(NUMERIC) -- Need variable type as we can have overloaded functions

CREATE OR REPLACE FUNCTION delete_inactive(seconds NUMERIC) RETURNS NIGINT AS $$
    WITH deleted AS (DELETE FROM users WHERE last_opened > seconds RETURNING *);
    SELECT COUNT(*) FROM deleted;
$$ LANGUAGE SQL;

SELECT delete_inactive(86400)
```
2. Composite types and sets in functions
```
CREATE OR REPLACE FUNCTION opened_ago(email_open_row email_opens) RETURNS INTEGER AS $$
    SELECT cast(extract(epoch FROM CURRENT_TIMESTAMP) AS INTEGER) - email_open_row.opened_time AS email_opened_ago;
$$ LANGUAGE SQL;

SELECT *, opened_ago(email_opens) FROM email_opens;

SELECT * FROM users
JOIN email_opens ON users.id = email_opens.user_id
WHERE opened_ago(email_opens) < 17509903;
```
3. Stored procedures - Functions as transactions
```
CREATE PROCEDURE insert_test_data() AS $$
BEGIN
    DROP TABLE IF EXISTS test_data;
    CREATE TABLE test_data (id INTEGER, name TEXT);
    INSERT INTO test_data VALUES (1, 'Rob');
    INSERT INTO test_data VALUES (2, 'Rolf');
    COMMIT;
END;
$$ LANGUAGE plpgsql; -- Need this language to prevent test_data not defined

CALL insert_test_data(); -- Cannot call 2 procedures in the same transaction
```

4. Locking
- Table level locking
- Row level locking
- Advisory locking

5. AIOPG - Async psycopg2

6. SQL string composition
```
from psycopg2 import sql

query = sql.SQL("SELECT * FROM {table} WHERE {column} = %s;")
query = query.format(
    table=sql.Identifier(table_name),
    column=sql.Identifier(column_name)
)
```
```
fields = fields_csv.strip().split(",")
sql_fields = [sql.Identifier(field) for field in fields]

query = sql.SQL("SELECT {fields} FROM users;")
query = query.format(
    fields=sql.SQL(",").join(sql_fields)
)
```