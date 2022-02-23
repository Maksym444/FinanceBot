# pylint: disable=C0114
# import datetime
import logging
import psycopg
from psycopg import errors
import pandas as pd
import config


def admin_show_user(tg_id):
    """Show users to admin in row data"""
    if config.admin == tg_id:
        postgresql_select_query = "select * from profile"
        with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(postgresql_select_query)
                    all_records = cur.fetchall()
                    users = []
                    for item in all_records:
                        user = item[1], item[4], item[6], item[8], item[9], item[13]
                        users.append(user)
                except ConnectionError:
                    logging.warning("Is_admin user error")
                else:
                    conn.commit()
                finally:
                    conn.close()
                    return users
    else:
        return "Нет такой команды"


def admin_user_to_exl(tg_id):
    """Function make xlsx file and save to admin"""
    if config.admin == tg_id:
        postgresql_select_query = "select * from profile"
        with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(postgresql_select_query)
                    all_records = cur.fetchall()
                    df = pd.DataFrame(columns=['TG_ID', 'IS_ADMIN', 'IS_BOT', 'USERNAME',
                                               'WALLET', 'FIRST_NAME', 'CONTACT',
                                               'PHONE_NUMBER', 'REGISTER_DATE', 'LANG',
                                               'QUESTION_TIME', 'ANSWER_TIME', 'ACTIVITY_DATE',
                                               'ACTIVITY'])
                    for item in all_records:
                        df = df.append({'TG_ID': [item[1]],
                                          'IS_ADMIN': [item[2]],
                                          'IS_BOT': [item[3]],
                                          'USERNAME': [item[4]],
                                          'WALLET': [item[5]],
                                          'FIRST_NAME': [item[6]],
                                          'CONTACT': [item[7]],
                                          'PHONE_NUMBER': [item[8]],
                                          'REGISTER_DATE': [item[9]],
                                          'LANG': [item[10]],
                                          'QUESTION_TIME': [item[11]],
                                          'ANSWER_TIME': [item[12]],
                                          'ACTIVITY_DATE': [item[13]],
                                          'ACTIVITY': [item[14]]}, ignore_index=True)
                    df.to_excel('./admin_files/users.xlsx', sheet_name='welcome', index=True)
                except ConnectionError:
                    logging.warning("admin users to xslx user error")
                else:
                    conn.commit()
                finally:
                    conn.close()
    else:
        return "Нет такой команды"

admin_user_to_exl(172608373)

def admin_show_user_activity(tg_id):
    """Show user activity in row data from table profile"""
    if config.admin == tg_id:
        postgresql_select_query = "select * from profile where activity = True"
        with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(postgresql_select_query)
                    all_records = cur.fetchall()
                    users = []
                    for item in all_records:
                        user = item[1], item[4], item[6], item[8], item[9], item[13]
                        users.append(user)
                except ConnectionError:
                    logging.warning("Is_admin user error")
                else:
                    conn.commit()
                finally:
                    conn.close()
                    return users
    else:
        return "Нет такой команды"


def make_admin(tg_id):
    """MAKE admin function. SET True in column is_admin in Profile table"""
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            try:
                postgres_insert_query = f""" UPDATE PROFILE SET IS_ADMIN =
                TRUE WHERE TG_ID = {tg_id};"""
                cur.execute(postgres_insert_query)
                conn.commit()
            except ConnectionError:
                raise
            finally:
                conn.close()


# def check_user_activity(date):
#     """Check user activity"""
#     postgresql_select_query = "select * from profile"
#     with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
#         with conn.cursor() as cur:
#             try:
#                 cur.execute(postgresql_select_query)
#                 all_records = cur.fetchall()
#                 for item in all_records:
#                     last_date = item[12]
#                     check_date = last_date + datetime.timedelta(days=14)
#                     if check_date < date:
#                         postgres_insert_query = f""" UPDATE PROFILE SET ACTIVITY
#                         = FALSE WHERE TG_ID = {item[0]};"""
#                         cur.execute(postgres_insert_query)
#                         conn.commit()
#                         return f"Пользователь {item[0]} за 2 недели ни разу не запускал"
#                     else:
#                         return f"Пользователь {item[0]} за 2 недели хоть раз что то делал."
#             except errors:
#                 logging.warning("Is_admin user error")
#             else:
#                 conn.commit()
#             finally:
#                 conn.close()
