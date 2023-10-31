from buff_ids import ids
import requests


def cny_to_usd(amount, rate):
    return round(amount * rate, 2)


def get_buff_price(buff_id):
    url = f"https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={buff_id}"
    response = requests.get(url)
    data = response.json()
    price = data['data']['items'][0]['price']
    return float(price)


class Listing:

    def __init__(self, skin_id, asset_id, name, wear, pattern, price, cny_to_usd_rate):
        self.skin_id = skin_id
        self.asset_id = asset_id
        self.name = name
        self.buff_id = ids[name]
        self.wear = float(wear)
        self.pattern = int(pattern)
        self.listing_price = round(float(price) / 100, 2)
        self.buff_price = cny_to_usd(get_buff_price(ids[name]), cny_to_usd_rate)
        self.link = f"https://csfloat.com/item/{skin_id}"

    def __str__(self):
        return f"Skin: {self.name} | Pattern: {self.pattern} | Float: {self.wear}"\
               f" | Listing Price: {self.listing_price} | Buff Price: {self.buff_price}"\
               f" | Link: {self.link}"

