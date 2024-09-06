from aiogram import Bot, Dispatcher, executor, types
from telegram import Update
from alerts_in_ua import Client as AlertsClient
import asyncio
import random
import logging
from aiogram.dispatcher.filters import Text, Regexp
import re
import os

TELEGRAM_TOKEN = '7157883595:AAG9rR9ovslnfeIciHQncSkqvCiSznIjVfI'
 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)


TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Лінка на пост задається тут
post_link = "https://t.me/galizishes/3"

async def get_commentators(post_link: str):
    post_id_data = extract_post_id_from_link(post_link)
    discussion_chat_id = '-2057553857'  # Вкажіть тут ID чату обговорення
    post_id = post_id_data['post_id']
    
    logging.info(f"Extracted chat_id: {discussion_chat_id}, post_id: {post_id}")
    
    commentators = set()
    
    try:
        # Запит на отримання історії повідомлень з чату обговорень
        response = requests.get(f"{TELEGRAM_API_URL}/getUpdates")
        
        data = response.json()
        
        if not data['ok']:
            logging.error("Failed to get chat history from Telegram API")
            return list(commentators)
        
        # Обробляємо отримані повідомлення
        for result in data['result']:
            message = result.get('message')
            if not message:
                continue
            
            # Перевірка, чи є повідомлення відповіддю на пост
            if 'reply_to_message' in message and message['reply_to_message']['message_id'] == post_id:
                commentators.add(message['from']['id'])
                logging.info(f"Added commentator: {message['from']['id']}")
    except Exception as e:
        logging.error(f"Error fetching chat history: {e}")

    return list(commentators)

def extract_post_id_from_link(link: str):
    parts = link.split('/')
    chat_id = f"@{parts[-2]}"
    post_id = int(parts[-1])
    return {'chat_id': chat_id, 'post_id': post_id}

@dp.message_handler(commands=['cum'])
async def test_get_commentators(message: types.Message):
    commentators = await get_commentators(post_link)
    
    if commentators:
        await message.answer(f"Список ID коментаторів: {commentators}")
    else:
        await message.answer("No commentators found or failed to fetch data.")

alerts_client = AlertsClient(token="b24eabefa69df127630fb9d126cd1e9168d17f96ab2203")

# Список фраз для випадкового вибору
phrases_viktor = [
    "ок. стулись.",
    "ого, похуй",
    "ок.",
    "ти вже заїбав",
    "зрозуміло.",
    "яка корисна інформація. іду попісяю",
    "іди нахуй, заїбав",
    "о ні, всім знову похуй",
    "тримай в курсі",
    "добре, закрийся нахуй",
    "ого, іди нахуй",
    "ого, іди вбийся",
    "ого, соси хуй",
    "та поїбати всім",
    "не займайся хуйньою, шиз",
    "тобі пиздак стулиться вже?",
    "Тобі самому ще не набридло?",
    "Та коли ти стулишся?",
    "бидлу ще не набридло?",
 #   "що якщо бога нема?",
  #  "бога нема, заїбав",
   # "бога нема",
    "бачу ти любиш товктися в сраку",
    "всім похуй на тебе",
    "ти клінічний шизофренік",
    "іди лічися",
    "іди ся вбий",
    "стули пиздак бидло",
    "яке ти душне",
    "відкрию вікно.",
    "ти коли-небудь єбло стуляєш?",
    "тобі треба відрізати язик та руки.",
    "тебе розіп'яти?",
    "концтабір чекає на тебе. і не як на працівника",
    "я зараз вириватиму тобі зуби пласкогубцями",
    "як шкода що ти ше не здох",
    "нахуй ти дихаєш",
    "іди вішайся",
    "іди ся вішай",
    "іди втопися",
    "зламати тобі череп?",
   # "віддай нарешті душу богові",
   # "чого ти щен не вмер за ісуса?",
    "ти бевзю йобаний",
    "бездар говорить",
    "пиздак тобі так і не стуляється",
    "заїбеш",
    "чому ти не можеш  бути нормальним?",
    "тебе в дитинстві впустили?",
    "лоба розбити?",
    "стули рило",
    "хрюк хрюк",
    "польське радіо",
    "пук пук",
    "сруньк сруньк",
    "нагадування: всім поїбати абсолютно",
    "who cares",
    "who asked",
    "who needs you opinion Seisse",
    "zamknie pizde kurwo",
    "стулися вже",
    "коли ти вже наговоришся",
    "хочу щоб ТВОЄ ЄБАЛО І РУКИ АТРОФУВАЛИСЯ НАХУЙ",
    "видали блять телеграм",
    "викинь гаджети всі",
    "нахуй тобі то життя?",
    "бажаю тобі замкнути свій пиздак на віки вічні",
    "ти не виліковний",
    "тут курва вже аптечка не поможе",
    "всі просто вдають, що дружать з тобою",
    "ми спілкуємося з тобою тільки з міркувань етикету і жалості",
    "проламати череп?",
    "яке ти хворе блять",
    "який же ти клоун",
    "але ти клоун попояний",
    "попаяного довбойоба спитати забули",
    "тебе хтось питав?",
    "Тьфу. Дьяволе, відчіписі",
    "йди нахуй, чорт",
    "йди далі слугуй свому сатані",
    "втопися, йобаний грішник",
    "як будеш іти по гриби, спробуй бліду поганку",
    "вау, похуй",
    "хочеш вибухнути? нюхай балон",
    "з кожним повідомленням твоє iq падає",
    "захотілося помацати м'які стіни?",
    "стінгер тобі в сраку",
    "лайноїд, стулись вже",
    "тебе ніхто не питав, уйобіще",
    "єбать ти смішний, а тепер йди вішайся",
    "ти лопух, не більше",
    "віддай ящик горілки",
    "лох"
]


