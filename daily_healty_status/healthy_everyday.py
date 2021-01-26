from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import tkinter.messagebox
import random
import sys
import string
import random
import base64
import csv



# base64 decode your password in case you use a bat to run the script
# and are afraid of password being stored in plaintext
def decode(s):
    return base64.b64decode(s).decode('ascii')

with open('login_information.csv') as f:    #read students information from csv
    reader = csv.reader(f)     
    for row in reader:
        if len(row)>1:  
                browser = webdriver.Chrome(executable_path=r'./webdriver/chromedriver.exe')        
                browser.get('http://ehall.seu.edu.cn/qljfwapp2/sys/lwReportEpidemicSeu/index.do')

                # browser.maximize_window()

                fields = browser.find_elements_by_class_name('auth_input')

                fields[0].send_keys(row[0])
                fields[1].send_keys(row[1])
                time.sleep(5)

                login_btn = browser.find_elements_by_class_name('auth_login_btn')
                login_btn[0].click()
                time.sleep(10)

               
                # add
                submit_btn = browser.find_element_by_css_selector('div.bh-btn.bh-btn-primary')
                submit_btn.click()               
                time.sleep(15)
                
               
                if len(browser.find_elements_by_css_selector('div.bh-dialog-btnContainerBox'))>0: #if you already filled,than continue
                    browser.quit()
                    print('Already filled !')
                    continue

                # random body temperature
                input_fields = browser.find_elements_by_tag_name('input')
                for i in input_fields:
                    if i.get_attribute("name").find("DZ_JSDTCJTW") >= 0:
                        # scroll down until body temperature textfield is visible
                        browser.execute_script("arguments[0].scrollIntoView();", i)

                        i.click()
                        i.send_keys(str(random.randint(362, 370) / 10.0))
                        break
                time.sleep(10)

                # save
                save_btn = browser.find_element_by_css_selector("div#save.bh-btn.bh-btn-primary")
                time.sleep(5)
                save_btn.click()
                time.sleep(5)

                # confirm
                confirm_btn = browser.find_element_by_css_selector("a.bh-dialog-btn.bh-bg-primary.bh-color-primary-5")
                confirm_btn.click()
                time.sleep(5)
                print("Successfully fill in!")
                browser.quit()
              

            