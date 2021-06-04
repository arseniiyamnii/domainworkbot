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
currentDir=os.getcwd()
TOKEN=os.environ['TELEGRAMM_API_BOT_TOKEN']

# Enable logging
#reponame
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
def new_domain_check(text):
    check = True
    for line in text.split():
        if len(line)>10:
            check = False
        if not bool(re.match(r"^([A-Z]|[a-z]|[0-9])+$", line)):
            check = False
    return(check)

def banned_check(text):
    if text.split()[0] == "Banned":
        return(True)
    else:
        return(False)
def active_processing(text):
    global currentDir
    os.chdir(currentDir+'/ansible-playbooks')
    for i in text.split():
        domain="vavada"+i+".com"
        process = subprocess.Popen(["bash",currentDir+"/callperlnew.sh",domain], stdout=subprocess.PIPE)
        output, error = process.communicate()
    process = subprocess.Popen(["bash",currentDir+"/gitactive.sh"], stdout=subprocess.PIPE)
    output, error = process.communicate()
    try:
        with open('mr.json') as json_file:
            data = json.load(json_file)
        return(data["web_url"])
    except:
        return("cant find mr.json")
    

def banned_processing(text):
    global currentDir
    os.chdir(currentDir+'/ansible-playbooks')
    allurls = [x.group() for x in re.finditer(r'([a-z]|[A-Z]|[0-9])*\.([a-z]|[A-Z]|[0-9])*',text)] # all banned urls
    # perl -0777 -i.original -pe 's/  - name: vavadahugewin001.com\n    state: active/  - name: vavadahugewin001.com\n    state: banned/igs' vars/production.yml
    for url in allurls:
        process = subprocess.Popen(["bash",currentDir+"/callperl.sh",url], stdout=subprocess.PIPE)
        output, error = process.communicate()
    process = subprocess.Popen(["bash",currentDir+"/gitbanned.sh"], stdout=subprocess.PIPE)
    output, error = process.communicate()
    try:
        with open('mr.json') as json_file:
            data = json.load(json_file)
        return(data["web_url"])
    except:
        return("cant find mr.json")

def check_message(text):
    if new_domain_check(text.text):
        return(str(active_processing(text.text)))
    elif banned_check(text.text):
        return(str(banned_processing(text.text)))
    else:
        return(False)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
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
    if str(sys.argv[1]) == "init":
        process = subprocess.Popen(("git clone "+os.environ['GITLAB_REPO_SSH']).split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        