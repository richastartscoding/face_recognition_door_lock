import requests

BOT_TOKEN = "7780797367:AAF4Rjo2vD894HxUZYIgiTxGARxQJtLTk7w"
CHAT_ID = "1600983377"
message = "🚨 Unauthorized access attempt detected!"

requests.get(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    params={"chat_id": CHAT_ID, "text": message}
)
