import telebot
from time import sleep
from selenium.common.exceptions import TimeoutException


class TelegramBot:
    TOKEN = '1342963300:AAGBnoqmIQ63KpcVMa9QuPgF_RtF_HXhwEU'
    CHAT_ID = 428637454
    TEXT = 'Hi'

    def __init__(self):
        self.types = telebot.types

    def send_message_to_telega(self, text):
        try:
            self.bot = telebot.TeleBot(TelegramBot.TOKEN, parse_mode=None)
            self.bot.send_message(TelegramBot.CHAT_ID, text)
            print('Massage is send')
        except TimeoutException:
            sleep(1)
            self.send_message_to_telega()

    def send_message(self, text):
        self.bot.send_message(TelegramBot.CHAT_ID, text)

