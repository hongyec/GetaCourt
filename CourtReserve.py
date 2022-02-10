from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import argparse
import schedule
import time

def bookCourt(usernameValue, passwordValue, website):
    MAX_ATTEMPT = 10000

    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get((website))


    # Autofill the username
    username = browser.find_element_by_id('ctl00_pageContentHolder_loginControl_UserName')
    username.send_keys(usernameValue)

    # Autofill the password
    password = browser.find_element_by_id('ctl00_pageContentHolder_loginControl_Password')
    password.send_keys(passwordValue)

    # Auto signin
    signInButton = browser.find_element_by_id('ctl00_pageContentHolder_loginControl_Login')
    signInButton.click()

    # refresh the page until there is the ticket
    count = 0
    while True:
        try:
            ## Wait the page loaded and register for yourself
            submit = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, 'ctl00_pageContentHolder_btnContinueCart')))
            print("ello", submit)
            submit.click()
        except:
            print(count)
            count+=1
            browser.refresh()
            if count > MAX_ATTEMPT:
                raise Exception("exceed attempt limit")

def main():

    # acquire the argument
    parser = argparse.ArgumentParser(description='Automatically court reservation, designed to get a badminton court')
    parser.add_argument("-u", "--username", help = "username")
    parser.add_argument("-p", "--password", help = "password")
    parser.add_argument("-w", "--website", help = "the website you wanna reserve")
    parser.add_argument("-t", "--startTime", help = "set the schedule for the program to start")

    arguments = parser.parse_args()

    # shedule the time to start the script
    usernameValue = arguments.username
    passwordValue = arguments.password
    website = arguments.website
    startTime = arguments.startTime
    #bookCourt(usernameValue, passwordValue, website)
    schedule.every().day.at(startTime).do(bookCourt,usernameValue, passwordValue, website)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()