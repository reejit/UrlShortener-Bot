from aiogram.utils.emoji import emojize


class ResponseMsgs:
    """Holds all messages that are sent to user by bot."""

    HELP = emojize("Send me a URL, and I'll shorten it. :sunglasses:")

    SHORTENED_URL_READY = emojize(
        "Here is your shortened url :point_down:")
    GET_QR = "Get QR code"
    QR_FOR_IMG = "QR for {url}"

    BAD_URL = emojize("Sorry, that url can't be shortened. :pensive: The url is most likely invalid.")
    INTERNAL_ERROR = emojize(
        "Sorry, something went wrong on our end. :disappointed: :disappointed: Try again later.")
