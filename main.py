#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import yaml
import logging
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import subprocess
import json
import sys
currentDir = os.getcwd()
TOKEN = os.environ['TELEGRAMM_API_BOT_TOKEN']

# Enable logging
# reponame
logging.basicConfig(format='\
%(asctime)s - \
%(name)s - \
%(levelname)s - \
%(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def new_domain_check(text):
    check = True
    for line in text.split():
        if len(line) > 15:
            check = False
        if not bool(re.match(r"^([A-Z]|[a-z]|[0-9])+$", line)) and not bool(re.match(r"^vavada([A-Z]|[a-z]|[0-9])+.com$", line)):
            check = False
    return(check)


def banned_check(text):
    if text.split()[0] == "Banned":
        return(True)
    else:
        return(False)


def active_processing(text, mode):
    global currentDir
    os.chdir(currentDir+'/repo')
    with open("vars/production.yml", 'r') as f:
        prod = f.readlines()
    for i in text.split():
        if bool(re.match(r"^vavada([A-Z]|[a-z]|[0-9])+.com$", i)):
            domain = i
        else:
            domain =\
                os.environ["DOMAIN_MAIN_URL_START"]\
                + i +\
                os.environ["DOMAIN_MAIN_URL_END"]
        print(domain)
        space = [i for i, x in enumerate(prod) if x == "\n"]
        lastline = 0
        for i in space:
            # print(prod[int(i)-1])
            if prod[int(i)-1] == "    state: active\n" or prod[int(i)-1] == "    state: banned\n":
                lastline = i
                break
        prod.insert(lastline, "    state: active\n")
        prod.insert(lastline, "    kind: combined\n")
        prod.insert(lastline, "  - name: "+domain+"\n")
    with open("vars/production.yml", 'w') as f:
        for item in prod:
            f.write(item)
    answer = ""
    answer=gitprocess("active", mode)
    return(answer)


def banned_processing(text,mode):
    global currentDir
    os.chdir(currentDir+'/repo')
    with open("vars/production.yml", 'r') as f:
        prod = f.readlines()
    allurls = [x.group() for x in re.finditer(
        r'([a-z]|[A-Z]|[0-9])*\.([a-z]|[A-Z]|[0-9])*', text)]
    for url in allurls:
        ind = int(prod.index("  - name: "+url+"\n"))
        del prod[ind]
        del prod[ind]
        if "  - name" not in prod[ind]:
            del prod[ind]
        space = [i for i, x in enumerate(prod) if x == "\n"]
        lastline = 0
        for i in space:
            # print(prod[int(i)-1])
            if prod[int(i)-1] == "    state: active\n" or prod[int(i)-1] == "    state: banned\n":
                lastline = i
                break
        prod.insert(lastline, "    state: banned\n")
        prod.insert(lastline, "  - name: "+url+"\n")
    with open("vars/production.yml", 'w') as f:
        for item in prod:
            f.write(item)
    # for url in allurls:
        # string = "s/  - name: "+url+"\n    state: active//igs"
        # subprocess.call(["perl", "-0777", "-i", "-pe", string, "vars/production.yml"])
        # string = "s/    state: active\n\n/    state: active\n  - name: "+url+"\n    state: banned\n\n/igs"
        # # perl -0777 -i -pe "${string}" vars/production.yml

        # subprocess.call(["perl", "-0777", "-i", "-pe", string, "vars/production.yml"])
    answer=gitprocess("banned", mode)
    return(answer)


def check_message(text,mode):
    try:
        msg=text.text
    except:
        msg=text
    if new_domain_check(msg):
        print("adding new domains")
        return(str(active_processing(msg, mode)))
    elif banned_check(msg):
        return(str(banned_processing(msg, mode)))
    else:
        return(False)

# Define a few command handlers.
# These usually take the two arguments update andcontext.
# Error handlers also receive the raised TelegramError object in error.

def gitprocess(text, mode):
    subprocess.call(["bash", currentDir+"/gitprocessing.sh", text, str(mode)])
    try:
        with open('mr.json') as json_file:
            data = json.load(json_file)
        return(data["web_url"])
    except OSError:
        return("cant find mr.json. Something wrong!")


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    answer = check_message(update.message)
    if answer:
        update.message.reply_text(str(answer))


def manual(myargv=1):
    text = sys.argv[myargv]
    answer = check_message(text, myargv)
    if answer:
        print(str(answer))


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    if str(sys.argv[1]) == "start":
        main()
    if str(sys.argv[1]) == "reinit":
        process = subprocess.Popen(
            ("rm -rf repo").split(),
            stdout=subprocess.PIPE)
        output, error = process.communicate()
        process = subprocess.Popen(
            ("git clone "+os.environ['GITLAB_REPO_SSH']+" repo").split(),
            stdout=subprocess.PIPE)
        output, error = process.communicate()
        exit()
    if str(sys.argv[1]) == "init":
        process = subprocess.Popen(
            ("git clone "+os.environ['GITLAB_REPO_SSH']+" repo").split(),
            stdout=subprocess.PIPE)
        output, error = process.communicate()
        exit()
    if str(sys.argv[1]) == "test":
        message = """abc
def
ghi"""
        if new_domain_check(message):
            answer=(str(active_processing(message)))
        elif banned_check(message):
            answer=(str(banned_processing(message)))
        else:
            answer=(False)

        if answer:
            print(str(answer))
    if str(sys.argv[1]) == "add":
        manual(2)
    else:
        manual()
