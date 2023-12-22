from discord_listing import Listing
import discord
from discord.ext import commands
import asyncio
import requests

def insert(skin_id, recents, LIMIT):
    if skin_id in recents:
        return False
    recents.insert(0, skin_id)
    if len(recents) == LIMIT + 1:
        recents.pop()
    return True


async def get_csfloat_recent(CNY_USD_RATE, PERCENT_DISCOUNT, MIN_AMOUNT, LIMIT, recents, channel):
    if 0 > LIMIT or LIMIT > 50:
        LIMIT = 50
    url = f"https://csfloat.com/api/v1/listings?sort_by=most_recent&limit={LIMIT}"
    response = requests.get(url)
    data = response.json()
    for i in range(len(data)):
        if 'float_value' in data[i]['item']:
            skin_id = data[i]['id']
            price = data[i]['price']
            min_offer_price = "No Bargains Enabled"
            if 'min_offer_price' in data[i]:
                min_offer_price = round(float(data[i]['min_offer_price']) / 100, 2)
            if insert(skin_id, recents, LIMIT) and (price / 100) >= MIN_AMOUNT:
                current_listing = Listing(
                    skin_id,
                    data[i]['item']['asset_id'],
                    data[i]['item']['market_hash_name'],
                    data[i]['item']['float_value'],
                    data[i]['item']['paint_seed'],
                    min_offer_price,
                    data[i]['seller']['statistics']['total_verified_trades'],
                    price,
                    CNY_USD_RATE
                )
                if current_listing.buff_price * (1 - (PERCENT_DISCOUNT / 100)) > current_listing.listing_price:
                    await channel.send(f"```{current_listing.__str__()}```")
                await asyncio.sleep(0.5)
                
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        while True:
            await get_csfloat_recent(.14, -100, 0, 20, [], channel)
            await asyncio.sleep(60)



bot.run("{BOT_TOKEN}")
