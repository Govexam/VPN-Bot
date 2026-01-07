import requests, pandas as pd, io, asyncio, os
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
BLOG_URL = "https://yourblog.blogspot.com" # Apna Blogger link yahan dalein

async def send_vpn_update():
    print("Fetching servers...")
    url = "https://www.vpngate.net/api/iphone/"
    response = requests.get(url)
    data = "\n".join(response.text.split('\n')[1:-2]).replace('*', '')
    df = pd.read_csv(io.StringIO(data))
    df['Ping'] = pd.to_numeric(df['Ping'], errors='coerce')
    df = df.dropna(subset=['Ping']).sort_values(by='Ping')
    
    top_servers = df.head(8)
    message = "🛡️ *MISSION MERIT VPN LIVE* 🛡️\n━━━━━━━━━━━━━━━━━━\n\n"
    for _, row in top_servers.iterrows():
        icon = "🟢" if row['Ping'] < 60 else "🟡"
        message += f"{icon} *Country:* {row['CountryLong']}\n🌐 *IP:* `{row['IP']}`\n⚡ *Ping:* {int(row['Ping'])}ms\n━━━━━━━━━━━━━━━━━━\n"
    
    message += "\n👤 *User:* `vpn` | 🔑 *Pass:* `vpn` \n🔄 _Updated every hour_"

    # Buttons for professional look
    keyboard = [
        [InlineKeyboardButton("📖 How to Connect (Guide)", url=BLOG_URL)],
        [InlineKeyboardButton("💬 Contact Support", url="https://t.me/LUCIFERKAKA")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown', reply_markup=reply_markup)

if __name__ == "__main__":
    asyncio.run(send_vpn_update())
