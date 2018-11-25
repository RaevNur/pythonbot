import telebot, os, logging
from flask import Flask, request

TOKEN = "739393314:AAHWAmhb3lYsP-j2xhlejFMbojqXhRZigMo"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200
		
    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://guarded-mesa-96076.herokuapp.com/bot")
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    bot.remove_webhook()
    bot.polling(none_stop=True)