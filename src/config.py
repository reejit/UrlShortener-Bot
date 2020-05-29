import os


class BotConfig:
    """ Bot Configuration """

    API_TOKEN = os.environ.get(
        'ApiToken', '')