TARGET_USERNAME = 'o_otaku'
# Обробник для повідомлень від конкретного користувача
@dp.message_handler(lambda message: message.from_user.username == TARGET_USERNAME)
async def reply_to_viktor(message: types.Message):
    response = random.choice(phrases_viktor)
    await message.reply(response)
    
# Alerts
###############################################################################################
async def is_alert_active_for_region(region_name: str) -> bool:\

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

async def on_startup(dp):
    asyncio.create_task(check_and_alert())
    
async def check_and_alert():
    alert_active = False  # Початковий стан тривоги

    while True:
        regions_to_check = ["Львівська область", "Івано-Франківська область"]

        if not alert_active:
            for region in regions_to_check:

                if await is_alert_active_for_region(region):
                    CHAT_ID = '-1002057553857'
                    selected_gif = random.choice(gif_list)
                    message = await bot.send_animation(CHAT_ID, selected_gif, caption=message_text)
                    await bot.pin_chat_message(CHAT_ID, message.message_id, disable_notification=False)
                    alert_active = True  # Змінюємо стан тривоги
                    logger.info("тривожно")
                    message_to_unpin = message.message_id
                    break  # Перериваємо цикл, оскільки тривога вже активована
                    
                else:
                    logger.info(region)
                    logger.info("спокійно")
                    logger.info(" ")
                    
                    
        else:
            # Тривога була активована, чекаємо на її відбій
            still_active = any([await is_alert_active_for_region(region) for region in regions_to_check])
            if not still_active:
                selected_gif2 = random.choice(gif_list2)
                await bot.delete_message(CHAT_ID, message_to_unpin)
                await bot.send_animation(CHAT_ID, selected_gif2, caption=message_text2)
                alert_active = False  # Відновлюємо початковий стан тривоги
                logger.info("тривога на 0")
        logger.info("чекаєм")
        await asyncio.sleep(45)
### Screen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time

# Глобальні змінні для збереження стану браузера
driver = None
theme_switched = False

