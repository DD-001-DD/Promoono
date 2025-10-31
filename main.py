import sqlite3
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# 🔹 Verilənlər bazasını hazırlayırıq
def init_db():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT
        )
    """)
    conn.commit()
    conn.close()

# 🔹 /start komandası
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_button = KeyboardButton("📞 Share your contact", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Salam! Əgər nömrəni paylaşmaq istəyirsənsə, aşağıdakı düyməyə bas 👇",
        reply_markup=reply_markup
    )

# 🔹 İstifadəçi nömrəsini paylaşanda işləyir
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if contact:
        name = contact.first_name
        phone = contact.phone_number

        # Mesaj göndəririk
        await update.message.reply_text(f"✅ {name}, sənin nömrən: {phone}")

        # 🔹 Bazaya yazırıq
        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
        conn.commit()
        conn.close()
        print(f"[+] Yeni nömrə əlavə olundu: {name} - {phone}")

    else:
        await update.message.reply_text("❌ Nömrə paylaşılmadı.")

# 🔹 Botu işə salırıq
def main():
    init_db()  # Bazanı yaradıb yoxlayırıq

    # ⚠️ Buraya öz BOT tokenini yaz
    TOKEN = "8380962766:AAHuEddhvRKIYaPASbkQ96PbuHGO-Vvmg-4"

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

    print("🤖 Bot işləyir... Telegram-da /start yaz və test et.")
    app.run_polling()

if __name__ == "__main__":
    main()
