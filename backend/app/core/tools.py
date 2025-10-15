from typing import Optional

import requests

from app.core.models import CyptoPriceInfo, CryptoType


def get_latest_bitcoin_price(
        vs_currency: str = "USD",
        source: str = "coingecko",
        timeout: float = 10.0,
        fallback: bool = True,
) -> float:
    """
    Get the latest Bitcoin (BTC) price.

    Args:
        vs_currency: Target quote currency, e.g. "USD", "EUR", "USDT". Case-insensitive.
        source: Preferred data provider: "coingecko" | "coinbase" | "binance".
        timeout: HTTP request timeout in seconds.
        fallback: If True, automatically try other providers when the preferred one fails.

    Returns:
        Latest price of 1 BTC quoted in `vs_currency`, as float.

    Raises:
        ValueError: If the currency/pair is unsupported or price is missing.
        requests.RequestException: If all providers fail due to network/HTTP issues.

    Examples:
        >>> get_latest_bitcoin_price()
        64231.12
        >>> get_latest_bitcoin_price("EUR", source="coinbase")
        59876.45
        >>> get_latest_bitcoin_price("USDT", source="binance")
        64201.33
    """
    providers = [source]
    if fallback:
        for p in ("coingecko", "coinbase", "binance"):
            if p not in providers:
                providers.append(p)

    last_exception: Optional[Exception] = None

    for provider in providers:
        try:
            if provider == "coingecko":
                url = "https://api.coingecko.com/api/v3/simple/price"
                params = {"ids": "bitcoin", "vs_currencies": vs_currency.lower()}
                r = requests.get(url, params=params, timeout=timeout)
                r.raise_for_status()
                data = r.json()
                price = data.get("bitcoin", {}).get(vs_currency.lower())
                if price is None:
                    raise ValueError(f"Currency '{vs_currency}' not supported by CoinGecko")
                return float(price)

            elif provider == "coinbase":
                pair = f"BTC-{vs_currency.upper()}"
                url = f"https://api.coinbase.com/v2/prices/{pair}/spot"
                r = requests.get(url, timeout=timeout)
                r.raise_for_status()
                data = r.json()
                amount = data.get("data", {}).get("amount")
                if amount is None:
                    raise ValueError(f"Currency '{vs_currency}' not supported by Coinbase")
                return float(amount)

            elif provider == "binance":
                symbol = f"BTC{vs_currency.upper()}"
                url = "https://api.binance.com/api/v3/ticker/price"
                r = requests.get(url, params={"symbol": symbol}, timeout=timeout)
                r.raise_for_status()
                data = r.json()
                price_str = data.get("price")
                if price_str is None:
                    raise ValueError(f"Symbol '{symbol}' not supported by Binance")
                return float(price_str)

            else:
                raise ValueError(f"Unknown provider: {provider}")

        except Exception as exc:
            last_exception = exc
            continue

    if isinstance(last_exception, requests.RequestException):
        raise last_exception
    raise ValueError(f"Unable to fetch BTC price for '{vs_currency}': {last_exception}")


def get_latest_ethereum_price(
        vs_currency: str = "USD",
        source: str = "coingecko",
        timeout: float = 10.0,
        fallback: bool = True,
) -> float:
    """
    Get the latest Ethereum (ETH) price.

    Args:
        vs_currency: Target quote currency, e.g. "USD", "EUR", "USDT". Case-insensitive.
        source: Preferred data provider: "coingecko" | "coinbase" | "binance".
        timeout: HTTP request timeout in seconds.
        fallback: If True, automatically try other providers when the preferred one fails.

    Returns:
        Latest price of 1 ETH quoted in `vs_currency`, as float.

    Raises:
        ValueError: If the currency/pair is unsupported or price is missing.
        requests.RequestException: If all providers fail due to network/HTTP issues.

    Examples:
        >>> get_latest_ethereum_price()
        3245.67
        >>> get_latest_ethereum_price("EUR", source="coinbase")
        2998.12
        >>> get_latest_ethereum_price("USDT", source="binance")
        3240.15
    """
    providers = [source]
    if fallback:
        for p in ("coingecko", "coinbase", "binance"):
            if p not in providers:
                providers.append(p)

    last_exception: Optional[Exception] = None

    for provider in providers:
        try:
            if provider == "coingecko":
                url = "https://api.coingecko.com/api/v3/simple/price"
                params = {"ids": "ethereum", "vs_currencies": vs_currency.lower()}
                r = requests.get(url, params=params, timeout=timeout)
                r.raise_for_status()
                data = r.json()
                price = data.get("ethereum", {}).get(vs_currency.lower())
                if price is None:
                    raise ValueError(f"Currency '{vs_currency}' not supported by CoinGecko")
                return float(price)

            elif provider == "coinbase":
                pair = f"ETH-{vs_currency.upper()}"
                url = f"https://api.coinbase.com/v2/prices/{pair}/spot"
                r = requests.get(url, timeout=timeout)
                r.raise_for_status()
                data = r.json()
                amount = data.get("data", {}).get("amount")
                if amount is None:
                    raise ValueError(f"Currency '{vs_currency}' not supported by Coinbase")
                return float(amount)

            elif provider == "binance":
                symbol = f"ETH{vs_currency.upper()}"
                url = "https://api.binance.com/api/v3/ticker/price"
                r = requests.get(url, params={"symbol": symbol}, timeout=timeout)
                r.raise_for_status()
                data = r.json()
                price_str = data.get("price")
                if price_str is None:
                    raise ValueError(f"Symbol '{symbol}' not supported by Binance")
                return float(price_str)

            else:
                raise ValueError(f"Unknown provider: {provider}")

        except Exception as exc:
            last_exception = exc
            continue

    if isinstance(last_exception, requests.RequestException):
        raise last_exception
    raise ValueError(f"Unable to fetch ETH price for '{vs_currency}': {last_exception}")


def get_latest_price(crypto_price_info: CyptoPriceInfo) -> float:
    if crypto_price_info.cypto_type == CryptoType.BITCOIN:
        return get_latest_bitcoin_price(vs_currency=crypto_price_info.currency.value,
                                        source=crypto_price_info.cypto_source.value)

    return get_latest_ethereum_price(vs_currency=crypto_price_info.currency.value,
                                     source=crypto_price_info.cypto_source.value)


if __name__ == "__main__":
    print(get_latest_bitcoin_price())  # default: USD, CoinGecko, with fallback   # Binance pairs like BTCUSDT
    print(get_latest_ethereum_price())  # default: USD, CoinGecko, with fallback
    print(get_latest_ethereum_price("EUR", "coinbase"))  # specify provider
    print(get_latest_ethereum_price("USDT", "binance"))  # Binance pairs like ETHUSDT