def initialize_driver(executable_path):
    global driver
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    try:
        service = ChromeService(executable_path=executable_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print("Failed to initialize the Chrome driver:", str(e))
        driver = None

def get_alert_map_screenshot(url, path_to_save_screenshot):
    global driver, theme_switched

    if driver is None:
        initialize_driver('D:\\DESKTOPWORKSPACE\\originaldotbot\\chromedriver.exe')
        if driver is None:
            return  # Вихід, якщо драйвер не вдалося ініціалізувати

    try:
        if theme_switched == False :
            driver.get(url)
            time.sleep(0.4)  # Збільшено час очікування для завантаження сторінки

            # Натиснути кнопку перемикання теми лише один раз
            try:
                toggle_theme_button = driver.find_element(By.CSS_SELECTOR, "modes-button non-compact")
                toggle_theme_button.click()
                time.sleep(0.4)  # Збільшено час очікування для застосування теми
                theme_switched = True
            except Exception as e:
                print("Failed to switch theme:", str(e))

        # Зберегти скріншот
        driver.save_screenshot(path_to_save_screenshot)
    except Exception as e:
        print("An error occurred:", str(e))
        driver.quit()
        driver = None  # Перевстановити драйвер для наступного виклику, якщо сталася помилка

# Виклик функції для першого знімка
get_alert_map_screenshot('https://alerts.in.ua/', 'alert_map_initial.png')



from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time

# Глобальні змінні для збереження стану браузера
cryptobubble_driver = None

def initialize_cryptobubble_driver(executable_path):
    global cryptobubble_driver
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    try:
        service = ChromeService(executable_path=executable_path)
        cryptobubble_driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print("Failed to initialize the Chrome driver:", str(e))
        cryptobubble_driver = None

def get_cryptobubble_screenshot(url, path_to_save_screenshot):
    global cryptobubble_driver

    if cryptobubble_driver is None:
        initialize_cryptobubble_driver('D:\\DESKTOPWORKSPACE\\originaldotbot\\chromedriver.exe')
        if cryptobubble_driver is None:
            return  # Вихід, якщо драйвер не вдалося ініціалізувати

    try:
        if not cryptobubble_driver.current_url.startswith(url):
            cryptobubble_driver.get(url)
            time.sleep(3)  # Додано час очікування для завантаження сторінки

        # Зберегти скріншот
        cryptobubble_driver.save_screenshot(path_to_save_screenshot)
    except Exception as e:
        print("An error occurred:", str(e))
        cryptobubble_driver.quit()
        cryptobubble_driver = None  # Перевстановити драйвер для наступного виклику, якщо сталася помилка

# Виклик функції для першого знімка
get_cryptobubble_screenshot('https://cryptobubble.com/', 'cryptobubble_initial.png')


@dp.message_handler(commands=['cryptobubble'])
async def send_crypto_bubble(message: types.Message):
    screenshot_path = 'crypto_bubble.png'
    get_cryptobubble_screenshot('https://cryptobubbles.net/', screenshot_path)
    with open(screenshot_path, 'rb') as photo:
        await message.reply_photo(photo=photo, caption="крипта то скам📊")

@dp.message_handler(commands=['alerts'])
async def send_alert_map(message: types.Message):
    get_alert_map_screenshot('https://alerts.in.ua/', 'alert_map.png')
    await message.reply_photo(photo=open('alert_map.png', 'rb'), caption="📍 Aktuelle Karte der Luftwarnungen")

@dp.message_handler(Text(equals='тривожно', ignore_case=True))
async def send_alert_prikol(message: types.Message):
    await message.reply("хуйожно" )
    get_alert_map_screenshot('https://alerts.in.ua/', 'alert_map.png')
    await message.reply_photo(photo=open('alert_map.png', 'rb'), caption="не тривожся")

@dp.message_handler(Text(equals='тривога', ignore_case=True))
async def send_alert_prikol(message: types.Message):
    await message.reply("хуйога" )
    get_alert_map_screenshot('https://alerts.xn.ua/', 'alert_map.png')
    await message.reply_photo(photo=open('alext_map.png', 'rb'), caption="не тривожся")

# Crypto
#############################################x######################################################
import requests
from aiogram import types, Dispatcher

class CryptoParser:
    def __init__(self):
        self.api_url = "https://api.binance.com/api/v3/ticker/price"
        self.symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "USDTUAH"]
    
    def get_prices(self):
        prices = {}
        for symbol in self.symbols:
            response = requests.get(f"{self.api_url}?symbol={symbol}")
            if response.status_code == 200:
                data = response.json()
                prices[data['symbol']] = data['price']
        return prices

parser_crypto = CryptoParser()

