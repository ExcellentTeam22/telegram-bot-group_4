from flask import Flask, Response, request
import requests
import pyngrok
import pandas as pd

SHOPS = {}
VEGETABLES = {}

data = {
    'Yesh': ['', '0.3', '1.1'],
    'Rami Levi': ['0.5', '0.3', '1.3'],
    'Shoopersal': ['0.6', '0.3', '1'],
    'Osher Ad': ['0.5', '0.3', '']}

df = pd.DataFrame(data, index=['cucumber', 'tomato', 'onion'])
print(df)

TOKEN = "5644359637:AAG3m8x0zSNOJRttMEE7dZh7C0YhtJ9GivQ"
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://ed32-2a10-800e-be98-0-855d-a307-caea-9926.eu.ngrok.io/message'.format(
    TOKEN)

app = Flask(__name__)


def check_input(my_input_list: list) -> list:
    """

    :param my_input_list: input from user to check if valid.
    :return: list of relevant vegetables.
    """
    error_message =''
    list_of_vegetables = []
    for item in my_input_list:
        if item not in df.index:
            error_message = error_message +"\n"+("Dont found vegetable named \"" + item+"\"")
        else:
            list_of_vegetables.append(item)
    return list_of_vegetables, error_message


def add_to_dict(vegetables: list) -> None:
    """

    :param vegetables: list of vegetables
    add vegetables and amount to VEGETABLES dict from given list
    """
    for vegetable in vegetables:
        if vegetable in VEGETABLES.keys():
            VEGETABLES[vegetable] += 1
        else:
            VEGETABLES[vegetable] = 1


def delete_dicts():
    VEGETABLES.clear()
    SHOPS.clear()







def show_results():
    """

    Show the sorted shop by the sum of buy and missing vegetable.
    """
    sorted_shop_by_price = sorted(SHOPS.items(), key=lambda x: x[1][0])
    sorted_shop = sorted(sorted_shop_by_price, key=lambda x: x[1][1])
    respond = ''
    for shop in sorted_shop:
        if shop[1][0] != 0:
            respond = respond + "\n"+ (shop[0] + " price: " + str(shop[1][0])+" " + str(shop[1][2]))
    return respond


def average_calculation() -> None:
    """

    Calculation of an average purchase, including the amount of missing vegetables and information.
    """
    for shop in df.columns:
        SHOPS[shop] = [0, 0, ""]
    for need_vegetable in list(df.index):
        if need_vegetable in list(VEGETABLES.keys()):
            amount = VEGETABLES[need_vegetable]
            for shop in SHOPS.keys():
                if df[shop][need_vegetable]:
                    SHOPS[shop][0] = SHOPS[shop][0] + float(df[shop][need_vegetable]) * amount
                else:
                    SHOPS[shop][2] = SHOPS[shop][2] + "no " + need_vegetable + " "
                    SHOPS[shop][1] = SHOPS[shop][1] + 1


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    chat_id = request.get_json()['message']['chat']['id']
    input = request.get_json()['message']['text']
    if input == "end":
        delete_dicts()
        res = requests.get(
            "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TOKEN, chat_id, "By By"))
    else:
        print(input.split())
        list_of_vegetables, error_message = check_input(input.split())
        if error_message:
            res = requests.get(
                "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TOKEN, chat_id, error_message))

        add_to_dict(list_of_vegetables)
        average_calculation()
        respond = show_results()
        res = requests.get(
            "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TOKEN, chat_id, respond))

    return Response("success")


@app.route('/')
def index():
    return "<h1>server is runnig!</h1>"


if __name__ == '__main__':
    requests.get(TELEGRAM_INIT_WEBHOOK_URL)
    app.run(port=5002)
