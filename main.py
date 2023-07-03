# -*- coding: utf-8 -*-
import asyncio
import telegram
import requests
import configparser
from xml.etree import ElementTree


def get_usd_rate():
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    root = ElementTree.fromstring(response.content)
    for currency in root.findall('Valute'):
        if currency.find('CharCode').text == 'USD':
            return float(currency.find('Value').text.replace(',', '.'))


async def send_message():
    today_course = get_usd_rate()
    total_price = 1623.5  # сумма, которую надо перевести из рублей в USD
    final_price = ((today_course/100)*3.1+today_course)*total_price
    final_msg = f'Сегодняшний курс: {today_course:.2f} \nПерерасчет на курс туроператора: {final_price:.2f}'
    print(final_msg)
    await bot.send_message(chat_id=chat_id, text=final_msg)


async def main():
    while True:
        await send_message()
        await asyncio.sleep(60)


config = configparser.ConfigParser()
config.read(r'C:\Users\user\Dev\USD API script\config.ini')
bot_token = config.get('bot_token', 'bot_token')
chat_id = config.get('chat_id', 'chat_id')
if __name__ == "__main__":
    bot = telegram.Bot(token=bot_token)
    asyncio.run(main())
