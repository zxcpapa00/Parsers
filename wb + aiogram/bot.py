import json
from aiogram.utils.markdown import hbold, hlink
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from main import main
from bot_token import bot_token

TOKEN_API = bot_token

bot = Bot(TOKEN_API, parse_mode='html')
dp = Dispatcher(bot)

rkb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
b1 = KeyboardButton('Начать поиск')
rkb.add(b1)


@dp.message_handler(commands='start')
async def start_com(message: types.Message):
    await message.answer('Hello', reply_markup=rkb)


@dp.message_handler(Text(equals='Начать поиск'))
async def search_com(message: types.Message):
    await message.answer('Введите название товара...\n(Название Цена(от)-Цена(до)\n Пример: Пылесос 2000-5000')

    @dp.message_handler()
    async def search_product(message: types.Message):
        await message.answer('Собираю данные...')

        main(message.text)
        try:
            with open('result.json', encoding='utf-8') as file:
                data = json.load(file)

            for item in data:
                card = f'{hlink(item.get("Название модели"), item.get("Ссылка на товар"))}\n' \
                    f'{hbold("Бренд: ")} {item.get("Бренд")}\n' \
                    f'{hbold("Цена со скидкой: ")} {item.get("Цена со скидкой")}\n' \
                    f'{hbold("Цена без скидки: ")} {item.get("Цена без скидки")}\n' \
                    f'{hbold("Размер скидки: ")} {item.get("Размер скидки")}\n' \
                    f'{hbold("Количество звёзд: ")} {item.get("Количество звёзд")}\n' \
                    f'{hbold("Количество отзывов: ")} {item.get("Количество отзывов")}\n'

                await bot.send_photo(chat_id=message.chat.id,
                                     photo=item.get('img'),
                                     caption=card)

        except Exception as ex:
            print(ex)
            await message.answer(text='Ошибка')

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)