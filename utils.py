# # util.py
# import requests
# from bs4 import BeautifulSoup

# def fetch_webpage(url):
#     """请求网页内容并返回BeautifulSoup对象。"""
#     response = requests.get(url)
#     if response.status_code == 200:
#         return BeautifulSoup(response.text, 'html.parser')
#     else:
#         print("Failed to retrieve data")
#         return None

# def parse_headers(rows):
#     """解析表头行并返回最终的表头列表。"""
#     headers = {}
#     for th in rows[0].find_all('th'):
#         if th.has_attr('id'):
#             headers[th['id']] = {'name': th.get_text(separator=' ').strip()}
#     for th in rows[1].find_all('th'):
#         parent_id = th['headers'][0]
#         if parent_id in headers:
#             subheader_name = f"{headers[parent_id]['name']}.{th.get_text(separator=' ').strip()}"
#             headers[parent_id].setdefault('subheaders', []).append(subheader_name)
#     final_headers = []
#     for header_id, header_info in headers.items():
#         if 'subheaders' in header_info:
#             final_headers.extend(header_info['subheaders'])
#         else:
#             final_headers.append(header_info['name'])
#     return final_headers

# def parse_data_rows(rows, final_headers):
#     """解析数据行并返回DataFrame对象。"""
#     data = []
#     for row in rows[4:]:
#         cols = row.find_all(['th', 'td'])
#         row_data = [col.get_text(separator=' ').strip() for col in cols]
#         data.append(row_data)
#     return pd.DataFrame(data, columns=final_headers)

# def generate_filename(soup, df):
#     """基于网页中的时间戳和DataFrame中的时间信息生成文件名。"""
#     date_time_str = soup.find('p', id='timestamp').strong.get_text()
#     _, date_part = date_time_str.split(' on ', 1)
#     day_name, day, month, year, _ = date_part.split()

#     months = {
#         'January': '01', 'February': '02', 'March': '03', 'April': '04',
#         'May': '05', 'June': '06', 'July': '07', 'August': '08',
#         'September': '09', 'October': '10', 'November': '11', 'December': '12'
#     }
#     month_number = months[month]
#     formatted_date = f"{year}{month_number}{day.zfill(2)}"

#     time_part = df.loc[0, 'Date/Time EST'].replace(':', '').lower().split("/")[-1]
#     return f"{formatted_date}_{time_part}.csv"

# def save_dataframe(df, filename):
#     """保存DataFrame到CSV文件，不包含索引列。"""
#     df.to_csv(filename, encoding='utf-8-sig', index=False)

import requests
import logging
from bs4 import BeautifulSoup
import os
import pandas as pd

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_webpage(url):
    """请求网页内容并返回BeautifulSoup对象。"""
    response = requests.get(url)
    if response.status_code == 200:
        logging.info("Web page fetched successfully")
        return BeautifulSoup(response.text, 'html.parser')
    else:
        logging.error(f"Failed to retrieve data with status code: {response.status_code}")
        return None

def parse_headers(rows):
    """解析表头行并返回最终的表头列表。"""
    headers = {}
    for th in rows[0].find_all('th'):
        if th.has_attr('id'):
            headers[th['id']] = {'name': th.get_text(separator=' ').strip()}
    for th in rows[1].find_all('th'):
        parent_id = th['headers'][0]
        if parent_id in headers:
            subheader_name = f"{headers[parent_id]['name']}.{th.get_text(separator=' ').strip()}"
            headers[parent_id].setdefault('subheaders', []).append(subheader_name)
    final_headers = []
    for header_id, header_info in headers.items():
        if 'subheaders' in header_info:
            final_headers.extend(header_info['subheaders'])
        else:
            final_headers.append(header_info['name'])
    logging.info("Headers parsed successfully")
    return final_headers

def parse_data_rows(rows, final_headers):
    """解析数据行并返回DataFrame对象。"""
    data = []
    for row in rows[4:]:
        cols = row.find_all(['th', 'td'])
        row_data = [col.get_text(separator=' ').strip() for col in cols]
        data.append(row_data)
    logging.info("Data rows parsed successfully")
    return pd.DataFrame(data, columns=final_headers)

def generate_filename(soup, df):
    """基于网页中的时间戳和DataFrame中的时间信息生成文件名。"""
    date_time_str = soup.find('p', id='timestamp').strong.get_text()
    _, date_part = date_time_str.split(' on ', 1)
    day_name, day, month, year, _ = date_part.split()

    months = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04',
        'May': '05', 'June': '06', 'July': '07', 'August': '08',
        'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }
    month_number = months[month]
    formatted_date = f"{year}{month_number}{day.zfill(2)}"

    time_part = df.loc[0, 'Date/Time EST'].replace(':', '').lower().split("/")[-1]
    filename = f"{formatted_date}_{time_part}.csv"
    logging.info(f"Filename generated: {filename}")
    return filename

# def save_dataframe(df, filename):
#     """保存DataFrame到CSV文件，不包含索引列。"""
#     df.to_csv(filename, encoding='utf-8-sig', index=False)
#     logging.info(f"Data saved to {filename}")

def save_dataframe(df, filename):
    """保存DataFrame到CSV文件，不包含索引列，并检查文件是否已存在以避免重复保存。"""
    if os.path.exists(filename):
        logging.warning(f"File {filename} already exists. Ignore.")
    else:
        df.to_csv(filename, encoding='utf-8-sig', index=False)
        logging.info(f"Data saved to {filename}")
