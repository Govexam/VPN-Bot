import requests, pandas as pd, io, asyncio, os
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

# GitHub Secrets se data fetch
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Aapka Blogger link jo aapne banaya
BLOG_URL = "https://missionmerit.blogspot.com/p/how-to-connect.html"

async def send_vpn_update():
    print("Fetching servers from VPNGate...")
    url = "https://www.vpngate.net/api/iphone/"
    
    try:
        response = requests.get(url)
        lines = response.text.split('\n')
        data = "\n".join(lines[1:-2]).replace('*', '')
        df = pd.read_csv(io.StringIO(data))
        
        # Best Ping wale servers select karein
        df['Ping'] = pd.to_numeric(df['Ping'], errors='coerce')
        df = df.dropna(subset=['Ping']).sort_values(by='Ping')
        
        top_servers = df.head(8)
        
        message = "🛡️ *MISSION MERIT VPN LIVE* 🛡️\n"
        message += "━━━━━━━━━━━━━━━━━━\n\n"
        
        for _, row in top_servers.iterrows():
            icon = "🟢" if row['Ping'] < 60 else "🟡"
            message += f"{icon} *Country:* {row['CountryLong']}\n"
            message += f"🌐 *IP:* `{row['IP']}`\n"
            message += f"⚡ *Ping:* {int(row['Ping'])}ms\n"
            message += "━━━━━━━━━━━━━━━━━━\n"
            
        message += "\n👤 *User/Pass:* `vpn` | `vpn` \n"
        message += "🔄 _Updated every 60 minutes_"

        # Professional Buttons
        keyboard = [
            [InlineKeyboardButton("📖 How to Connect (Setup)", url=BLOG_URL)],
            [InlineKeyboardButton("💬 Contact Support", url="https://t.me/LUCIFERKAKA")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown', reply_markup=reply_markup)
        print("✅ Message sent with Buttons!")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(send_vpn_update())
