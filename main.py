import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext


ACCUWEATHER_API_KEY = 'misfUOaBCUWFbPAdTbqQz7CibMNBBXvn'
TELEGRAM_BOT_TOKEN = '7971969852:AAGQh_PzxlER6XfQCvkcAxit4h0kM9zLhAs'


cities = {
    "Москва": "294021",
    "Санкт-Петербург": "295212",
    "Хабаровск": "293623",
    "Омск": "288563",
    "Курган": "288452",
    "Тюмень": "288596",
    "Владивосток": "290491",
    "Челябинск": "290607",
    "Великий Новгород": "288366",
    "Красноярск": "288620"
}


def get_weather(city_key):
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{city_key}"
    params = {
        'apikey': ACCUWEATHER_API_KEY,
        'language': 'ru',
        'details': 'true'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_text = data[0]['WeatherText']
        temperature = data[0]['Temperature']['Metric']['Value']
        feels_like = data[0]['RealFeelTemperature']['Metric']['Value']
        return f"{weather_text}, Температура: {round(temperature)}, Ощущается как: {round(feels_like)}°C"
    else:
        return "Не удалось получить данные о погоде."


async def start(update: Update, context: CallbackContext) -> None:
    city_names = list(cities.keys())
    keyboard = [[city] for city in city_names]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Привет! Выберите город, чтобы узнать погоду:",
        reply_markup=reply_markup
    )


async def city_weather(update: Update, context: CallbackContext) -> None:
    requested_city = update.message.text.strip()
    if requested_city in cities:
        city_key = cities[requested_city]
        weather_info = get_weather(city_key)
        await update.message.reply_text(f"Погода в {requested_city}:\n{weather_info}")
    else:
        await update.message.reply_text("Пожалуйста, выберите город из списка.")


def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, city_weather))
    application.run_polling()


if __name__ == '__main__':
    main()
