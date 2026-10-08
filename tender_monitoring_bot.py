import time
import datetime
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types

# --- SOZLAMALAR ---
TELEGRAM_BOT_TOKEN = "8886515862:AAF_OgNPap1iJUWuMv9lDMlbRbVLOqOZd8A"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Odatiy kalit so'zlar ro'yxati
user_keywords = ["burg'ilash", "portlatish", "bvr", "бурение", "взрыв", "бвр"]
sent_tenders = set()

# Holatni kuzatib borish uchun lug'at (kalit so'z o'zgartirish rejimi uchun)
user_states = {}

def get_headers():
    return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# 1. ETENDER.UZEX.UZ TEKSHIRISH
def check_etender(chat_id):
    bot.send_message(chat_id, "🔍 <b>etender.uzex.uz</b> tekshirilmoqda...", parse_mode="HTML")
    url = "https://etender.uzex.uz/lot-list"
    found = 0
    try:
        res = requests.get(url, headers=get_headers(), timeout=15)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            lots = soup.find_all('div', class_='lot-item')
            for lot in lots:
                title_elem = lot.find('a', class_='lot-title')
                if not title_elem:
                    continue
                title = title_elem.text.strip()
                link = "https://etender.uzex.uz" + title_elem['href']

                if any(kw.lower() in title.lower() for kw in user_keywords):
                    msg = (
                        f"🚨 <b>ETENDER: YANGI TENDER!</b>\n\n"
                        f"📌 <b>Nomi:</b> {title}\n"
                        f"🔗 <b>Havola:</b> <a href='{link}'>Lotni ko'rish</a>\n"
                        f"📅 <b>Sana:</b> {datetime.date.today()}"
                    )
                    bot.send_message(chat_id, msg, parse_mode="HTML")
                    found += 1
        if found == 0:
            bot.send_message(chat_id, "ℹ️ etender.uzex.uz portalida kalit so'zlaringizga mos tenderlar topilmadi.")
    except Exception as e:
        bot.send_message(chat_id, f"❌ etender.uzex.uz tekshirishda xatolik: {e}")

# 2. XARID.UZEX.UZ / DXARIDS TEKSHIRISH
def check_xarid_uzex(chat_id):
    bot.send_message(chat_id, "🔍 <b>xarid.uzex.uz</b> tekshirilmoqda...", parse_mode="HTML")
    url = "https://dxarids.uzex.uz/ru/trade/auction"
    found = 0
    try:
        res = requests.get(url, headers=get_headers(), timeout=15)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            lots = soup.find_all('tr', class_='trade-row')
            for lot in lots:
                title_elem = lot.find('a')
                if not title_elem:
                    continue
                title = title_elem.text.strip()
                link = "https://dxarids.uzex.uz" + title_elem['href']

                if any(kw.lower() in title.lower() for kw in user_keywords):
                    msg = (
                        f"🚨 <b>XARID.UZEX: YANGI LOT!</b>\n\n"
                        f"📌 <b>Nomi:</b> {title}\n"
                        f"🔗 <b>Havola:</b> <a href='{link}'>Lotni ko'rish</a>\n"
                        f"📅 <b>Sana:</b> {datetime.date.today()}"
                    )
                    bot.send_message(chat_id, msg, parse_mode="HTML")
                    found += 1
        if found == 0:
            bot.send_message(chat_id, "ℹ️ xarid.uzex.uz portalida mos lotlar topilmadi.")
    except Exception as e:
        bot.send_message(chat_id, f"❌ xarid.uzex.uz tekshirishda xatolik: {e}")

