import logging
import psycopg
import config


def question_time(time, tg_id):
    """"""
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                postgres_insert_query = f""" UPDATE PROFILE SET
                  QUESTION_TIME_TIME = '{time}' WHERE TG_ID = {tg_id};"""
                cur.execute(postgres_insert_query)
                conn.commit()
                return "Данные записаны"
            except ConnectionError:
                logging.warning("Save data to  error")
            finally:
                conn.close()


def answer_regular(regular, tg_id):
    """"""
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                postgres_insert_query = f""" UPDATE PROFILE SET
                  ANSWER_TIME_SCHEDULE = '{regular}' WHERE TG_ID = {tg_id};"""
                cur.execute(postgres_insert_query)
                conn.commit()
                return "Данные записаны"
            except ConnectionError:
                logging.warning("Save data to  error")
            finally:
                conn.close()


def answer_day(day, tg_id):
    """"""
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                postgres_insert_query = f""" UPDATE PROFILE SET
                  ANSWER_TIME_DAY = '{day}' WHERE TG_ID = {tg_id};"""
                cur.execute(postgres_insert_query)
                conn.commit()
                return "Данные записаны"
            except ConnectionError:
                logging.warning("Save data to  error")
            finally:
                conn.close()


def get_question_time(tg_id):
    postgresql_select_query = f"select QUESTION_TIME_TIME from PROFILE where tg_id={tg_id}"
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(postgresql_select_query)
                data = cur.fetchone()
                return data[0]
            except:  # pylint: disable=W0702
                logging.warning("Sum all data error")
            finally:
                conn.close()


def get_answer_day(tg_id):
    postgresql_select_query = f"select ANSWER_TIME_DAY from PROFILE where tg_id={tg_id}"
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(postgresql_select_query)
                data = cur.fetchone()
                return data[0]
            except:  # pylint: disable=W0702
                logging.warning("Sum all data error")
            finally:
                conn.close()


def get_answer_regular(tg_id):
    postgresql_select_query = f"select ANSWER_TIME_SCHEDULE from PROFILE where tg_id={tg_id}"
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(postgresql_select_query)
                data = cur.fetchone()
                return data[0]
            except:  # pylint: disable=W0702
                logging.warning("Sum all data error")
            finally:
                conn.close()
