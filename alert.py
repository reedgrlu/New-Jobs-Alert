# references:
# https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25
# https://www.codementor.io/@gergelykovcs/how-and-why-i-built-a-simple-web-scrapig-script-to-notify-us-about-our-favourite-food-fcrhuhn45


# Future iteration:
# 1. add the job page links to the email for each hit
# 2. be able to do multiple page searches, clicking through pages

import bs4, requests, smtplib
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("location of googledriver on your system", options=options)

# link of the webpage that has the jobs postings
link = ""

driver.get(link)
page_source = driver.page_source
menu = bs4.BeautifulSoup(page_source, 'html.parser')

# parse through the html jobs page to find the target class name
# in the case below the class name is job-title
jobs = menu.select('.job-title')
available = False

# list of keywords that you would like to search for
keywords = [""] 

for job in jobs:
    output = str(job).lower()
    for word in keywords:
        if output.find(word) != -1 and available == False:
            available = True
        else:
            pass

# To enable gmail authentication, login on Chrome under yourUserName@gmail.com and go to:
# https://myaccount.google.com/lesssecureapps?pli=1

conn = smtplib.SMTP('smtp.gmail.com', 587) # smtp address and port
conn.ehlo() # call this to start the connection
conn.starttls() # starts tls encryption. When we send our password it will be encrypted.
conn.login('yourUserName@gmail.com', 'yourPassword')

if available == True:
    conn.sendmail('fromUser@gmail.com', 'toUser@gmail.com', "Subject: Attention!!!\n\nA New Job Is Available!\n\n" + link)
    conn.quit()
    print('Jobs available! Sent notificaton e-mails')

else:
    conn.sendmail('fromUser@gmail.com', 'toUser@gmail.com', "Subject: No New Jobs Available\n\n" + link)
    conn.quit()
    print('No new jobs available today')



