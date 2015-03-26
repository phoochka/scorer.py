import os
from sys import version_info
import requests
from bs4 import BeautifulSoup
from time import sleep
import logging

logging.basicConfig(level=logging.DEBUG)

# The notifier function
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

"""
# Calling the function
notify(title    = 'A Real Notification',
       subtitle = 'with python',
       message  = 'Hello, this is me, notifying you!')
"""

def sendmessage(title, message):
    if notifyModule is "pynotify":
        logging.debug("Initializing pynotify")
        pynotify.init("Scorer")
        logging.debug("Sending notification: title:{}, message:{}".format(title,message))
        pynotify.Notification(title, message, "dialog-information").show()
    elif notifyModule is "Notify":
        logging.debug("Initializing Notify")
        Notify.init("Scorer")
        logging.debug("Sending notification: title:{}, message:{}".format(title,message))
        Notify.Notification.new(title, message, "dialog-information").show()
    else:
        logging.debug("Initializing notify2")
        notify2.init("Scorer")
        logging.debug("Sending notification: title:{}, message:{}".format(title,message))
        notify2.Notification(title, message, "dialog-information").show()


url, match, score, interrupted = "http://static.cricinfo.com/rss/livescores.xml", 0, "", False

print("Fetching matches..")
while True:
    try:
        logging.info("Sending requests")
        r = requests.get(url)
        while r.status_code is not 200:
            logging.debug("Request failed: trying again")
            sleep(2)
            r = requests.get(url)
        data = BeautifulSoup(r.text).find_all("description")
        if not match:
            print("Matches available:")
            for counter, game in enumerate(data[1:], 1):
                print(counter, game.text)
            match = int(input("Enter your choice: "))
            while True:
                if match in range(1, counter):
                    break
                match = int(input("Invalid Choice. Enter your choice: "))
            interrupted=False
        newscore = data[match].text
        logging.info("Score found is {}".format(newscore))
        if newscore != score:
            logging.info("This is the most recent score, send me a notification")
            score = newscore
            notify("Score","India vs Aus", score)
        sleep(15)

    except KeyboardInterrupt:
        if interrupted:
            logging.info("keyboard interrupted, once")
            print("Bye bye")
            break
        else:
            print("Press Ctrl+C again to quit")
            match, interrupted = 0, True

