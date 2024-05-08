# # # from utils import fetch_webpage, parse_headers, parse_data_rows, generate_filename, save_dataframe

# # # def main():
# # #     url = 'https://reg.bom.gov.au/vic/observations/melbourne.shtml'
# # #     # 获取网页内容
# # #     soup = fetch_webpage(url)
# # #     if soup:
# # #         # 解析HTML以提取表头和数据
# # #         rows = soup.find_all('tr')
# # #         final_headers = parse_headers(rows)
# # #         df = parse_data_rows(rows, final_headers)
        
# # #         # 生成文件名并保存数据
# # #         filename = generate_filename(soup, df)
# # #         save_dataframe(df, filename)
# # #         print(f"Data saved to {filename}")

# # # if __name__ == "__main__":
# # #     main()

# # import os
# # import time
# # import datetime
# # from util import fetch_webpage, parse_headers, parse_data_rows, generate_filename, save_dataframe
# # import schedule

# # def main():
# #     url = 'https://reg.bom.gov.au/vic/observations/melbourne.shtml'
# #     # 获取网页内容
# #     soup = fetch_webpage(url)
# #     if soup:
# #         # 解析HTML以提取表头和数据
# #         rows = soup.find_all('tr')
# #         final_headers = parse_headers(rows)
# #         df = parse_data_rows(rows, final_headers)
        
# #         # 获取当前日期时间格式化字符串
# #         current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# #         # 创建一个新的目录在 log 下
# #         directory = f"log/{current_time}"
# #         if not os.path.exists(directory):
# #             os.makedirs(directory)
        
# #         # 生成文件名并保存数据
# #         filename = generate_filename(soup, df)
# #         full_path = f"{directory}/{filename}"
# #         save_dataframe(df, full_path)
# #         print(f"Data saved to {full_path}")

# # def schedule_run():
# #     schedule.every(9).minutes.do(main)
    
# #     # 无限循环，保持程序运行
# #     while True:
# #         schedule.run_pending()
# #         time.sleep(1)  # Sleep for a short time to prevent high CPU usage

# # if __name__ == "__main__":
# #     schedule_run()

# import os
# import time
# import datetime
# import schedule
# import logging
# from utils import fetch_webpage, parse_headers, parse_data_rows, generate_filename, save_dataframe

# def main():
#     logging.info("Starting the data fetch process")
#     url = 'https://reg.bom.gov.au/vic/observations/melbourne.shtml'
#     soup = fetch_webpage(url)
#     if soup:
#         rows = soup.find_all('tr')
#         final_headers = parse_headers(rows)
#         df = parse_data_rows(rows, final_headers)
        
#         current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         directory = f"log/{current_time}"
#         if not os.path.exists(directory):
#             os.makedirs(directory)
#             logging.info(f"Created directory: {directory}")
        
#         filename = generate_filename(soup, df)
#         full_path = f"{directory}/{filename}"
#         save_dataframe(df, full_path)

# # def schedule_run():
# #     schedule.every(9).minutes.do(main)
# #     logging.info("Scheduler started")
# #     while True:
# #         schedule.run_pending()
# #         time.sleep(1)

# def schedule_run():
#     # Run the main function immediately before setting up the scheduling
#     main()
#     logging.info("Initial run completed, setting up scheduler.")

#     # Schedule the main function to run every 9 minutes
#     schedule.every(9).minutes.do(main)
#     logging.info("Scheduler started. Next run scheduled in 9 minutes.")

#     # Infinite loop to keep the scheduler running
#     while True:
#         schedule.run_pending()
#         time.sleep(1)  # Sleep for a short time to prevent high CPU usage

# if __name__ == "__main__":
#     schedule_run()

import os
import time
import datetime
import schedule
import logging
from utils import fetch_webpage, parse_headers, parse_data_rows, generate_filename, save_dataframe

# 记录程序开始的时间
START_TIME = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def main():
    logging.info("Starting the data fetch process")
    url = 'https://reg.bom.gov.au/vic/observations/melbourne.shtml'
    soup = fetch_webpage(url)
    if soup:
        rows = soup.find_all('tr')
        final_headers = parse_headers(rows)
        df = parse_data_rows(rows, final_headers)
        
        directory = f"log/{START_TIME}"
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")
        
        filename = generate_filename(soup, df)
        full_path = f"{directory}/{filename}"
        save_dataframe(df, full_path)

def schedule_run():
    main()  # Run once immediately
    schedule.every(9).minutes.do(main)
    logging.info("Scheduler started")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    schedule_run()
