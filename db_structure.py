# pylint: disable=C0114
import logging
import psycopg
import config


with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
    with conn.cursor() as cur:
        try:
            cur.execute('''CREATE TABLE PROFILE
                 (ID SERIAL PRIMARY KEY,
                 TG_ID INT NOT NULL,
                 IS_ADMIN BOOLEAN NOT NULL,
                 IS_BOT BOOLEAN NOT NULL,
                 USERNAME TEXT NOT NULL,
                 WALLET TEXT NOT NULL,
                 FIRST_NAME TEXT NOT NULL,
                 CONTACT BOOLEAN NOT NULL,
                 PHONE_NUMBER TEXT NOT NULL,
                 REGISTER_DATE TIMESTAMP NOT NULL,
                 LANG TEXT NOT NULL,
                 QUESTION_TIME_TIME TEXT NOT NULL,
                 ANSWER_TIME_DAY TEXT NOT NULL,
                 ANSWER_TIME_SCHEDULE TEXT NOT NULL,
                 ACTIVITY_DATE TIMESTAMP NOT NULL,
                 ACTIVITY BOOLEAN NOT NULL);''')
        except psycopg.errors.DuplicateTable:
            logging.warning("Table Profile exist")
        else:
            conn.commit()
        finally:
            conn.close()

with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
    with conn.cursor() as cur:
        try:
            cur.execute('''CREATE TABLE WALLET
                 (ID SERIAL PRIMARY KEY,
                 TG_ID INT NOT NULL,
                 WALLET TEXT NOT NULL,
                 WALLET_CONTENT FLOAT NOT NULL,
                 DATE TIMESTAMP NOT NULL);''')
        except psycopg.errors.DuplicateTable:
            logging.warning("Table Wallet exist")
        else:
            conn.commit()
        finally:
            conn.close()


with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
    with conn.cursor() as cur:
        try:
            cur.execute('''CREATE TABLE EXPENDITURE
                 (ID SERIAL PRIMARY KEY,
                 TG_ID INT NOT NULL,
                 AMOUNT FLOAT NOT NULL,
                 CATEGORY TEXT NOT NULL,
                 ANNOTATION TEXT NOT NULL,
                 STATUS BOOLEAN NOT NULL,
                 DATE TIMESTAMP NOT NULL);''')
        except psycopg.errors.DuplicateTable:
            logging.warning("Table EXPENDITURE exist")
        else:
            conn.commit()
        finally:
            conn.close()
