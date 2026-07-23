import math
import yfinance as yf


def clean_value(value):
    """
    Converts NaN/None into None so FastAPI returns proper JSON.
    """

    if value is None:
        return None

    try:
        if math.isnan(value):
            return None
    except Exception:
        pass

    return value


def get_financials(symbol: str):

    try:

        stock = yf.Ticker(symbol)

        info = stock.info

        return {

            "revenue": clean_value(
                info.get("totalRevenue")
            ),

            "net_income": clean_value(
                info.get("netIncomeToCommon")
            ),

            "eps": clean_value(
                info.get("trailingEps")
            ),

            "roe": clean_value(
                info.get("returnOnEquity")
            ),

            "operating_margin": clean_value(
                info.get("operatingMargins")
            ),

            "debt_to_equity": clean_value(
                info.get("debtToEquity")
            ),

            "current_ratio": clean_value(
                info.get("currentRatio")
            ),

            "dividend_yield": clean_value(
                info.get("dividendYield")
            ),

            "market_cap": clean_value(
                info.get("marketCap")
            ),

            "currency": info.get(
                "currency",
                "INR"
            )

        }

    except Exception as e:

        return {

            "error": str(e)

        }
    