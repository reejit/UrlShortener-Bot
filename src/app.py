import logging
from io import BytesIO

import qrcode
from aiogram import Bot, Dispatcher, executor, types

from url_shorteners import TinyUrlShortener
from response_msgs import ResponseMsgs
from config import BotConfig, WebAppConfig

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BotConfig.API_TOKEN)
dp = Dispatcher(bot)

# Setup url shortener
url_shortener = TinyUrlShortener()


async def on_startup(dp):
    """
    Called on bot startup.
    """
    await bot.set_webhook(BotConfig.WEBHOOK_URL)


async def on_shutdown(dp):
    """
    Called on bot shutdown.
    """
    await bot.delete_webhook()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(ResponseMsgs.HELP)


@dp.message_handler(commands=['about', 'contact'])
async def send_contact_details(message: types.Message):
    """
    This handler will be called when user sends `/about` or `/contact` command
    """
    await message.answer(ResponseMsgs.CONTACT)


@dp.message_handler()
async def shorten_url(message: types.Message):
    """
    Creates and sends to the user a shortened url for the given one.
    """
    try:
        res_msg = await url_shortener.shorten(message.text)
        if res_msg is not None:
            inline_keyboard = types.InlineKeyboardMarkup()
            inline_keyboard.add(types.InlineKeyboardButton(
                ResponseMsgs.GET_QR, callback_data=res_msg))
            await message.answer(f"{ResponseMsgs.SHORTENED_URL_READY}\n\n{res_msg}", reply_markup=inline_keyboard)
            return

        res_msg = ResponseMsgs.INTERNAL_ERROR
    except ValueError:
        res_msg = ResponseMsgs.BAD_URL
    except Exception:
        res_msg = ResponseMsgs.INTERNAL_ERROR

    await message.answer(res_msg)


@dp.callback_query_handler()
async def send_qr(callback_query: types.CallbackQuery):
    """
    Creates and sends to the user the QR code of the url in callback query.
    """
    img = qrcode.make(callback_query.data)

    bio = BytesIO()
    bio.name = 'qr.png'
    img.save(bio, 'PNG')
    bio.seek(0)

    img_file = types.InputFile(bio, filename='qr.png')
    await callback_query.answer()
    await bot.send_photo(callback_query.from_user.id, img_file, ResponseMsgs.QR_FOR_IMG.format(url=callback_query.data))


if __name__ == '__main__':
    executor.start_webhook(dp, '/', on_startup=on_startup, on_shutdown=on_shutdown, host='0.0.0.0',
                           port=WebAppConfig.PORT)
