import requests
import pandas as pd
import io
import asyncio
import os
from telegram import Bot

# GitHub Secrets se data uthane ke liye os.getenv use hota hai
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

async def send_vpn_update():
    print("Fetching live servers from VPNGate...")
    url = "https://www.vpngate.net/api/iphone/"
    
    try:
        response = requests.get(url)
        # Data cleaning logic
        lines = response.text.split('\n')
        data = "\n".join(lines[1:-2]).replace('*', '')
        df = pd.read_csv(io.StringIO(data))
        
        # Ping check aur best servers filter
        df['Ping'] = pd.to_numeric(df['Ping'], errors='coerce')
        df = df.dropna(subset=['Ping']).sort_values(by='Ping')
        
        # Top 8 fastest servers
        top_servers = df.head(8) 
        
        message = "🛡️ *MISSION MERIT VPN LIVE* 🛡️\n"
        message += "━━━━━━━━━━━━━━━━━━\n\n"
        
        for _, row in top_servers.iterrows():
            icon = "🟢" if row['Ping'] < 60 else "🟡"
            message += f"{icon} *Country:* {row['CountryLong']}\n"
            message += f"🌐 *IP:* `{row['IP']}`\n"
            message += f"⚡ *Ping:* {int(row['Ping'])}ms\n"
            message += f"📥 *Speed:* {round(row['Speed']/10**6, 2)} Mbps\n"
            message += "━━━━━━━━━━━━━━━━━━\n"
            
        message += "\n👤 *User:* `vpn` | 🔑 *Pass:* `vpn` \n"
        message += "\n🔄 _Next update in 1 hour_"
        
        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
        print("✅ Success! Update sent to Telegram.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

# GitHub Actions environment mein asyncio run karne ka tarika
if __name__ == "__main__":
    asyncio.run(send_vpn_update())
