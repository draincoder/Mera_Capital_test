import json
import logging

import websockets
from websockets import connect

from parser.models import Balance, Index

logger = logging.getLogger(__name__)


class Deribit:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = None
        self.access_token = None

    # Магический метод для открытия контекстного менеджера
    async def __aenter__(self):
        self.url = 'wss://test.deribit.com/ws/api/v2'
        self._conn = connect(self.url)
        self.websocket = await self._conn.__aenter__()
        await self.auth()
        return self

    # Магический метод для закрытия контекстного менеджера + logout
    async def __aexit__(self, *args, **kwargs):
        try:
            msg = {"jsonrpc": "2.0",
                   "method": "private/logout",
                   "params": {
                       "access_token": self.access_token,
                       "invalidate_token": True}}
            await self.websocket.send(json.dumps(msg))
            await self._conn.__aexit__(*args, **kwargs)
        except websockets.ConnectionClosed as e:
            print(f'Terminated', e)

    # Авторизация
    async def auth(self) -> None:
        try:
            msg = {"jsonrpc": "2.0",
                   "method": "public/auth",
                   "params": {
                       "grant_type": "client_credentials",
                       "client_id": self.client_id,
                       "client_secret": self.client_secret}}
            await self.websocket.send(json.dumps(msg))
            answer = json.loads(await self.websocket.recv())
            self.access_token = answer.get('result').get('access_token')
            self.refresh_token = answer.get('result').get('refresh_token')
            logger.info('Авторизация прошла успешно')
        except Exception as e:
            logger.error(f'Произошла ошибка при аутентефикации: {e}')

    # Получить баланс
    async def get_deposit(self) -> Balance:
        try:
            msg = {"jsonrpc": "2.0",
                   "method": "private/get_account_summary",
                   "params": {
                       "access_token": self.access_token,
                       "currency": "BTC",
                       "extended": True}}
            await self.websocket.send(json.dumps(msg))
            answer = json.loads(await self.websocket.recv())
            return Balance(currency='BTC', amount=answer.get('result').get('available_funds'),
                           time_answer=answer.get('usOut'))
        except Exception as e:
            logger.error(e)
            await self.refresh()

    # Получить стоимость биткоина в долларах
    async def get_index(self) -> Index:
        try:
            msg = {"jsonrpc": "2.0",
                   "method": "public/get_index_price",
                   "params": {
                       "index_name": "btc_usd"}}
            await self.websocket.send(json.dumps(msg))
            answer = json.loads(await self.websocket.recv())
            return Index(currency_pair='BTC_USD', index_price=answer.get('result').get('index_price'),
                         estimated_price=answer.get('result').get('estimated_delivery_price'),
                         time_answer=answer.get('usOut'))
        except Exception as e:
            logger.error(e)
            await self.refresh()

    # Обновить токен
    async def refresh(self) -> None:
        try:
            msg = {"jsonrpc": "2.0",
                   "method": "public/exchange_token",
                   "params": {
                       "refresh_token": self.refresh_token,
                       "subject_id": 10}}
            await self.websocket.send(json.dumps(msg))
            answer = json.loads(await self.websocket.recv())
            self.access_token = answer.get('result').get('access_token')
            self.refresh_token = answer.get('result').get('refresh_token')
            logger.info('Токен успешно сменен')
        except Exception as e:
            logger.error(f'Произошла ошибка при смене токена: {e}')
