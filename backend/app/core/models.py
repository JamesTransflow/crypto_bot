from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class CoTResponse(BaseModel):
    explanation: str = Field(..., description="解释为何生成这个回答")


class Intention(Enum):
    FIND_CRYPTO_PRICE = "查询虚拟币价格"
    OTHER = "其他"


class IntentionResponse(CoTResponse):
    intention: Intention


class CryptoSource(Enum):
    COINGECKO = "coingecko"
    COINBASE = "coinbase"
    BINANCE = "binance"


class CryptoType(Enum):
    ETHEREUM = "以太坊"
    BITCOIN = "比特币"


class Currency(Enum):
    USDT = "USDT"
    EUR = "EUR"
    USD = "USD"


class CyptoPriceInfo(BaseModel):
    cypto_source: CryptoSource
    cypto_type: CryptoType
    currency: Currency


class CyptoPriceInfoResponse(CoTResponse):
    crypto_price_info: Optional[CyptoPriceInfo]
