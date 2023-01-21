from sqlalchemy import Column, BigInteger, REAL

from .base import Base


class Index(Base):
    __tablename__ = 'indexes'

    id = Column(BigInteger, primary_key=True)
    calc_date = Column(BigInteger)
    usd_btc = Column(REAL)
    asset_value = Column(REAL)
    pnl = Column(REAL)
    index_pnl = Column(REAL)
