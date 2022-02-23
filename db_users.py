# pylint: disable=C0114
import string
import os
import random
import logging
import psycopg
from datetime import datetime
from psycopg import errors
import config
import db_structure  # pylint: disable=W0611
import db_wallet
from db_admin import make_admin
from main_pdf import create_pdf_doc


def check_user(user_id, date):
    """Big function check, create, make admin, create wallet"""
    tg_id = user_id['id']
    postgresql_select_query = f"select from profile where tg_id = '{tg_id}'"
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(postgresql_select_query)
                profile_records = cur.fetchall()
                username = user_id['username']
                if username is None:
                    username = "Безымянный"
                if not profile_records:
                    db_wallet.create_user_wallet(user_id, save_user(user_id, date), date)
                    create_directory(user_id)
                    if tg_id == config.admin:
                        make_admin(tg_id)
                    return f"Добро пожаловать, {username}.Мы создали Вам кошелек."
                for item in profile_records:
                    if not bool(item):
                        return f"С возвращением, {username}"
                    else:
                        db_wallet.create_user_wallet(user_id, save_user(user_id, date), date)
                        create_directory(user_id)
                        if tg_id == config.admin:
                            make_admin(tg_id)
                        return f"Добро пожаловать, {username}.Мы создали Вам кошелек."
            except ConnectionError:
                return logging.warning("CHECK_USER CONNECTION ERROR")
            else:
                conn.commit()
            finally:
                conn.close()


def take_user_reg_time(tg_id):
    postgresql_select_query = f"select REGISTER_DATE from profile where tg_id = '{tg_id}'"
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(postgresql_select_query)
                date = cur.fetchone()
                reg = datetime.strftime(date[0], "%d.%m.%Y")
            except ConnectionError:
                return logging.warning("CHECK_USER CONNECTION ERROR")
            else:
                conn.commit()
            finally:
                conn.close()
                return reg




def create_directory(user_id):
    """Function create directory for files"""
    tg_id = user_id['id']
    directory = f'{tg_id}'
    parent_dir = './files'
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)


def save_user(user_id, date):
    """Function save user to table"""
    tg_id = user_id['id']
    is_bot = user_id['is_bot']
    if user_id['last_name'] is not None:
        name = user_id['first_name'] + ' ' + user_id['last_name']
    else:
        name = user_id['first_name']
    username = user_id['username']
    if username is None:
        username = "Безымянный"
    wallet = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    lang = user_id['language_code']
    postgres_insert_query = """ INSERT INTO PROFILE (TG_ID, IS_ADMIN, IS_BOT, USERNAME, WALLET,
     FIRST_NAME, CONTACT, PHONE_NUMBER, REGISTER_DATE, LANG, QUESTION_TIME_TIME,
                 ANSWER_TIME_DAY, ANSWER_TIME_SCHEDULE, ACTIVITY_DATE, ACTIVITY) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    record_to_insert = (tg_id, False, is_bot, username, wallet, name, False, 'None', date,
                        lang, "18:00", "sunday", 30, date, True)
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(postgres_insert_query, record_to_insert)
            except ConnectionError:
                logging.warning("Save user error")
            else:
                conn.commit()
            finally:
                conn.close()
                return wallet


def update_user_contact(tg_id, phone_number):
    """Update user contact"""
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                postgres_insert_query = f""" UPDATE PROFILE SET CONTACT = TRUE,
                PHONE_NUMBER = {phone_number} WHERE TG_ID = {tg_id};"""
                cur.execute(postgres_insert_query)
                conn.commit()
                return "Данные записаны"
            except ConnectionError:
                logging.warning("Save data to  error")
            finally:
                conn.close()


def check_phone(tg_id, start_date, end_date):
    """Function will check if user have contact"""
    postgresql_select_query = f"select CONTACT from profile where tg_id = '{tg_id}'"
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(postgresql_select_query)
                phone = cur.fetchone()
                if phone[0]:
                    create_pdf_doc(tg_id, start_date, end_date)
                    return "Ваши данные"
                else:
                    return False
            except ConnectionError:
                logging.warning("Check_phone error")
            finally:
                conn.close()


def delete_phone(tg_id):
    """Function will delete phone number"""
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                postgres_insert_query = f""" UPDATE PROFILE SET CONTACT = FALSE,
                PHONE_NUMBER = 'None' WHERE TG_ID = {tg_id};"""
                cur.execute(postgres_insert_query)
                conn.commit()
                return "Данные удалены"
            except ConnectionError:
                logging.warning("Save data to minus error")
            finally:
                conn.close()


def update_user_activity(tg_id, date):
    """Function will update user activity trigger in table"""
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                postgres_insert_query = f""" UPDATE PROFILE SET ACTIVITY_DATE = '{date}'
                 WHERE TG_ID = {tg_id};"""
                cur.execute(postgres_insert_query)
                conn.commit()
                return "Данные записаны"
            except ConnectionError:
                logging.warning("Save data to minus error")
            finally:
                conn.close()


def get_all_user_tg_id():
    """Function will collect and return tg_id of all users"""
    postgresql_select_query = "select * from profile"
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(postgresql_select_query)
                all_users = cur.fetchall()
                users = []
                for item in all_users:
                    user = item[1]
                    users.append(user)
                return users
            except ConnectionError:
                logging.warning("GET ALL USER TG_ID error")
            finally:
                conn.close()