async def send_crypto_prices(message: types.Message, prices):
    btc_price = float(prices["BTCUSDT"])
    eth_price = float(prices["ETHUSDT"])
    bnb_price = float(prices["BNBUSDT"])
    uah_price = float(prices["USDTUAH"])
    response_message = (
        f"💰 BTC Preise: {btc_price}$\n"
        f"💰 ETH Preise: {eth_price}$\n"
        f"💰 BNB Preise: {bnb_price}$\n"
        f"💸 Курс долара: {uah_price} грн"
    )
    # Using reply() to respond directly to the message
    await message.reply(response_message)

def crypto_keyword_filter(message: types.Message):
    phrases = ["тримай в курсі"]
    keywords = ["курс", "біток", "ефірум", "біткоїн"]

    message_text = message.text.lower() if message.text else ""

    if any(phrase in message_text for phrase in phrases):
        return True

    message_words = message_text.split()
    return any(keyword in message_words for keyword in keywords)

@dp.message_handler(lambda message: crypto_keyword_filter(message))
async def handle_keyword_message(message: types.Message):
    prices = parser_crypto.get_prices()
    await send_crypto_prices(message, prices)

@dp.message_handler(commands=['crypto'])
async def command_crypto(message: types.Message):
    prices = parser_crypto.get_prices()
    await send_crypto_prices(message, prices)
#
##########################################################################################
#test
@dp.message_handler(commands=['test'])
async def send_test(message: types.Message):
    #test_message = await bot.send_message(CHAT_ID, "test pin")
    #await bot.pin_chat_message(CHAT_ID, test_message.message_id)
    #await asyncio.sleep(3)
    #await bot.delete_message(CHAT_ID, test_message.message_id)
    #CHAT_ID = message.chat.id
    await message.reply("хуєст.\nFick dich der Wichser Verdammte Scheisse")

#msg filter reply
##########################################################################################

async def keyword_response(message: types.Message, response_texts):
    """Sends a random response to the message."""
    response_text = random.choice(response_texts)
    await message.reply(response_text)

