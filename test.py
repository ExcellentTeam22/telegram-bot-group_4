import pandas as pd

SHOPS = {}
VEGETABLES = {}

data = {
    'yesh': ['', '0.3', '1.1'],
    'rami_levi': ['0.5', '0.3', '1.3'],
    'shoopersal': ['0.6', '0.3', '1'],
    'osher_ad': ['0.5', '0.3', '']}

df = pd.DataFrame(data, index=['cucumber', 'tomato', 'onion'])
print(df)


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


def check_input(my_input: str) -> list:
    """

    :param my_input: input from user to check if valid.
    :return: list of relevant vegetables.
    """
    list_of_vegetables = []
    my_list = my_input.split()
    for item in my_list:
        if item not in df.index:
            print("Dont found vegetable named " + item)
        else:
            list_of_vegetables.append(item)
    return list_of_vegetables


def show_results():
    """

    Show the sorted shop by the sum of buy and missing vegetable.
    """
    sorted_shop_by_price = sorted(SHOPS.items(), key=lambda x: x[1][0])
    sorted_shop = sorted(sorted_shop_by_price, key=lambda x: x[1][1])
    for shop in sorted_shop:
        print(shop[0] + " price: " + str(shop[1][0])+" " + str(shop[1][2]))


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


if __name__ == '__main__':
    my_input = input("Enter the vegetables: ")
    list_of_vegetables = []
    while my_input != "end":
        list_of_vegetables = check_input(my_input)
        add_to_dict(list_of_vegetables)
        my_input = input("Enter more vegetables or end: ")
    average_calculation()
    show_results()
