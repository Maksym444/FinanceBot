import os
import logging
import time
from datetime import datetime
from fpdf import FPDF
import re
import psycopg
import config
from pylab import figure, axes, pie
from matplotlib import pyplot as plt

logging.basicConfig(level=logging.INFO)

logging.basicConfig(filename='/log/pdf_creation.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


def remove_emojis(data):
    emoj = re.compile("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese char
                      u"\U00002702-\U000027B0"
                      u"\U00002702-\U000027B0"
                      u"\U000024C2-\U0001F251"
                      u"\U0001f926-\U0001f937"
                      u"\U00010000-\U0010ffff"
                      u"\u2640-\u2642"
                      u"\u2600-\u2B55"
                      u"\u200d"
                      u"\u23cf"
                      u"\u23e9"
                      u"\u231a"
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)


def get_all_info(user_id, start_date, end_date):
    tg_id = user_id
    postgresql_select_query = f"select * from EXPENDITURE where tg_id={tg_id}"
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            cur.execute(postgresql_select_query)
            data = cur.fetchall()
            plus = list()
            minus = list()
            d = dict()
            for row in data:
                data_date = row[6]
                if start_date < data_date < end_date:
                    if row[5]:
                        plus.append(row[2])
                    else:
                        minus.append(row[2])
            d['Ваши доходы'] = sum(plus)
            d['Ваши траты:'] = sum(minus)
            return d


def get_sum_each_categories(user_id, start_date, end_date):
    tg_id = user_id
    postgresql_select_query = f"select * from EXPENDITURE where tg_id={tg_id}"
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
            cur.execute(postgresql_select_query)
            data = cur.fetchall()
            list_c = list()
            for row in data:
                data_date = row[6]
                if start_date < data_date < end_date:
                    list_c.append(row[3])
            categories = set(list_c)
            all = list()
            for i in categories:
                temp = dict()
                l = list()
                for row in data:
                    data_date = row[6]
                    if start_date < data_date < end_date:
                        if i == row[3]:
                            l.append(row[2])
                temp['Категория'] = i
                temp['Сумма'] = (sum(l))
                all.append(temp)
            return all


def get_all_date_annotation(user_id, start_date, end_date):
    tg_id = user_id
    postgresql_select_query = f"select * from EXPENDITURE where tg_id={tg_id}"
    with psycopg.connect(f"dbname={config.database} user={config.user}") as conn:
        with conn.cursor() as cur:
                cur.execute(postgresql_select_query)
                data = cur.fetchall()
                all = list()
                for row in data:
                    data_date = row[6]
                    if start_date < data_date < end_date:
                        category = row[3]
                        all.append(category)
                main = set(all)
                all_info_list = list()
                for i in main:
                    info = dict()
                    info["Категория"] = i
                    d_l = list()
                    for a in data:
                        data_date = a[6]
                        if start_date < data_date < end_date:
                            for d in info.values():
                                if d == a[3]:
                                    da = dict()
                                    da['Дата'] = datetime.strftime(a[6], "%d.%m.%Y")
                                    da['Сумма'] = a[2]
                                    da['Аннотация'] = a[4]
                                    d_l.append(da)
                    info["Основная инфа"] = d_l
                    all_info_list.append(info)
                return all_info_list


class PDF(FPDF):
    # Page header
    def header(self):
        self.set_y(0)
        self.set_left_margin(0)
        self.set_right_margin(0)
        # Colors of background and text
        self.set_fill_color(0, 163, 255)
        self.set_text_color(255, 255, 255)
        self.set_font('Times', 'B', 24)
        self.cell(0, 16, 'Finance-Bot', 0, 0, 'C', 1)
        # Logo
        self.image('static/logo.png', 15, 2, 12, 12)
        self.ln(20)
        # Page footer

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.cell(0, 10, 'finance_bot', 0, 0, 'C')
        # Page number
        self.cell(0, 10, str(self.page_no()), 0, 0, 'C')
        # logging_info = f'Detail page created for word {word}!'
        # logging.info(logging_info)

#     # Main page for score data
    def first_page(self,user_id, start_date, end_date):
        self.set_left_margin(15)
        self.set_right_margin(20)
        self.add_font('Merriweather_Bold', '', 'static/fonts/Merriweather/Merriweather-Bold.ttf', uni=True)
        self.add_font('Merriweather_Regular', '', 'static/fonts/Merriweather/Merriweather-Regular.ttf', uni=True)
        self.add_font('Merriweather_Italic', '', 'static/fonts/Merriweather/Merriweather-BoldItalic.ttf', uni=True)

        self.set_font('Merriweather_Bold', '', 20)
        self.cell(0, 10, f'Отчет за период с {str(start_date)[:10]} по {str(end_date)[:10]}', 0, 1, 'C')
        self.cell(10, 5, '', 0, 10, 'C')
        self.set_font('Merriweather_Regular', '', 15)
        value = [v for k,v in get_all_info(user_id, start_date, end_date).items()]
        self.multi_cell(165, 10, "Ваши доходы за выбранный промежуток времени: ", border=0, ln=3,
                        max_line_height=self.font_size)
        self.set_font('Merriweather_Bold', '', 15)
        self.multi_cell(40, 10,f'{value[0]}', border=0, ln=3,
                        max_line_height=self.font_size)
        self.ln(10)
        self.set_font('Merriweather_Regular', '', 15)
        self.multi_cell(165, 10, "Ваши расходы за выбранный промежуток времени: ", border=0, ln=3,
                        max_line_height=self.font_size)
        self.set_font('Merriweather_Bold', '', 15)
        self.multi_cell(40, 10,f'{value[1]}', border=0, ln=3,
                        max_line_height=self.font_size)
        self.ln(15)

        data = get_sum_each_categories(user_id, start_date, end_date)
        self.set_font('Merriweather_Bold', '', 18)
        self.cell(0, 10, 'Общая сумма Ваших доходов и расходов за выбранный', 0, 1, 'C')
        self.cell(0, 10, 'промежуток времени по категориям:', 0, 1, 'C')
        self.cell(10, 2, '', 0, 10, 'C')
        ge = 1
        for i in data:
            self.set_font('Merriweather_Regular', '', 15)
            # self.cell(0, 10, f'{ge}. {i["Категория"]} - {i["Сумма"]}', 0, 1, 'L')
            self.multi_cell(80, 10, f'{ge}. {i["Категория"]}', border=0, ln=3,
                            max_line_height=self.font_size)
            self.set_font('Merriweather_Bold', '', 15)
            self.multi_cell(60, 10, f'-    {i["Сумма"]}', border=0, ln=3,
                            max_line_height=self.font_size)
            ge += 1
            self.ln(10)

        self.add_page()  # add new page
        self.set_y(30)
        labe = list()
        frac = list()
        explo = list()
        for i in data:
            labe.append(i["Категория"])
            frac.append(i["Сумма"])
            explo.append(0.15)

        figure(1, figsize=(6, 6))
        ax = axes([0.1, 0.5, 0.8, 0.45])

        labels = tuple(labe)
        fracs = frac
        explode = tuple(explo)

        pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                  fancybox=True, shadow=True, ncol=1)
        plt.savefig('foo.png')
        line_height = self.font_size * 1.9
        self.allow_images_transparency = False
        self.set_font("Helvetica", size=15)
        self.cell(w=self.epw/2, h=self.epw)
        self.image('foo.png', 0)
        self.ln(line_height)

        self.add_page() # add new page
        self.set_font('Merriweather_Bold', '', 18)
        self.set_left_margin(15)
        self.set_right_margin(20)
        self.cell(0, 10, f'{"Общий список Ваших доходов и расходов за выбранный"}', 0, 1, 'C')
        self.cell(0, 10, f'{"промежуток времени"}', 0, 1, 'C')
        self.cell(10, 2, '', 0, 10, 'C')
        col_width = self.epw / 2.94  # distribute content evenly
        for v in get_all_date_annotation(user_id, start_date, end_date):
            for a in v.values():
                if type(a) == str:
                    self.set_left_margin(15)
                    self.set_font('Merriweather_Bold', '', 16)
                    self.cell(0, 10, str(a), 0, 1, 'C')
                else:
                    gen = 1
                    for info in a:
                        if gen <= 1:
                            self.set_left_margin(15)
                            self.set_font('Merriweather_Italic', '', 15)
                            self.multi_cell(10, line_height, "ID", border=1, ln=3,
                                            max_line_height=self.font_size)
                        for i in info.keys():
                            if gen <= 1:  # генератор что бы вывести только один раз заглавие таблицы
                                self.set_left_margin(15)
                                self.set_font('Merriweather_Italic', '', 15)
                                self.multi_cell(col_width, line_height, i, border=1, ln=3,
                                                max_line_height=self.font_size)
                            else:
                                pass
                        gen += 1
                    self.ln(line_height)
                    gene = 1
                    for info in a:
                        self.set_left_margin(15)
                        self.set_font('Merriweather_Regular', '', 14)
                        self.multi_cell(10, line_height, str(gene), border=1, ln=3,
                                        max_line_height=self.font_size)
                        for c in info.values():
                            self.set_left_margin(15)
                            self.set_font('Merriweather_Regular', '', 14)
                            self.multi_cell(col_width, line_height, str(c), border=1, ln=3,
                                            max_line_height=self.font_size)
                        gene += 1
                        self.ln(line_height)
                self.cell(10, 5, '', 0, 10, 'C')


# date_format='%d.%m.%Y %H:%M:%S' for start_date and end_date
def create_pdf_doc(user_id, start_date, end_date):
    logging_info = f'Start creating pdf report to {user_id}, from {start_date} - to {end_date}!'
    logging.info(logging_info)
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    start = datetime.strptime(start_date, "%d.%m.%Y")
    end = datetime.strptime(end_date, "%d.%m.%Y")
    pdf.first_page(user_id, start, end)
    path = f'files/{user_id}'
    try:
        os.mkdir(path)
    except OSError as e:
        pass
    pdf.output(f'files/{user_id}/{start_date[:10]}-{end_date[:10]}.pdf', 'F')
    logging_info = f'PDF report done!'
    logging.info(logging_info)
