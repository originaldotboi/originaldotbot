from aiogram import Bot, Dispatcher, types
import asyncio
import logging
from alerts_in_ua import Client as AlertsClient
import asyncio
import random
import logging
import requests


TELEGRAM_TOKEN = '7157883595:AAG9rR9ovslnfeIciHQncSkqvCiSznIjVfI'
CHAT_ID = '-1002057553857'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


alerts_client = AlertsClient(token="b24eabefa69df127630fb9d126cd1e9168d17f96ab2203")

async def is_alert_active_for_region(region_name: str) -> bool:
    # Використовуємо asyncio.to_thread() для виклику синхронної функції асинхронно
    active_alerts = await asyncio.to_thread(alerts_client.get_active_alerts)
    for alert in active_alerts:
        # Замінюємо доступ через квадратні дужки на доступ через атрибути
        if alert.location_title == region_name and alert.finished_at is None:
            return True
    return False

gif_list = [
    'https://media1.tenor.com/m/_NXwuzGUy_QAAAAC/%D0%BF%D0%BE%D0%B2%D1%96%D1%82%D1%80%D1%8F%D0%BD%D0%B0%D1%82%D1%80%D0%B8%D0%B2%D0%BE%D0%B3%D0%B0-%D1%82%D1%80%D0%B8%D0%B2%D0%BE%D0%B3%D0%B0.gif',
    'https://media1.tenor.com/m/fkodgmYAqNsAAAAd/uvaga-warning.gif',
    'https://media1.tenor.com/m/8-u8mRydMe8AAAAd/%D0%BF%D0%BE%D0%B2%D1%96%D1%82%D1%80%D1%8F%D0%BD%D0%B0-%D1%82%D1%80%D0%B8%D0%B2%D0%BE%D0%B3%D0%B0-%D1%82%D1%80%D0%B8%D0%B2%D0%BE%D0%B3%D0%B0.gif',
    'https://media.tenor.com/ZiflRimYLA4AAAAM/%D0%BF%D0%BE%D0%B2%D1%96%D1%82%D1%80%D1%8F%D0%BD%D0%B0%D1%82%D1%80%D0%B8%D0%B2%D0%BE%D0%B3%D0%B0.gif',
    'https://media.tenor.com/6_kY_Cn26awAAAAM/%D0%BF%D0%BE%D0%B2%D1%96%D1%82%D1%80%D1%8F%D0%BD%D0%B0-%D1%82%D1%80%D0%B8%D0%B2%D0%BE%D0%B3%D0%B0-%D1%85%D1%80%D1%8E%D0%BA%D0%B0%D1%82%D0%B8.gif',
    'https://media.tenor.com/uJRsvDxXvI8AAAAM/%D0%BC%D0%B0%D0%B2%D0%BF%D0%B8-%D0%BC%D0%B0%D0%B2%D0%BF%D0%B0.gif',
    'https://media1.tenor.com/m/_x93cTEdgooAAAAC/siren-%D1%82%D1%80%D0%B8%D0%B2%D0%BE%D0%B3%D0%B0.gif',
    'https://media4.giphy.com/media/MyJXZMbjRaXjQw591u/200.gif',
    'https://media1.giphy.com/media/4b1fm8BYmrU30B4n5u/200.gif'
]

gif_list2 = [
    'https://media1.tenor.com/m/cKrq7zekafEAAAAd/%D0%B2%D1%96%D0%B4%D0%B1%D1%96%D0%B9%D0%BF%D0%BE%D0%B2%D1%96%D1%82%D1%80%D1%8F%D0%BD%D0%BE%D1%97%D1%82%D1%80%D0%B8%D0%B2%D0%BE%D0%B3%D0%B8-%D1%97%D0%B6%D0%B0%D0%BA.gif'
]
message_text = f"Luftalarm!!!"
message_text2 = "Heben Sie den Luftangriffsalarm auf!"
message_to_unpin = None

async def check_and_alert():
    alert_active = False  # Початковий стан тривоги
    message_to_unpin = None

    while True:
        regions_to_check = ["Львівська область", "Івано-Франківська область"]

        if not alert_active:
            for region in regions_to_check:
                if await is_alert_active_for_region(region):
                    selected_gif = random.choice(gif_list)
                    message = await bot.send_animation(CHAT_ID, selected_gif, caption=message_text)
                    await bot.pin_chat_message(CHAT_ID, message.message_id)
                    alert_active = True
                    logger.info("тривожно")
                    message_to_unpin = message.message_id
                    break
                    
        else:
            still_active = any([await is_alert_active_for_region(region) for region in regions_to_check])
            if not still_active and message_to_unpin:
                await bot.unpin_chat_message(CHAT_ID, message_to_unpin)
                selected_gif2 = random.choice(gif_list2)
                await bot.send_animation(CHAT_ID, selected_gif2, caption=message_text2)
                alert_active = False
                logger.info("тривога на 0")
        
        logger.info("чекаєм")
        await asyncio.sleep(60)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def get_alert_map_screenshot(url, path_to_save_screenshot):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск Chrome у фоновому режимі
    chrome_options.add_argument("--window-size=1920x1080")  # Встановлення розміру вікна

    driver_service = Service(executable_path='D:\!DESKTOPWORKSPACE\originaldotbot\chromedriver.exe')
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    driver.get(url)

    # Чекаємо, поки сторінка повністю завантажиться
    time.sleep(5)

    # Знаходимо елемент мапи (можливо, вам доведеться змінити селектор)
    map_element = driver.find_element(By.ID, "xmlns")  # Змініть "map-id" на ідентифікатор або селектор, який використовується на веб-сайті
    map_element.screenshot(path_to_save_screenshot)

    driver.quit()

# Використовуйте функцію для отримання скріншоту
get_alert_map_screenshot('https://alerts.in.ua/', 'alert_map.png')


@dp.message_handler(commands=['alerts'])
async def send_alert_map(message: types.Message):
    get_alert_map_screenshot('https://alerts.in.ua/', 'alert_map.png')
    await message.answer_photo(photo=open('alert_map.png', 'rb'))

class Parser:
    def _get_data(self, name):
        self.binance_currency_price = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")

    def _get_uah_usdt_data(self):
        self.binance_currency_price = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol=USDTUAH")


class ParserCrypto(Parser):
    def __init__(self):
        self.name = None

    def price(self, flag=True):
        if flag:
            super()._get_data(self.name)
        else:
            super()._get_uah_usdt_data()

    def get_currency_price(self, name):
        self.name = name.upper()
        self.price()
        return self.binance_currency_price.json()['price']

    def get_currency_price_usdt(self):
        self.price(flag=False)
        return self.binance_currency_price.json()['price']
    
parser_crypto = ParserCrypto()
    
@dp.message_handler(commands=['BTC'])
async def send_alert_map(message: types.Message):
    data = parser_crypto.get_currency_price(message.text)
    await message.answer(f"Курс біткоїна  зараз: {float(data)}$")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
