
#5711334526:AAHd7qg_DfVqrVHU61pC3XincRHBeQ5ggmI

from flask import Flask, Response,request
import requests



TOKEN = '5711334526:AAHd7qg_DfVqrVHU61pC3XincRHBeQ5ggmI'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://b135-82-80-173-170.eu.ngrok.io/message'.format(TOKEN)
app = Flask(__name__)

@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    chat_id = request.get_json()['message']['chat']['id']
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TOKEN, chat_id, "Got it"))

    return Response("success")

@app.route('/')
def index():
    return "<h1>server is runnig!</h1>"


if __name__ == '__main__':
    requests.get(TELEGRAM_INIT_WEBHOOK_URL)
    app.run(port=5002)
   # response = requests.get(TELEGRAM_INIT_WEBHOOK_URL)
   #print(response.status_code)



