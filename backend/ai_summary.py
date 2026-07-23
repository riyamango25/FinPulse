import os
from dotenv import load_dotenv
from google import genai

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_ai_summary(stock: dict) -> str:
    """
    Generates a short, plain-English explanation of a stock
    using its current snapshot data.
    """

    prompt = f"""You are a financial analyst writing for beginners.

Write exactly 3-4 short sentences.

Mention:
- what the company does
- explain what the P/E ratio suggests, but NEVER claim a stock is cheap or expensive unless compared to its industry
- mention one interesting metric from the provided data
- avoid investment advice
- avoid exaggeration
- do not invent facts that are not in the prompt
- keep the tone simple and professional


Company: {stock['company']} ({stock['symbol']})
Sector: {stock['sector']}
Price: ₹{stock['price']}
P/E Ratio: {stock['pe_ratio']}
EPS: {stock['eps']}
Market Cap: ₹{stock['market_cap']}
Day Change: {stock.get('change', 'N/A')}%

Explain what this company does, whether it looks expensive or cheap based on the P/E ratio, and one thing worth knowing about it right now."""

    try:
        response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        )
        return response.text

    except Exception as e:
        return f"AI summary unavailable right now ({str(e)})."