# pylint: disable=C0114
import logging
import psycopg
import config
from db_expenditure import sum_all_data


def create_user_wallet(user_id, wallet, date):
    """Function will create user wallet"""
    tg_id = user_id['id']
    postgres_insert_query = """ INSERT INTO WALLET (TG_ID, WALLET, WALLET_CONTENT, DATE)
    VALUES (%s,%s,%s,%s) """
    record_to_insert = (tg_id, wallet, 0, date)
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(postgres_insert_query, record_to_insert)
                conn.commit()
                return f"Кошелек {wallet} создан"
            except ConnectionError:
                logging.warning("create user wallet error")
            finally:
                conn.close()


def show_wallet_info(user_id):
    """Function will show user info"""
    insert_data_in_wallet(user_id, sum_all_data(user_id))
    tg_id = user_id['id']
    postgresql_select_query = f"select * from wallet where tg_id ={tg_id}"
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(postgresql_select_query)
                wallet_records = cur.fetchall()
                print(wallet_records)
                for row in wallet_records:
                    wallet_content = row[3]
                    return f"В вашем кошельке {wallet_content} средств"
            except ConnectionError:
                logging.warning("show wallet info error")
            else:
                conn.commit()
            finally:
                conn.close()


def insert_data_in_wallet(user_id, money=0):
    """Function will insert data in his/her wallet"""
    tg_id=user_id['id']
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                postgres_insert_query = f""" UPDATE WALLET SET WALLET_CONTENT = {money}
                WHERE TG_ID = {tg_id};"""
                print(postgres_insert_query)
                cur.execute(postgres_insert_query)
                conn.commit()
                return "Данные записаны"
            except ConnectionError:
                logging.warning("Insert data in wallet error")
            finally:
                conn.close()
