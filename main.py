import time
from listing import Listing
import requests


def insert(skin_id, recents, LIMIT):
    if skin_id in recents:
        return False
    recents.insert(0, skin_id)
    if len(recents) == LIMIT + 1:
        recents.pop()

    return True


def get_csfloat_recent(MIN_AMOUNT, LIMIT, recents):
    if 0 > LIMIT or LIMIT > 50:
        LIMIT = 50
    url = f"https://csfloat.com/api/v1/listings?sort_by=most_recent&limit={LIMIT}"
    response = requests.get(url)
    data = response.json()
    for i in range(len(data)):
        if 'float_value' in data[i]['item']:
            skin_id = data[i]['id']
            price = data[i]['price']
            if insert(skin_id, recents, LIMIT) and (price / 100) >= MIN_AMOUNT:
                current_listing = Listing(
                    skin_id,
                    data[i]['item']['asset_id'],
                    data[i]['item']['market_hash_name'],
                    data[i]['item']['float_value'],
                    data[i]['item']['paint_seed'],
                    price,
                    CNY_USD_RATE
                )
                if current_listing.buff_price * (1 - (PERCENT_DISCOUNT / 100)) > current_listing.listing_price:
                    print(current_listing.__str__())
                time.sleep(.5)


if __name__ == '__main__':
    CNY_USD_RATE = float(input("What is the current CNY to USD conversion rate?: "))
    PERCENT_DISCOUNT = float(input("What is your desired BUFF discount? For 10% enter 10: "))
    MIN_AMOUNT = float(input("What is the minimum USD amount you want an item to be?: "))
    LIMIT = int(input("How many items do you want to scrape at a time?: "))
    RATE = int(input("How often do you want to scrape in seconds?: "))

    recents = []

    while True:
        get_csfloat_recent(MIN_AMOUNT, LIMIT, recents)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|"\
              " Cycle Complete "\
              "|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        time.sleep(RATE)