# 3. XT-XARID.UZ TEKSHIRISH
def check_xt_xarid(chat_id):
    bot.send_message(chat_id, "🔍 <b>xt-xarid.uz</b> tekshirilmoqda...", parse_mode="HTML")
    url = "https://xt-xarid.uz/lots"
    found = 0
    try:
        res = requests.get(url, headers=get_headers(), timeout=15)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            lots = soup.find_all('div', class_='lot-card')
            for lot in lots:
                title_elem = lot.find('h5')
                if not title_elem:
                    continue
                title = title_elem.text.strip()
                link_elem = lot.find('a')
                link = "https://xt-xarid.uz" + link_elem['href'] if link_elem else "https://xt-xarid.uz"

                if any(kw.lower() in title.lower() for kw in user_keywords):
                    msg = (
                        f"🚨 <b>XT-XARID: YANGI LOT!</b>\n\n"
                        f"📌 <b>Nomi:</b> {title}\n"
                        f"🔗 <b>Havola:</b> <a href='{link}'>Lotni ko'rish</a>\n"
                        f"📅 <b>Sana:</b> {datetime.date.today()}"
                    )
                    bot.send_message(chat_id, msg, parse_mode="HTML")
                    found += 1
        if found == 0:
            bot.send_message(chat_id, "ℹ️ xt-xarid.uz portalida mos lotlar topilmadi.")
    except Exception as e:
        bot.send_message(chat_id, f"❌ xt-xarid.uz tekshirishda xatolik: {e}")

# MENYU TUGMALARI
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🌐 etender.uzex.uz")
    btn2 = types.KeyboardButton("🌐 xarid.uzex.uz")
    btn3 = types.KeyboardButton("🌐 xt-xarid.uz")
    btn4 = types.KeyboardButton("🚀 Barcha saytlarni tekshirish")
    btn5 = types.KeyboardButton("📋 Mening kalit soʻzlarim")
    btn6 = types.KeyboardButton("✏️ Kalit soʻzlarni oʻzgartirish")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

# /start BUYRUG'I
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "<b>Tender Monitoring Boti</b>ga xush kelibsiz!\n\n"
        "Menyu orqali saytlarni tekshirishingiz yoki qidiruv uchun kalit soʻzlarni oʻzgartirishingiz mumkin.",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

# XABARLARNI QABUL QILISH VA ISHLASH
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    text = message.text

    # Agar foydalanuvchi yangi kalit so'zlarni yuborayotgan bo'lsa
    if user_states.get(chat_id) == "waiting_for_keywords":
        global user_keywords
        # So'zlarni vergul bilan ajratib olamiz
        new_keywords = [kw.strip() for kw in text.split(",") if kw.strip()]
        if new_keywords:
            user_keywords = new_keywords
            user_states[chat_id] = None
            bot.send_message(
                chat_id,
                f"✅ Kalit soʻzlar muvaffaqiyatli yangilandi!\n\n<b>Yangi roʻyxat:</b> {', '.join(user_keywords)}",
                parse_mode="HTML",
                reply_markup=main_menu()
            )
        else:
            bot.send_message(chat_id, "⚠️ Iltimos, kamida bitta toʻgʻri kalit soʻz kiriting.")
        return

    # Menyu buyruqlari
    if text == "🌐 etender.uzex.uz":
        check_etender(chat_id)
    elif text == "🌐 xarid.uzex.uz":
        check_xarid_uzex(chat_id)
    elif text == "🌐 xt-xarid.uz":
        check_xt_xarid(chat_id)
    elif text == "🚀 Barcha saytlarni tekshirish" or text == "/tekshir":
        check_etender(chat_id)
        check_xarid_uzex(chat_id)
        check_xt_xarid(chat_id)
    elif text == "📋 Mening kalit soʻzlarim":
        bot.send_message(
            chat_id,
            f"📌 <b>Hozirgi kalit soʻzlar roʻyxati:</b>\n\n" + "\n".join([f"• {kw}" for kw in user_keywords]),
            parse_mode="HTML"
        )
    elif text == "✏️ Kalit soʻzlarni oʻzgartirish":
        user_states[chat_id] = "waiting_for_keywords"
        bot.send_message(
            chat_id,
            "📝 Yangi kalit soʻzlarni <b>vergul bilan ajratib</b> yuboring:\n\n"
            "<i>Masalan: cement, gisht, shifer, qurilish</i>",
            parse_mode="HTML"
        )
    else:
        bot.send_message(chat_id, "Iltimos, pastdagi menyu tugmalaridan birini tanlang.", reply_markup=main_menu())

if __name__ == "__main__":
    print("Bot menyu va yangi kalit so'zlar rejimi bilan ishga tushdi...")
    bot.infinity_polling()
