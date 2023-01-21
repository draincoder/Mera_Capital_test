from pydantic import BaseModel


class Balance(BaseModel):
    currency: str
    amount: float
    time_answer: int


class Index(BaseModel):
    currency_pair: str
    index_price: float
    estimated_price: float
    time_answer: int
