from sqlalchemy import select
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Pnl, Coord
from .models import Index
from .base import async_session


class Database:
    def __init__(self, db_session):
        self.session: AsyncSession = db_session

    async def add_index(self, calc_date: int, usd_btc: float,
                        asset_value: float, pnl: float, index_pnl: float) -> None:
        async with self.session() as session:
            index = Index(calc_date=calc_date, usd_btc=usd_btc, asset_value=asset_value, pnl=pnl, index_pnl=index_pnl)
            session.add(index)
            await session.commit()

    async def get_last_asset(self) -> Index:
        async with self.session() as session:
            last_row = await session.execute(select([Index]).order_by(Index.calc_date.desc()).limit(1))
            return last_row.scalar()

    async def get_statistics(self, date_from: int = None, date_to: int = None) -> Pnl:
        async with self.session() as session:
            if date_from and date_to:
                indexes = await session.execute(select(Index).where(
                    Index.calc_date.between(date_from, date_to)).order_by(Index.calc_date))
            else:
                indexes = await session.execute(select(Index).order_by(Index.calc_date))
            indexes = indexes.scalars().all()
            pnl, pnl_percent, index_pnl = [], [], []
            index_pnl_1 = 1
            count = 0
            for index in indexes:
                percent = 0 if count == 0 else (index.index_pnl / index_pnl_1 - 1) * 100
                pnl.append(Coord(x=index.calc_date, y=index.pnl))
                pnl_percent.append(Coord(x=index.calc_date, y=percent))
                index_pnl.append(Coord(x=index.calc_date, y=index.index_pnl))
                index_pnl_1 = index.index_pnl
                count += 1
            return Pnl(pnl=pnl, pnl_percent=pnl_percent, index_pnl=index_pnl,
                       date_from=str(datetime.fromtimestamp(int(indexes[0].calc_date / 1000))),
                       date_to=str(datetime.fromtimestamp(int(indexes[-1].calc_date / 1000))))


db = Database(async_session)


async def get_db() -> Database:
    return db
