import logging
from config import Config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bot import updater, browser
from telegram.ext import run_async
from telegram import ChatAction
import os
import pickle
import time
from os import execl
from sys import executable

userId = Config.USERID


def joinMeet(context, url_meet):

    def students(context):
        try:
            number = WebDriverWait(browser, 2400).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ow3"]/div[1]/div/div[8]/div[3]/div[6]/div[3]/div/div[2]/div[1]/span/span/div/div/span[2]'))).text
        except:
            return
        print(number)
        if(int(number) <10):
            context.bot.send_message(chat_id=userId, text="Your Class has ended!")
            browser.quit()
            execl(executable, executable, "chromium.py")

    try:
        if os.path.exists("meet.pkl"):
            cookies = pickle.load(open("meet.pkl", "rb"))
            browser.get('https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3Afad07e7074c3d678%2C10%3A1601127482%2C16%3A9619c3b16b4c5287%2Ca234368b2cab7ca310430ff80f5dd20b5a6a99a5b85681ce91ca34820cea05c6%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%22d18871cbc2a3450c8c4114690c129bde%22%7D&response_type=code&flowName=GeneralOAuthFlow')
            for cookie in cookies:
                browser.add_cookie(cookie)

        else:
            context.bot.send_message(chat_id=userId, text="You're not logged in please run /mlogin command to login. Then try again!")
            return

        browser.get(url_meet)
        time.sleep(3)   

        browser.save_screenshot("ss.png")
        context.bot.send_chat_action(chat_id=userId, action=ChatAction.UPLOAD_PHOTO)
        mid  = context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), timeout = 120).message_id
        os.remove('ss.png')

        if(browser.find_elements_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div')):
            browser.find_element_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div').click()
            time.sleep(3)

            context.bot.delete_message(chat_id=userId ,message_id = mid)

            browser.save_screenshot("ss.png")
            context.bot.send_chat_action(chat_id=userId, action=ChatAction.UPLOAD_PHOTO)
            mid = context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), timeout = 120).message_id
            os.remove('ss.png')
        try:
            browser.find_element_by_xpath("//span[@class='NPEfkd RveJvd snByac' and contains(text(), 'Ask to join')]").click()
            time.sleep(10)
        except:
            browser.find_element_by_xpath("//span[@class='NPEfkd RveJvd snByac' and contains(text(), 'Join now')]").click()
            time.sleep(10)

        context.bot.delete_message(chat_id=userId ,message_id = mid)

        browser.save_screenshot("ss.png")
        context.bot.send_chat_action(chat_id=userId, action=ChatAction.UPLOAD_PHOTO)
        mid = context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), timeout = 120).message_id
        os.remove('ss.png')
        time.sleep(5)

        context.bot.delete_message(chat_id=userId ,message_id = mid)
        time.sleep(10)

        browser.save_screenshot("ss.png")
        context.bot.send_chat_action(chat_id=userId, action=ChatAction.UPLOAD_PHOTO)
        mid = context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), timeout = 120).message_id
        os.remove('ss.png')

        context.bot.send_chat_action(chat_id=userId, action=ChatAction.TYPING)
        context.bot.send_message(chat_id=userId, text="Attending your lecture. You can chill :v")
        logging.info("STAAAAPH!!")
    except Exception as e:
        browser.quit()
        context.bot.send_message(chat_id=userId, text="Error occurred! Fix error and retry!")
        context.bot.send_message(chat_id=userId, text=str(e))
        execl(executable, executable, "chromium.py")

    j = updater.job_queue
    j.run_repeating(students, 20, 1000)



@run_async
def meet(update,context):
    logging.info("DOING")

    context.bot.send_chat_action(chat_id=userId, action=ChatAction.TYPING)
    url_meet = update.message.text.split()[-1]
    joinMeet(context, url_meet)


