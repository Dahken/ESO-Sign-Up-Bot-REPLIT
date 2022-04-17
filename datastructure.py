import sqlite3

try:
  connection = sqlite3.connect("database.db")
  c = connection.cursor()

  SQL_STATEMENT = """CREATE TABLE signup (
    signup_id integer primary key AUTOINCREMENT,
    channel_id INTEGER,
    username VARCHAR(50),
    user_id VARCHAR(50),
    guild_id VARCHAR(50),
    channel VARCHAR(50),
    joining DATE,
    role VARCHAR(10),
    message VARCHAR (50)
  );"""
  c.execute(SQL_STATEMENT)
  connection.commit()

  SQL_STATEMENT = """CREATE TABLE default_roles (
  username VARCHAR(50),
  role VARCHAR(10)
  );"""
  c.execute(SQL_STATEMENT)
  connection.commit()

  SQL_STATEMENT = """CREATE TABLE trials (
  channel_id INTEGER,
  channel VARCHAR(50),
  owner VARCHAR(50),
  trial_time DATE,
  trial_desc VARCHAR(400),
  TANKS INTEGER DEFAULT 2,
  HEALERS INTEGER DEFAULT 2,
  DPS INTEGER DEFAULT 8
  );"""
  c.execute(SQL_STATEMENT)
  connection.commit()
  connection.close()
except connection.Error as error:
    print("Error while creating a sqlite table", error)
finally:
    if connection:
        connection.close()
        print("sqlite connection is closed")