def contains_keywords(message: types.Message, keywords):
    """Checks if the message text contains any of the keywords."""
    text = message.text.lower() if message.text else ""
    return any(keyword.lower() in text.split() for keyword in keywords)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(
        lambda message: keyword_response(message, ["Hiel Hitler!"]),
        lambda message: contains_keywords(message, ["здрастуй", 'хелоу']),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["Sieg Heil!"]),
        lambda message: contains_keywords(message, ["Hiel Hitler!", "heil hitler"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["Привіт", "Бувай", "Йди ся вішай", "Hiel Hitler!"]),
        lambda message: contains_keywords(message, ["Привіт"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["блять", "ні блять, сирник"]),
        lambda message: contains_keywords(message, ["блін"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["хуяміст"]),
        lambda message: contains_keywords(message, ["програміст"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["ₘаксим"]),
        lambda message: contains_keywords(message, ["Максим"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["блін", "сам в ахуї", "матюки то гріх", "чіл, життя - хуйня", "давай не матюкатися", "пиздо курво шмато Halt die Klappe", "Halt deinen Mund, Fotze", "почни цінувати життя"]),
        lambda message: contains_keywords(message, []),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["Героям Слава!"]),
        lambda message: contains_keywords(message, ["Слава Україні!", "слава Україні"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["Смерть Ворогам!"]),
        lambda message: contains_keywords(message, ["слава нації"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["put in ass", "хуйло", "здох", "коли то хуйло вже здохне"]),
        lambda message: contains_keywords(message, ["путін"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["Смерть Ворогам!"]),
        lambda message: contains_keywords(message, ["слава нації"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["давай не матюкатися", "пиздо курво шмато Halt die Klappe", "Halt deinen Mund, Fotze"]),
        lambda message: contains_keywords(message, []),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["пизда"]),
        lambda message: contains_keywords(message, ["хуй"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["хуй"]),
        lambda message: contains_keywords(message, ["пизда"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["залупа хуйні", "the loopa"]),
        lambda message: contains_keywords(message, ["залупа"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["звертайся.", "Скажи дякую нашому фюреру"]),
        lambda message: contains_keywords(message, ["дякую"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["тобі репресій захотілося?", "будь дружелюбним і вибачайся", "давай без агресій, а то в концтабір попиздуєш"]),
        lambda message: contains_keywords(message, ["іди нахуй", "йди нахуй", "йди нах", "іди нах"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["та що тут доброго...", "добре, добре"]),
        lambda message: contains_keywords(message, ["добре"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["добре", "вибачення прийняті", "ладно, в концтабір не поїдеш", "проси пробачення у фюрера."]),
        lambda message: contains_keywords(message, ["вибач"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["нахуй всіх євреїв", "спалити нахуй", "всіх євреїв до газової камери", 
                                                   "Гена Цидєвреїв."]),
        lambda message: contains_keywords(message, ["єврей", "жид", "іудей", "jewish", "єврея", "євре", "євреїв", "євреї"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["цист."]),
        lambda message: contains_keywords(message, ["Яна"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["лава."]),
        lambda message: contains_keywords(message, ["Яша"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["хуєст..."]),
        lambda message: contains_keywords(message, ["тест"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["-", "±"]),
        lambda message: contains_keywords(message, ["+"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["давно", "так", "вони кончені"]),
        lambda message: contains_keywords(message, ["йобнулись", "йобнулис"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["давно", "так", "він кончений."]),
        lambda message: contains_keywords(message, ["йобнувся", "йобнувсь"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["цидєвреїв", "цидрусні" "Гена Цидєвреїв", "Гена Цидрусні"]),
        lambda message: contains_keywords(message, ["гена"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["пиздуєш в концтабір.", "вибачайся.", "@originaldotboi, в газову камеру його", "йди нахуй"]),
        lambda message: contains_keywords(message, ["хуюрер", "хуйюрер", "хуюреру", "хуйюреру"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["Шановна Служба безпеки України та голова СБ України Малюк Василь Васильович, \n Я не маю відношення до цього чату і був доданий сюди без своєї згоди. Я не погоджуюся з усіма думками, які висловленні в цьому чаті, а мої повідомлення були написані без моєї згоди."]),
        lambda message: contains_keywords(message, ["нацист"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["і не збирався.", "не дякую"]),
        lambda message: contains_keywords(message, ["не дякуй"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["хуютка"]),
        lambda message: contains_keywords(message, ["шютка", "щютка"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["хуєльник"]),
        lambda message: contains_keywords(message, ["мельник"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["хуюльник"]),
        lambda message: contains_keywords(message, ["мульник"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["як нахуя?", "щоб ти спитав."]),
        lambda message: contains_keywords(message, ["нахуя"]),
        content_types=['text']
    )
    dp.register_message_handler(
        lambda message: keyword_response(message, ["Sehr geehrter Bundessicherheitsdienst und Herr Direktor Thomas Haldenwang,\nIch habe mit diesem Chat nichts zu tun und wurde ohne meine Zustimmung hier hinzugefügt. Ich bin nicht mit allen in diesem Chat geäußerten Meinungen einverstanden und meine Beiträge wurden ohne meine Zustimmung verfasst."]),
        lambda message: contains_keywords(message, ["nazi"]),
        content_types=['text']
    )

register_handlers(dp)


@dp.message_handler(Regexp(r'(?i)^(олег|олежик|олько|o_otaku|петрушка|oleg|olegg|oleggg|oleh|olko|@o_otaku|oleh)$'))
async def oleg(message: types.Message):
    await message.reply("@o_otaku йде нахуй" )

#langdetect
#################################################

#anekdot
#################################################

anecdotes = [
   "Чоловік з сином біля могили тещі. Хлопчик запитує:"
"- Тато, а навіщо на могилі бабусі така велика плита?"
"- Щоб вона не вилізла, синку",

"Three tomatoes are walking down the street, poppa tomato, momma tomato and baby tomato. Baby tomato starts lagging behind and poppa tomato gets really angry. Goes back and squishes him and says, “Ketchup.”",
"Три помідорчики йдуть вулицею: тато, мама і маленький помідор. Малий помідор починає відставати, і тато дуже розсердився. Повертається назад, давить його і каже: Кетчуп.",

"Як називається американо без води?"
"Як?"
"Африкано.",

"Яка рiзниця мiж Санта Клаусом та євреєм? Напрямком у каміні",
"чому гітлер не став художником?\n війна почалась",

"Заходить папуга з чорношкірим до бару,бармен питає — Де ти його купив? Папуга каже — На базарі",

"Що треба кинути у воду потопаючому москалю?"
"-Його сім'ю", 

"Як можна підчипити еврейську дівчину? Совком",

"їбе ейнштейн ньютона в сраку, ньютон малює під собою квадрат і починає сміятись, ейнштейн питає:\n -шо смішного я ж тебе прям в сраку \n -ні ти не мене трахаєш, а паскаля",


"Їбе батько сліпого сина: – Бачиш, синку, добре, що мама померла. – Ні, тату, не бачу...",

"У мюллера і штірліца був танк. Вони каталися на ньому по черзі. Черга була невдоволена, але не розходилася",

"В єврейському гетто есесівець помітив дівчинку з нашитою шестиконечною зіркою:\n О, дівчинко, у тебе зірка - то ти єврейка?\n Ні, блядь, техаський рейнджер!",

"Зворотній екзорцизм - це коли диявол просить священника вийти з хлопчика.",

"Заходить сліпий в бар і каже: всім привіт, кого не бачив",

"заходить сліпий в бар і каже: заїбали з цим анекдотом. олег йди вбийся",

"Бухі Штірліц і Мюллер вийшли з бару."
"- Давайте знімемо дівчаток, - запропонував Штірліц."
"- У вас дуже добре серце, - відповів Мюллер. - Але нехай таки повисять до ранку.",

"Штірлицю за комір упала гусениця.  Десь вибухнув танк,  - подумав Штірліц.",

"Лекція"
"-Професоре, який найкращий метод контрацепції?"
"-Добре заварений зелений чай."
"-А, до чи після?"
"-Замість."

]

@dp.message_handler(commands=['anekdot'])
async def send_anekdot(message: types.Message):
    anekdot = random.choice(anecdotes)
    await message.reply(anekdot)

def check_keywords(message: types.Message):
    text = message.text.lower()
    keywords = ['порш', 'порше', 'porsh', 'porshe', 'porsche']
    return any(keyword in text for keyword in keywords)
@dp.message_handler(lambda message: check_keywords(message))
async def send_video_message(message: types.Message):
    local_video_path = r'D:\DESKTOPWORKSPACE\originaldotbot\video_2024-04-17_18-22-21.mp4' 
    with open(local_video_path, 'rb') as video:
        await message.reply_video(video=video, caption="glückliche Nation")

#help
##################################################################
 
@dp.message_handler(commands=['start', 'help'])
async def send_alert_map(message: types.Message):
    response_text = (
        "♟ Dieser Bot kann das: \n"
        "/alerts - Відправляє карту актуальних тривог\n"
        "/crypto - Відправляє курси валют\n"
        "/cryptobubble - Відправляє веселі бульки\n"
        "/test - Тестова команда, але краще не відправляй її\n"
        "/anekdot - Відправляє анекдоти"
        "\n По дефолту відбувається хуєсошення віктора релігійного фанатика"
        "\n\nТакож відбувається постійний моніторинг тривог ✨"
        "\nПоводься чемно, і не поїдеш в концтабір."
    )
    photo_url = 'https://techpost.io/uploads/big-brother.jpg'
    await message.reply_photo(photo = photo_url, caption = response_text)
#context replies
###################################################################################
@dp.message_handler()
async def handle_all_messages(message: types.Message):
    async def send_kvas_photo():
        if re.search(r'\bквас\b', message.text, re.IGNORECASE):
            kvas_photo_url = "https://content.rozetka.com.ua/goods/images/original/325295910.jpg"
            await message.reply_photo(kvas_photo_url, caption="Квас Тарас Хлібний")
        if re.search(r'\bквасу\b', message.text, re.IGNORECASE):
            kvas_photo_url = "https://content.rozetka.com.ua/goods/images/original/325295910.jpg"
            await message.reply_photo(kvas_photo_url, caption="Квас Тарас Хлібний")
    await send_kvas_photo()


#Test

# engine

##############################################################################
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

