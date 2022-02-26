# pylint: disable=C0114
import logging
import psycopg
# from psycopg import errors
import config
from datetime import datetime


def save_data(user_id, quantity, category, annotation, vector, date):
    """Save data to table expenditure"""
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                postgres_insert_query = """ INSERT INTO EXPENDITURE (TG_ID, AMOUNT, CATEGORY,
                ANNOTATION, STATUS, DATE) VALUES (%s, %s, %s, %s, %s, %s) """
                record_to_insert = (user_id, quantity, category, annotation, vector, date)
                cur.execute(postgres_insert_query, record_to_insert)
                conn.commit()
                return "Данные записаны"
            except:  # pylint: disable=W0702
                logging.warning("Save data error")
            finally:
                conn.close()


def sum_all_data(user_id):
    """SUM ALL data and save to wallet"""
    tg_id = user_id['id']
    postgresql_select_query = f"select * from EXPENDITURE where tg_id={tg_id} "
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                all = 0
                cur.execute(postgresql_select_query)
                wallet_records = cur.fetchall()
                for row in wallet_records:
                    wallet_content = row[2]
                    if row[6].month != datetime.today().month:
                        pass
                    else:
                        if row[5]:
                            all += wallet_content
                        else:
                            all -= wallet_content
                return all
            except:  # pylint: disable=W0702
                logging.warning("Sum all data error")
            finally:
                conn.close()
