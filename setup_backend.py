import os

print("Creating Pollin AI backend files...")

os.makedirs("routers", exist_ok=True)

# ── __init__.py ──────────────────────────────────────────────
with open("routers/__init__.py", "w") as f:
    f.write("")

# ── main.py ──────────────────────────────────────────────────
with open("main.py", "w") as f:
    f.write("""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import stocks, predict, sentiment

app = FastAPI(title="Pollin AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks.router,   prefix="/api")
app.include_router(predict.router,  prefix="/api")
app.include_router(sentiment.router,prefix="/api")

@app.get("/")
def home():
    return {"message": "Pollin AI is running!"}
""")

# ── routers/stocks.py ─────────────────────────────────────────
with open("routers/stocks.py", "w") as f:
    f.write("""from fastapi import APIRouter, HTTPException
import yfinance as yf

router = APIRouter()

@router.get("/stock/{symbol}")
def get_stock(symbol: str, period: str = "6mo"):
    try:
        ticker = yf.Ticker(symbol.upper())
        info   = ticker.info
        hist   = ticker.history(period=period)
        if hist.empty:
            raise HTTPException(status_code=404, detail="No data found")
        history = []
        for date, row in hist.iterrows():
            history.append({
                "date":   date.strftime("%Y-%m-%d"),
                "open":   round(row["Open"],  2),
                "high":   round(row["High"],  2),
                "low":    round(row["Low"],   2),
                "close":  round(row["Close"], 2),
                "volume": int(row["Volume"]),
            })
        return {
            "symbol":        symbol.upper(),
            "name":          info.get("longName", symbol),
            "current_price": info.get("currentPrice") or history[-1]["close"],
            "currency":      info.get("currency", "USD"),
            "sector":        info.get("sector", "N/A"),
            "market_cap":    info.get("marketCap", 0),
            "pe_ratio":      info.get("trailingPE", 0),
            "52w_high":      info.get("fiftyTwoWeekHigh", 0),
            "52w_low":       info.get("fiftyTwoWeekLow",  0),
            "history":       history,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/{query}")
def search_stocks(query: str):
    popular = [
        {"symbol": "AAPL",          "name": "Apple Inc."},
        {"symbol": "GOOGL",         "name": "Alphabet Inc."},
        {"symbol": "MSFT",          "name": "Microsoft Corp."},
        {"symbol": "AMZN",          "name": "Amazon.com Inc."},
        {"symbol": "TSLA",          "name": "Tesla Inc."},
        {"symbol": "META",          "name": "Meta Platforms"},
        {"symbol": "NVDA",          "name": "NVIDIA Corp."},
        {"symbol": "NFLX",          "name": "Netflix Inc."},
        {"symbol": "RELIANCE.NS",   "name": "Reliance Industries"},
        {"symbol": "TCS.NS",        "name": "Tata Consultancy Services"},
        {"symbol": "INFY.NS",       "name": "Infosys Ltd."},
        {"symbol": "HDFCBANK.NS",   "name": "HDFC Bank"},
        {"symbol": "WIPRO.NS",      "name": "Wipro Ltd."},
        {"symbol": "BAJFINANCE.NS", "name": "Bajaj Finance"},
    ]
    q = query.lower()
    return [s for s in popular if q in s["symbol"].lower() or q in s["name"].lower()][:6]
""")

# ── routers/predict.py ────────────────────────────────────────
with open("routers/predict.py", "w") as f:
    f.write("""from fastapi import APIRouter, HTTPException
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from datetime import timedelta

router = APIRouter()

@router.get("/predict/{symbol}")
def predict_price(symbol: str):
    try:
        ticker = yf.Ticker(symbol.upper())
        hist   = ticker.history(period="6mo")
        if hist.empty or len(hist) < 30:
            raise HTTPException(status_code=404, detail="Not enough data")
        closes = hist["Close"].values.reshape(-1, 1)
        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(closes)
        WINDOW = 20
        X, y = [], []
        for i in range(WINDOW, len(scaled)):
            X.append(scaled[i - WINDOW:i].flatten())
            y.append(scaled[i][0])
        X, y = np.array(X), np.array(y)
        model = LinearRegression()
        model.fit(X, y)
        predictions = []
        window    = scaled[-WINDOW:].flatten().tolist()
        last_date = hist.index[-1]
        for i in range(7):
            x_in       = np.array(window[-WINDOW:]).reshape(1, -1)
            next_sc    = model.predict(x_in)[0]
            next_price = scaler.inverse_transform([[next_sc]])[0][0]
            next_date  = last_date + timedelta(days=i + 1)
            while next_date.weekday() >= 5:
                next_date += timedelta(days=1)
            predictions.append({"date": next_date.strftime("%Y-%m-%d"), "price": round(float(next_price), 2)})
            window.append(next_sc)
        r2           = model.score(X, y)
        confidence   = max(0, min(100, round(r2 * 100, 1)))
        current      = float(scaler.inverse_transform([[scaled[-1][0]]])[0][0])
        change_pct   = round(((predictions[-1]["price"] - current) / current) * 100, 2)
        return {
            "symbol":        symbol.upper(),
            "current_price": round(current, 2),
            "predictions":   predictions,
            "confidence":    confidence,
            "change_7d_pct": change_pct,
            "trend":         "bullish" if change_pct > 0 else "bearish",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
""")

# ── routers/sentiment.py ──────────────────────────────────────
with open("routers/sentiment.py", "w") as f:
    f.write("""from fastapi import APIRouter, HTTPException
import yfinance as yf
from textblob import TextBlob

router = APIRouter()

def analyze(text):
    p     = TextBlob(text).sentiment.polarity
    label = "Positive" if p > 0.1 else "Negative" if p < -0.1 else "Neutral"
    color = "green"    if p > 0.1 else "red"      if p < -0.1 else "gray"
    return {"polarity": round(p, 3), "label": label, "color": color}

@router.get("/sentiment/{symbol}")
def get_sentiment(symbol: str):
    try:
        ticker   = yf.Ticker(symbol.upper())
        news     = ticker.news
        if not news:
            return {"symbol": symbol.upper(), "overall_score": 0,
                    "overall_label": "Neutral", "overall_color": "gray", "articles": []}
        articles = []
        for item in news[:10]:
            content   = item.get("content", {})
            title     = content.get("title")   or item.get("title",   "No title")
            summary   = content.get("summary") or item.get("summary", "")
            url       = (content.get("canonicalUrl") or {}).get("url") or item.get("link", "#")
            publisher = (content.get("provider")     or {}).get("displayName") or item.get("publisher", "")
            sentiment = analyze(f"{title}. {summary}")
            articles.append({"title": title, "summary": summary[:200],
                             "url": url, "publisher": publisher, **sentiment})
        avg   = sum(a["polarity"] for a in articles) / len(articles) if articles else 0
        label = "Positive" if avg > 0.1 else "Negative" if avg < -0.1 else "Neutral"
        color = "green"    if avg > 0.1 else "red"      if avg < -0.1 else "gray"
        return {"symbol": symbol.upper(), "overall_score": round(avg, 3),
                "overall_label": label, "overall_color": color, "articles": articles}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
""")

print("")
print("All files created successfully!")
print("")
print("Files created:")
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d != "venv" and not d.startswith(".")]
    for file in files:
        print(" ", os.path.join(root, file))
print("")
print("Now run:  uvicorn main:app --reload")
