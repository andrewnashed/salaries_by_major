from selenium import webdriver
import csv
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


driver = webdriver.Chrome(executable_path=os.getenv("EXECUTABLE_PATH"))
driver.get("https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors")

columns = [i.text for i in driver.find_elements_by_class_name("data-table__header")]
p = 0
data = []
while p < 34:
    for item in driver.find_elements_by_class_name("data-table__row"):
        row_data = [i.text for i in item.find_elements_by_class_name("data-table__cell")]
        data.append(row_data)
    driver.find_element_by_class_name('pagination__next-btn').click()
    p += 1


with open('payscale_majors_pay_you_back.csv', 'w', encoding='UTF8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(columns)
    writer.writerows(data)


driver.close()
df = pd.read_csv('payscale_majors_pay_you_back.csv')

new_df = df.drop(columns=['Rank', '% High Meaning'])


def convert_string(dataframe):
    e = dataframe.str.replace("^\['|'\]$", "").str.replace("$", "").str.replace(",", "")
    dataframe = pd.to_numeric(e)
    return dataframe


new_df['Early Career Pay'] = convert_string(new_df['Early Career Pay'])
new_df['Mid-Career Pay'] = convert_string(new_df['Mid-Career Pay'])

new_df.to_csv('salaries_by_major.csv', index=False)

