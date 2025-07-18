import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
import threading
import os
from playwright.async_api import async_playwright

TOKEN = "ISI_TOKEN_BOT_MU"

app = Flask(__name__)

async def generate_qr():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://shopee.co.id/buyer/login?login_type=qr")
        await page.wait_for_selector("canvas", timeout=10000)
        qr_path = "qrcode.png"
        await page.locator("canvas").screenshot(path=qr_path)
        await asyncio.sleep(90)
        await browser.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Gunakan /mintaqr untuk mendapatkan QR login Shopee"
    )

async def mintaqr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Silakan scan QR ke Shopee")
    await generate_qr()
    with open("qrcode.png", "rb") as qr_file:
        await update.message.reply_photo(photo=qr_file)
    await asyncio.sleep(90)
    await update.message.reply_text("❌ QR expired. Ketik /mintaqr untuk ambil baru.")

@app.route("/")
def home():
    return "Bot QR Shopee aktif!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run_flask).start()

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("mintaqr", mintaqr))
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
