with open('routers/chat.py', 'w') as f:
    f.write("""from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import httpx

router = APIRouter()

GEMINI_API_KEY = "paste-your-key-here"

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@router.post("/chat")
async def chat(req: ChatRequest):
    history = []
    for m in req.messages:
        role = "user" if m.role == "user" else "model"
        history.append({"role": role, "parts": [{"text": m.content}]})

    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}",
            json={
                "system_instruction": {
                    "parts": [{"text": "You are Pollin AI Assistant, a friendly stock market education assistant built into the Pollin AI app similar to Groww. Help users understand stock market concepts, chart reading, market terminology, NIFTY, SENSEX, investment basics, and how to interpret AI forecasts. Keep responses concise, friendly, use simple language and emojis. Use bullet points for lists. Never give specific buy/sell advice."}]
                },
                "contents": history,
            },
            timeout=30.0,
        )
        data = res.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"reply": reply}
""")

print("chat.py created successfully in routers folder!")
