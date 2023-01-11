import os
import json
from requests import get
from pprint import PrettyPrinter

BASE_URL = "https://free.currconv.com/"
filepath = f"{os.curdir}/api-key.json"

def ask_key():
    print("You are missing an API key!")
    print("Get one from https://www.currencyconverterapi.com,")
    print(f"then set the value in {filepath}.")
    exit()

if os.path.exists(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    key = data.get("key")
    if not key or key == "":
        ask_key()
    
    API_KEY = key
else:
    with open(filepath, 'w') as f:
        json.dump({"key": ""}, f, indent=4)
    ask_key()


printer = PrettyPrinter()

def get_currencies():
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    url = BASE_URL + endpoint
    resp = get(url)
    if resp.status_code == 400:
        print("Your API key is invalid or expired!")
        exit()

    data = data.json()['results']

    data = list(data.items())
    data.sort()

    return(data)

def print_currencies(currencies):
    for name, currency in currencies:
        name = currency['currencyName']
        _id = currency['id']
        symbol = currency.get("currencySymbol", "")
        print(f"{_id} - {name} - {symbol}")

def exchange_rate(curr1, curr2):
    endpoint = f"api/v7/convert?q={curr1}_{curr2}&compact=ultra&apiKey={API_KEY}"
    url = BASE_URL + endpoint
    data = get(url).json()

    if len(data) == 0:
        print('Invalid currencies.')
        return

    rate = list(data.values())[0]
    print( f"{curr1} --> {curr2} = {rate}")
    return rate

def convert(curr1, curr2, amount):
    rate = exchange_rate(curr1, curr2)
    if rate is None:
        return
    
    try:
        amount = float(amount)
    except:
        print("Invalid amount.")
        return
    
    converted_amount = rate * amount
    print(f"{amount} {curr1} = {converted_amount} {curr2}")

def main():
    currencies = get_currencies()

    print("Welcome to the Currency Converter.")
    print("   list - lists the different currencies")
    print("   convert - convert from one currency to another")
    print("   rate - get the exchange rate for two currencies")
    print()

    while True:
        command = input("Enter a command (q to quit): ").lower()

        if command == "q":
            break
        elif command == "list":
            print_currencies(currencies)
        elif command == "convert":
            curr1 = input("Enter a starting currency id: ").upper()
            curr2 = input("Enter an ending currency id: ").upper()
            amount = input(f"Enter an amount in {curr1}: ")
            convert(curr1, curr2, amount)
        elif command == "rate":
            curr1 = input("Enter a starting currency id: ").upper()
            curr2 = input("Enter an ending currency id: ").upper()
            exchange_rate(curr1, curr2)
        else:
            print("Unrecognized command.")

main()