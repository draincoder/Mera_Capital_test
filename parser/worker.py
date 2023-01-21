import asyncio
import logging
from datetime import datetime

import pytz

from database.base import config
from database.crud import db
from parser import Deribit

logger = logging.getLogger(__name__)


async def background_parser():
    try:
        tz = pytz.timezone('Europe/Moscow')  # устанавливаем часовой пояс для смещения
        # открываем контекстный менеджер для работы с API Deribit
        async with Deribit(config.deribit.client_id, config.deribit.client_secret) as der:
            asset_2, index_pnl_2, flag = await get_initial_data()  # определяем изначальные данные
            if not asset_2:
                # если данных в бд нет, то берем за основу текущие
                deposit = await der.get_deposit()
                index = await der.get_index()
                asset_2 = deposit.amount * index.index_price
            # открываем цикл пока установлено сооденение по вебсокету
            while der.websocket.open:
                deposit = await der.get_deposit()  # получаем данные о балансе BTC на нашем счете
                index = await der.get_index()  # получаем цену BTC в USD
                asset_1 = deposit.amount * index.index_price  # стоимость чистых активов в USD на конец периода
                index_pnl_1 = asset_1 / asset_2 * index_pnl_2  # значение индекса на конец периода
                calc_date = int(datetime.now(tz).astimezone(pytz.utc).timestamp() * 1000)  # получаем unix время и передвигаем запятую
                usd_btc = 1 / index.index_price  # курс доллара относительно биткоина в данныи момент времени
                pnl = asset_1 - asset_2 if flag else 0
                flag = True  # переопределяем флаг так как начальные данные уже обработаны
                await db.add_index(calc_date, usd_btc, asset_2, pnl, index_pnl_1)
                index_pnl_2 = index_pnl_1  # значение индекса на начало периода
                asset_2 = asset_1  # стоимость чистых активов в USD на начало периода
                await asyncio.sleep(config.deribit.pause)
    except Exception as e:
        logger.error(e)


async def get_initial_data():
    last_asset = await db.get_last_asset()
    asset_2 = last_asset.asset_value if last_asset else 0  # если в бд уже есть записи, то берем их за основу
    index_pnl_2 = last_asset.index_pnl if last_asset else 1  # если в бд уже есть записи, то берем их за основу
    flag = True if last_asset else False  # флаг для переопределения pnl
    return (asset_2, index_pnl_2, flag)
