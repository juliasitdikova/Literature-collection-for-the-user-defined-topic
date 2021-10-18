#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os
import pandas as pd
get_ipython().system('pip install selenium')
get_ipython().system('pip install webdriver-manager')
from selenium.webdriver.chrome.options import Options
import selenium.webdriver as webdriver
import time

from email.message import EmailMessage
import smtplib
query = "RPA impact"
num_page = 2
sender = "yursitdikova@edu.hse.ru"
password = "" #password
receiver = "yursitdikova@edu.hse.ru"

query = query.replace(" ", "%20")
query_link = f"https://www.semanticscholar.org/search?q={query}&sort=relevance&page="

# working paths
working_dir = os.getcwd()
folder_for_pdf = os.path.join(working_dir, "articles")
webdriver_path = os.path.join(working_dir, "chromedriver")  # proper version https://chromedriver.chromium.org/

# check if articles directory is exist and create if not
if not os.path.isdir(folder_for_pdf):
    os.mkdir(folder_for_pdf)

# webdriver
chrome_options = Options()
prefs = {"plugins.always_open_pdf_externally": True,"download.default_directory": folder_for_pdf, "download.prompt_for_download": False}
chrome_options.add_experimental_option('prefs', prefs)
os.environ[
    "webdriver.chrome.driver"] = webdriver_path  # 'webdriver' executable needs to be in PATH. Please see https://sites.google.com/a/chromium.org/chromedriver/home

links_list = [query_link + str(page + 1) for page in range(num_page)]  # create links to follow

#driver = webdriver.Chrome(executable_path=webdriver_path, chrome_options=chrome_options)
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

final_info = []  # empty dictionary for articles info

for search_link in links_list:
    driver.get(search_link)
    time.sleep(3)
    articles = driver.find_elements_by_xpath("//a[@data-selenium-selector='title-link']")

    articles_links = []
    for article in articles:
        try:
            link = article.get_attribute("href")
            articles_links.append(link)
        except:
            pass

    for link in articles_links:
        driver.get(link)

        try:
            title = driver.find_element_by_xpath("//h1[@data-selenium-selector='paper-detail-title']").text
        except:
            title = ''

        try:
            authors = driver.find_element_by_xpath("//span[@class='author-list']").text
        except:
            authors = ''

        try:
            desc = driver.find_element_by_xpath("//span[@data-selenium-selector='text-truncator-text']").text
        except:
            desc = ''

        try:
            citations = driver.find_element_by_xpath("//a[@data-heap-nav='citing-papers']/span").text
            citations = citations.replace(' Citations', '')
        except:
            citations = '0'

        try:
            initial_dir = os.listdir(folder_for_pdf)
            try:
                url_to_pdf = driver.find_element_by_xpath(
                    "//a[@class='icon-button flex-paper-actions__button alternate-sources__dropdown-button alternate-sources__dropdown-button--show-divider']").click()
            except:
                url_to_pdf = None

            time.sleep(3)
            current_dir = os.listdir(folder_for_pdf)
            filename = list(set(current_dir) - set(initial_dir))[0]
            full_path = os.path.join(folder_for_pdf, filename)
        except Exception as e:
            full_path = None

        tmp_info = {}
        tmp_info.update({
            'title': title,
            'source': link,
            'authors': authors,
            'description': desc,
            'citations': citations,
            'path_to_file': full_path
        })

        final_info.append(tmp_info.copy())

driver.quit()

# write all info to excel
df = pd.DataFrame(final_info)
df = df[['title','source','authors','description','citations']]
excel_path = os.path.join(working_dir, "data.xlsx")
df.to_excel(excel_path, index=False)

# create email

mail = EmailMessage()
mail['From'] = sender
mail['To'] = receiver
mail['Subject'] = "Results of query: " + query.replace("%20", " ")
mail.set_content("Hi!\n\nFind attached excel file with articles info.\n\nBest regards,Julia")

# add article attachment
with open(excel_path, 'rb') as f:
    file_data = f.read()
    file_name = f'data.xlsx'
mail.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

# send email
server = smtplib.SMTP('smtp.office365.com',587)
server.starttls()
server.login(sender, password)
server.send_message(mail)
server.quit()


# In[3]:





# In[ ]:




