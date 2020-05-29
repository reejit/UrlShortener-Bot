from http import HTTPStatus
from typing import Optional

import httpx


class TinyUrlShortener:
    """
    UrlShortener which uses https://tinyurl.com service.
    """

    __URL = 'https://tinyurl.com/api-create.php'

    async def shorten(self, url) -> Optional[str]:
        """
        Shortenes the given url.
        """
        async with httpx.AsyncClient() as client:
            r = await client.get(self.__URL, params={'url': url})

            if r.status_code == HTTPStatus.OK:
                return r.text
            elif r.status_code == HTTPStatus.BAD_REQUEST:
                raise ValueError()
            else:
                return None
