import asyncio
import random
import string
import logging
import aiosqlite
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = '8915805327:AAGSC0o39SCg3iVT-CftKEK2W0Y0_sj66aw'
ADMIN_PASSWORD = "hpQeu7Kk"

TEXTS = {
    "ru": {
        "welcome": "🏔️ Добро пожаловать в NORDNFT – надёжный P2P-гарант\n\n🔒 Покупайте и продавайте NFT, токены, Telegram-подарки и многое другое – безопасно и без риска.\n\n• Удобное управление балансами\n• Реферальная система\n• Сделки с гарантией\n\nВыберите нужный раздел ниже:",
        "profile": "💰 Ваши балансы:\n🇷🇺 Рубли: {rub} RUB\n💵 USD: {usd} USD\n⭐ Звёзды: {stars} STARS\n\n📝 Ваши реквизиты:\n{req_text}\n\n📊 Ваша история сделок:\n{history_text}",
        "no_req": "❌ Реквизиты не заполнены.",
        "no_history": "У вас пока нет сделок.",
        "reqs_saved": "✅ Реквизиты сохранены в базе!",
        "reqs_format": "💳 Введи свои реквизиты для вывода.\nИспользуй формат:\n\n`card: номер карты`\n`crypto: адрес кошелька`\n`stars: @username`\n\nПример:\n`card: 1234 5678 9012 3456`",
        "withdraw_ask": "💰 Введи сумму для вывода (в той валюте, которую хочешь вывести):",
        "withdraw_ok": "✅ Заявка на вывод {amount} {currency} создана!\nРеквизиты:\nКарта: {card}\nКрипта: {crypto}\nЗвёзды: {stars}\n\nСредства будут отправлены в ближайшее время.",
        "withdraw_low": "❌ Недостаточно средств на балансе.",
        "choose_pay": "💰 Выбери валюту, в которой принимаешь оплату:",
        "no_reqs_pay": "⚠️ Сначала добавь реквизиты для вывода!",
        "nft_name": "✏️ Введи название NFT (например: CryptoPunk #123):",
        "nft_price": "💰 Введи цену в выбранной валюте (только число):",
        "nft_buyer": "🆔 Введи @username покупателя (без @, например: john_doe):",
        "deal_created": "✅ Сделка #{id} создана!\nКод: {code}\nNFT: {nft}\nЦена: {price} {pay}\nПокупатель: @{buyer}\n\n🔗 Отправь ссылку покупателю:\n{link}",
        "buyer_notify": "📦 Продавец создал для тебя сделку!\nNFT: {nft}\nЦена: {price} {pay}\n\n🔗 Перейди по ссылке, чтобы оплатить:\n{link}",
        "deal_joined": "🔗 Вы присоединились к сделке #{id}!\nNFT: {nft}\nЦена: {price} {pay}\n\n💰 Ваш баланс ({pay}): {balance} \n\nДля оплаты нажмите кнопку. Деньги будут заморожены.",
        "pay_btn": "✅ Оплатить со счета",
        "no_money": "❌ Недостаточно средств на балансе в {pay}.\nВаш баланс: {balance}\nЦена: {price}\n\nОбратитесь к администратору.",
        "money_frozen": "✅ Деньги списаны и заморожены!\nСделка #{id} ожидает передачи NFT.",
        "seller_notify_pay": "🔔 Покупатель @{buyer} оплатил сделку #{id}!\nДеньги заморожены.\n\nПередайте NFT и нажмите кнопку.",
        "transfer_btn": "📤 Передал товар",
        "transfer_ok": "✅ Вы подтвердили передачу NFT!\nТеперь покупатель должен подтвердить получение.",
        "buyer_notify_transfer": "🔔 Продавец передал вам NFT по сделке #{id}!\nПроверьте получение и нажмите кнопку.",
        "confirm_btn": "✅ Подтвердить получение",
        "confirm_ok": "✅ Сделка #{id} завершена!\nДеньги разморожены и переведены продавцу.\nСпасибо!",
        "seller_notify_confirm": "💰 Сделка #{id} завершена!\nСумма {price} {pay} зачислена на ваш баланс.",
        "ref_link": "🔗 Твоя реферальная ссылка:\nhttps://t.me/NORDNFT_bot?start=ref_{uid}",
        "support": "📞 Связь с поддержкой: @Nordnftsupport",
        "back": "🏔️ Главное меню:",
        "lang_changed": "🌍 Язык изменён на русский.",
        "unknown": "Используй кнопки или /start.",
        "btn_profile": "💼 Профиль",
        "btn_create": "➕ Создать сделку",
        "btn_ref": "📊 Реферальная ссылка",
        "btn_lang": "🌐 Change language",
        "btn_support": "🆘 Поддержка",
        "btn_back": "🔙 Назад",
        "btn_edit_req": "✏️ Изменить реквизиты",
        "btn_withdraw": "💳 Вывести средства",
        "btn_add_req": "➕ Добавить реквизиты"
    },
    "en": {
        "welcome": "🏔️ Welcome to NORDNFT – reliable P2P escrow\n\n🔒 Buy and sell NFTs, tokens, Telegram gifts and more – safely and risk-free.\n\n• Easy balance management\n• Referral system\n• Secure deals\n\nChoose a section below:",
        "profile": "💰 Your balances:\n🇷🇺 RUB: {rub} RUB\n💵 USD: {usd} USD\n⭐ STARS: {stars} STARS\n\n📝 Your payment details:\n{req_text}\n\n📊 Your deal history:\n{history_text}",
        "no_req": "❌ Payment details not set.",
        "no_history": "You have no deals yet.",
        "reqs_saved": "✅ Details saved to database!",
        "reqs_format": "💳 Enter your payment details.\nFormat:\n\n`card: card number`\n`crypto: wallet address`\n`stars: @username`\n\nExample:\n`card: 1234 5678 9012 3456`",
        "withdraw_ask": "💰 Enter amount to withdraw (in the currency you want):",
        "withdraw_ok": "✅ Withdrawal request for {amount} {currency} created!\nDetails:\nCard: {card}\nCrypto: {crypto}\nStars: {stars}\n\nFunds will be sent soon.",
        "withdraw_low": "❌ Insufficient funds.",
        "choose_pay": "💰 Choose payment currency:",
        "no_reqs_pay": "⚠️ Add payment details first!",
        "nft_name": "✏️ Enter NFT name (e.g., CryptoPunk #123):",
        "nft_price": "💰 Enter price (number only):",
        "nft_buyer": "🆔 Enter buyer's @username (without @, e.g., john_doe):",
        "deal_created": "✅ Deal #{id} created!\nCode: {code}\nNFT: {nft}\nPrice: {price} {pay}\nBuyer: @{buyer}\n\n🔗 Send link to buyer:\n{link}",
        "buyer_notify": "📦 Seller created a deal for you!\nNFT: {nft}\nPrice: {price} {pay}\n\n🔗 Click to pay:\n{link}",
        "deal_joined": "🔗 You joined deal #{id}!\nNFT: {nft}\nPrice: {price} {pay}\n\n💰 Your balance ({pay}): {balance} \n\nClick to pay. Funds will be frozen.",
        "pay_btn": "✅ Pay from balance",
        "no_money": "❌ Insufficient funds in {pay}.\nBalance: {balance}\nPrice: {price}\n\nContact admin.",
        "money_frozen": "✅ Funds deducted and frozen!\nDeal #{id} awaits NFT transfer.",
        "seller_notify_pay": "🔔 Buyer @{buyer} paid for deal #{id}!\nFunds frozen.\n\nTransfer NFT and click button.",
        "transfer_btn": "📤 Transferred item",
        "transfer_ok": "✅ You confirmed transfer!\nNow buyer must confirm receipt.",
        "buyer_notify_transfer": "🔔 Seller transferred NFT for deal #{id}!\nCheck it and click confirm.",
        "confirm_btn": "✅ Confirm receipt",
        "confirm_ok": "✅ Deal #{id} completed!\nFunds unfrozen and sent to seller.\nThank you!",
        "seller_notify_confirm": "💰 Deal #{id} completed!\n{price} {pay} added to your balance.",
        "ref_link": "🔗 Your referral link:\nhttps://t.me/NORDNFT_bot?start=ref_{uid}",
        "support": "📞 Support: @Nordnftsupport",
        "back": "🏔️ Main menu:",
        "lang_changed": "🌍 Language changed to English.",
        "unknown": "Use buttons or /start.",
        "btn_profile": "💼 Profile",
        "btn_create": "➕ Create deal",
        "btn_ref": "📊 Referral link",
        "btn_lang": "🌐 Change language",
        "btn_support": "🆘 Support",
        "btn_back": "🔙 Back",
        "btn_edit_req": "✏️ Edit details",
        "btn_withdraw": "💳 Withdraw",
        "btn_add_req": "➕ Add details"
    }
}

async def init_db():
    async with aiosqlite.connect('database.db') as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS users (
            uid INTEGER PRIMARY KEY,
            balance_rub REAL DEFAULT 0,
            balance_usd REAL DEFAULT 0,
            balance_stars REAL DEFAULT 0,
            card TEXT DEFAULT '',
            crypto TEXT DEFAULT '',
            stars TEXT DEFAULT '',
            lang TEXT DEFAULT 'ru'
        )""")
        async with db.execute("PRAGMA table_info(users)") as cursor:
            columns = [info[1] for info in await cursor.fetchall()]
            if "lang" not in columns:
                await db.execute("ALTER TABLE users ADD COLUMN lang TEXT DEFAULT 'ru'")
        await db.execute("""CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller_id INTEGER,
            buyer_id INTEGER,
            nft TEXT,
            price REAL,
            payment TEXT,
            status TEXT,
            code TEXT,
            buyer_username TEXT
        )""")
        await db.commit()

async def get_user(uid):
    async with aiosqlite.connect('database.db') as db:
        async with db.execute("SELECT balance_rub, balance_usd, balance_stars, card, crypto, stars, lang FROM users WHERE uid = ?", (uid,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {"rub": row[0], "usd": row[1], "stars_bal": row[2], "card": row[3], "crypto": row[4], "stars": row[5], "lang": row[6]}
            else:
                await db.execute("INSERT INTO users (uid) VALUES (?)", (uid,))
                await db.commit()
                return {"rub": 0, "usd": 0, "stars_bal": 0, "card": "", "crypto": "", "stars": "", "lang": "ru"}

async def update_balance(uid, field, amount):
    if field in ['balance_rub', 'balance_usd', 'balance_stars']:
        async with aiosqlite.connect('database.db') as db:
            await db.execute(f"UPDATE users SET {field} = {field} + ? WHERE uid = ?", (amount, uid))
            await db.commit()

async def update_reqs(uid, field, value):
    if field in ['card', 'crypto', 'stars']:
        async with aiosqlite.connect('database.db') as db:
            await db.execute(f"UPDATE users SET {field} = ? WHERE uid = ?", (value, uid))
            await db.commit()

async def update_lang(uid, lang):
    async with aiosqlite.connect('database.db') as db:
        await db.execute("UPDATE users SET lang = ? WHERE uid = ?", (lang, uid))
        await db.commit()

async def get_deal(deal_id):
    async with aiosqlite.connect('database.db') as db:
        async with db.execute("SELECT * FROM deals WHERE id = ?", (deal_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    "id": row[0], "seller": row[1], "buyer_id": row[2], "nft": row[3], 
                    "price": row[4], "payment": row[5], "status": row[6], "code": row[7], "buyer_username": row[8]
                }
            return None

async def get_user_deals(uid):
    async with aiosqlite.connect('database.db') as db:
        async with db.execute("SELECT id, nft, price, status, buyer_username FROM deals WHERE seller_id = ? OR buyer_id = ? ORDER BY id DESC LIMIT 5", (uid, uid)) as cursor:
            return await cursor.fetchall()

async def update_deal_status(deal_id, status, buyer_id=None):
    async with aiosqlite.connect('database.db') as db:
        if buyer_id:
            await db.execute("UPDATE deals SET status = ?, buyer_id = ? WHERE id = ?", (status, buyer_id, deal_id))
        else:
            await db.execute("UPDATE deals SET status = ? WHERE id = ?", (status, deal_id))
        await db.commit()

def generate_deal_code():
    chars = string.ascii_letters + string.digits
    return f"#{''.join(random.choices(chars, k=6))}"

async def get_lang(uid):
    user = await get_user(uid)
    return user.get("lang", "ru")

async def get_text(uid, key, **kwargs):
    lang = await get_lang(uid)
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, key)
    if "uid" not in kwargs:
        kwargs["uid"] = uid
    return text.format(**kwargs)

async def main_menu_keyboard(uid):
    lang = await get_lang(uid)
    t = TEXTS[lang]
    keyboard = [
        [KeyboardButton(t["btn_profile"]), KeyboardButton(t["btn_create"])],
        [KeyboardButton(t["btn_ref"]), KeyboardButton(t["btn_lang"])],
        [KeyboardButton(t["btn_support"])]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def profile_keyboard(uid):
    lang = await get_lang(uid)
    t = TEXTS[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t["btn_edit_req"], callback_data="edit_req")],
        [InlineKeyboardButton(t["btn_withdraw"], callback_data="withdraw")]
    ])

async def payment_keyboard(uid):
    user = await get_user(uid)
    buttons = []
    lang = await get_lang(uid)
    if user.get("card"): buttons.append("🇷🇺 Рубли (карта)" if lang == "ru" else "🇷🇺 RUB (card)")
    if user.get("crypto"): buttons.append("💵 USDT (крипта)" if lang == "ru" else "💵 USDT (crypto)")
    if user.get("stars"): buttons.append("⭐ Звёзды (Telegram)" if lang == "ru" else "⭐ Stars (Telegram)")
    if not buttons: buttons = ["⚠️ Сначала добавь реквизиты" if lang == "ru" else "⚠️ Add details first"]
    keyboard = [[KeyboardButton(b)] for b in buttons]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await get_user(uid)
    
    if context.args and context.args[0].startswith("deal_"):
        try:
            deal_id = int(context.args[0].split("_")[1])
            await handle_deal_link(update, context, deal_id)
        except (IndexError, ValueError):
            await update.message.reply_text("❌ Неверный формат ссылки.")
        return

    text = await get_text(uid, "welcome")
    kb = await main_menu_keyboard(uid)
    await update.message.reply_text(text, reply_markup=kb)

async def handle_deal_link(update: Update, context: ContextTypes.DEFAULT_TYPE, deal_id: int):
    uid = update.effective_user.id
    deal = await get_deal(deal_id)

    if not deal:
        await update.message.reply_text("❌ Сделка не найдена.")
        return
    if deal['status'] != "ожидает оплаты":
        await update.message.reply_text(f"❌ Эта сделка уже {deal['status']}.")
        return

    buyer_username = update.effective_user.username or str(uid)
    if deal['buyer_username'] != buyer_username and deal['buyer_username'] != str(uid):
        await update.message.reply_text("❌ Эта сделка для другого пользователя.")
        return

    await update_deal_status(deal_id, "ожидает оплаты", buyer_id=uid)
    context.user_data['current_deal'] = deal_id
    
    display_id = deal_id + 458
    user = await get_user(uid)
    pay = deal['payment']
    if "Рубли" in pay: balance = user['rub']
    elif "USDT" in pay: balance = user['usd']
    else: balance = user['stars_bal']
    
    btn_text = await get_text(uid, "pay_btn")
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(btn_text, callback_data=f"pay_{deal_id}")]])

    text = await get_text(uid, "deal_joined", id=display_id, nft=deal['nft'], price=deal['price'], pay=pay, balance=balance)
    await update.message.reply_text(text, reply_markup=keyboard)

async def rub_command(update: Update, context: ContextTypes.DEFAULT_TYPE): await handle_deposit(update, context, "balance_rub")
async def usd_command(update: Update, context: ContextTypes.DEFAULT_TYPE): await handle_deposit(update, context, "balance_usd")
async def stars_command(update: Update, context: ContextTypes.DEFAULT_TYPE): await handle_deposit(update, context, "balance_stars")

async def handle_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE, field: str):
    uid = update.effective_user.id
    args = context.args
    if len(args) != 2:
        await update.message.reply_text(f"❌ Формат: /{update.message.text.split()[0][1:]} сумма пароль")
        return
    try: amount = float(args[0])
    except ValueError: await update.message.reply_text("❌ Введи число."); return
    if args[1] != ADMIN_PASSWORD: await update.message.reply_text("❌ Неверный пароль."); return

    await update_balance(uid, field, amount)
    user = await get_user(uid)
    await update.message.reply_text(f"✅ Баланс пополнен на {amount}!\nТекущие балансы:\nРубли: {user['rub']}\nUSD: {user['usd']}\nЗвёзды: {user['stars_bal']}")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    user = await get_user(uid)
    lang = await get_lang(uid)
    t = TEXTS[lang]

    # Очистка состояний при переходе по меню
    context.user_data.clear()

    if text == t["btn_profile"]:
        req_text = ""
        if user.get("card"): req_text += f"💳 Карта: {user['card']}\n"
        if user.get("crypto"): req_text += f"🔗 Крипта: {user['crypto']}\n"
        if user.get("stars"): req_text += f"⭐ Звёзды: {user['stars']}\n"
        if not req_text: req_text = await get_text(uid, "no_req")

        history_text = ""
        deals = await get_user_deals(uid)
        if not deals:
            history_text = await get_text(uid, "no_history")
        else:
            for d in deals:
                display_history_id = d[0] + 458
                history_text += f"🔹 #{display_history_id} | {d[1]} | {d[2]} | Статус: {d[3]}\n"
        
        profile_msg = await get_text(uid, "profile", rub=user['rub'], usd=user['usd'], stars=user['stars_bal'], req_text=req_text, history_text=history_text)
        kb = await profile_keyboard(uid)
        await update.message.reply_text(profile_msg, reply_markup=kb)
        return

    elif text == t["btn_lang"]:
        new_lang = "en" if lang == "ru" else "ru"
        await update_lang(uid, new_lang)
        changed_txt = await get_text(uid, "lang_changed")
        kb = await main_menu_keyboard(uid)
        await update.message.reply_text(changed_txt, reply_markup=kb)
        return

    elif text == t["btn_create"]:
        if not any([user.get("card"), user.get("crypto"), user.get("stars")]):
            no_reqs_txt = await get_text(uid, "no_reqs_pay")
            await update.message.reply_text(no_reqs_txt)
            return
        choose_pay_txt = await get_text(uid, "choose_pay")
        kb = await payment_keyboard(uid)
        await update.message.reply_text(choose_pay_txt, reply_markup=kb)
        context.user_data['awaiting_payment'] = True
        return

    elif text == t["btn_ref"]:
        ref_txt = await get_text(uid, "ref_link")
        await update.message.reply_text(ref_txt)
        return

    elif text == t["btn_support"]:
        sup_txt = await get_text(uid, "support")
        await update.message.reply_text(sup_txt)
        return

    elif text in ["🇷🇺 Рубли (карта)", "💵 USDT (крипта)", "⭐ Звёзды (Telegram)", "🇷🇺 RUB (card)", "💵 USDT (crypto)", "⭐ Stars (Telegram)"] and context.user_data.get('awaiting_payment'):
        context.user_data['payment_method'] = text
        context.user_data['awaiting_payment'] = False
        nft_name_txt = await get_text(uid, "nft_name")
        await update.message.reply_text(nft_name_txt)
        context.user_data['awaiting_nft'] = True
        return
        
    elif text in ["🔙 Назад", "🔙 Back"]:
        kb = await main_menu_keyboard(uid)
        back_txt = await get_text(uid, "back")
        await update.message.reply_text(back_txt, reply_markup=kb)
        return

async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text

    if context.user_data.get('awaiting_requisites'):
        saved_any = False
        for line in text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                if key in ['card', 'карта']:
                    await update_reqs(uid, 'card', value.strip())
                    saved_any = True
                elif key in ['crypto', 'крипта', 'usdt']:
                    await update_reqs(uid, 'crypto', value.strip())
                    saved_any = True
                elif key in ['stars', 'звезды', 'звёзды']:
                    await update_reqs(uid, 'stars', value.strip())
                    saved_any = True
        if saved_any:
            context.user_data.clear()
            saved_txt = await get_text(uid, "reqs_saved")
            kb = await main_menu_keyboard(uid)
            await update.message.reply_text(saved_txt, reply_markup=kb)
        else:
            await update.message.reply_text("❌ Ошибка формата. Используйте префиксы, например:\ncard: 1234 5678...")
        return

    if context.user_data.get('awaiting_withdraw'):
        try:
            amount = float(text)
            if amount <= 0:
                await update.message.reply_text("❌ Введи число больше 0.")
                return
            user = await get_user(uid)
            if amount > user.get("rub", 0):
                low_txt = await get_text(uid, "withdraw_low")
                await update.message.reply_text(low_txt)
                return
            await update_balance(uid, "balance_rub", -amount)
            user = await get_user(uid)
            ok_txt = await get_text(uid, "withdraw_ok", amount=amount, currency="RUB", card=user.get('card','-'), crypto=user.get('crypto','-'), stars=user.get('stars','-'))
            kb = await main_menu_keyboard(uid)
            await update.message.reply_text(ok_txt, reply_markup=kb)
            context.user_data.clear()
        except ValueError: 
            await update.message.reply_text("❌ Введи число.")
        return

    if context.user_data.get('awaiting_nft'):
        context.user_data['nft_name'] = text
        context.user_data['awaiting_nft'] = False
        price_txt = await get_text(uid, "nft_price")
        await update.message.reply_text(price_txt)
        context.user_data['awaiting_price'] = True
        return

    if context.user_data.get('awaiting_price'):
        try:
            price = float(text)
            context.user_data['price'] = price
            context.user_data['awaiting_price'] = False
            buyer_txt = await get_text(uid, "nft_buyer")
            await update.message.reply_text(buyer_txt)
            context.user_data['awaiting_buyer'] = True
        except ValueError: 
            await update.message.reply_text("❌ Введи число.")
        return

    if context.user_data.get('awaiting_buyer'):
        buyer_username = text.strip().replace('@', '')
        context.user_data['buyer_username'] = buyer_username
        context.user_data['awaiting_buyer'] = False
        await finish_deal(update, context)
        return

async def finish_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    deal_data = {
        "nft": context.user_data.get('nft_name'), 
        "price": context.user_data.get('price'), 
        "buyer_username": context.user_data.get('buyer_username'), 
        "payment_method": context.user_data.get('payment_method')
    }
    if not all(deal_data.values()):
        await update.message.reply_text("❌ Ошибка. Начни заново.")
        return

    deal_code = generate_deal_code()
    
    async with aiosqlite.connect('database.db') as db:
        cursor = await db.execute("""INSERT INTO deals (seller_id, nft, price, payment, status, code, buyer_username) VALUES (?, ?, ?, ?, ?, ?, ?)""", (uid, deal_data['nft'], deal_data['price'], deal_data['payment_method'], "ожидает оплаты", deal_code, deal_data['buyer_username']))
        deal_id = cursor.lastrowid
        await db.commit()

    display_id = deal_id + 458
    bot_username = (await context.bot.get_me()).username
    deal_link = f"https://t.me/{bot_username}?start=deal_{deal_id}"

    deal_created_txt = await get_text(uid, "deal_created", id=display_id, code=deal_code, nft=deal_data['nft'], price=deal_data['price'], pay=deal_data['payment_method'], buyer=deal_data['buyer_username'], link=deal_link)
    await update.message.reply_text(deal_created_txt)
    
    try: 
        buyer_notify_txt = await get_text(uid, "buyer_notify", nft=deal_data['nft'], price=deal_data['price'], pay=deal_data['payment_method'], link=deal_link)
        await context.bot.send_message(deal_data['buyer_username'], buyer_notify_txt)
    except Exception as e: 
        logging.error(f"Failed to notify buyer: {e}")
        pass
        
    context.user_data.clear()

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = update.effective_user.id
    data = query.data
    lang = await get_lang(uid)
    t = TEXTS[lang]

    if data == "edit_req":
        format_txt = await get_text(uid, "reqs_format")
        await query.message.reply_text(format_txt, parse_mode="Markdown")
        context.user_data['awaiting_requisites'] = True
        return
        
    elif data == "withdraw":
        user = await get_user(uid)
        if not any([user.get("card"), user.get("crypto"), user.get("stars")]):
            no_reqs_txt = await get_text(uid, "no_reqs_pay")
            await query.message.reply_text(no_reqs_txt)
            return
        ask_txt = await get_text(uid, "withdraw_ask")
        kb = ReplyKeyboardMarkup([[KeyboardButton(t["btn_back"])]], resize_keyboard=True)
        await query.message.reply_text(ask_txt, reply_markup=kb)
        context.user_data['awaiting_withdraw'] = True
        return
        
    elif data == "back":
        back_txt = await get_text(uid, "back")
        kb = await main_menu_keyboard(uid)
        await query.message.reply_text(back_txt, reply_markup=kb)
        return

    if data.startswith("pay_"):
        deal_id = int(data.split("_")[1])
        deal = await get_deal(deal_id)
        if not deal or deal['status'] != "ожидает оплаты": 
            await query.edit_message_text("❌ Недействительно.")
            return
        
        user = await get_user(uid)
        pay = deal['payment']
        
        if "Рубли" in pay: bal = user['rub']
        elif "USDT" in pay: bal = user['usd']
        else: bal = user['stars_bal']
        
        if bal < deal['price']: 
            no_money_txt = await get_text(uid, "no_money", balance=bal, pay=pay, price=deal['price'])
            await query.edit_message_text(no_money_txt)
            return
        
        if "Рубли" in pay: await update_balance(uid, "balance_rub", -deal['price'])
        elif "USDT" in pay: await update_balance(uid, "balance_usd", -deal['price'])
        else: await update_balance(uid, "balance_stars", -deal['price'])
        
        await update_deal_status(deal_id, "деньги заморожены", buyer_id=uid)
        display_id = deal_id + 458
        
        money_frozen_txt = await get_text(uid, "money_frozen", id=display_id)
        await query.edit_message_text(money_frozen_txt)

        btn_txt = await get_text(deal['seller'], "transfer_btn")
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(btn_txt, callback_data=f"transfer_{deal_id}")]])
        
        seller_notify_txt = await get_text(deal['seller'], "seller_notify_pay", buyer=deal['buyer_username'], id=display_id)
        await context.bot.send_message(deal['seller'], seller_notify_txt, reply_markup=keyboard)

    elif data.startswith("transfer_"):
        deal_id = int(data.split("_")[1])
        deal = await get_deal(deal_id)
        if not deal or deal['status'] != "деньги заморожены": 
            await query.edit_message_text("❌ Ошибка.")
            return
        
        await update_deal_status(deal_id, "передано")
        display_id = deal_id + 458
        
        transfer_ok_txt = await get_text(uid, "transfer_ok")
        await query.edit_message_text(transfer_ok_txt)
        
        btn_txt = await get_text(deal['buyer_id'], "confirm_btn")
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(btn_txt, callback_data=f"confirm_{deal_id}")]])
        try: 
            buyer_notify_txt = await get_text(deal['buyer_id'], "buyer_notify_transfer", id=display_id)
            await context.bot.send_message(deal['buyer_id'], buyer_notify_txt, reply_markup=keyboard)
        except Exception as e: 
            logging.error(f"Failed to notify buyer transfer: {e}")

    elif data.startswith("confirm_"):
        deal_id = int(data.split("_")[1])
        deal = await get_deal(deal_id)
        if not deal or deal['status'] != "передано": 
            await query.edit_message_text("❌ Ошибка.")
            return
        
        await update_deal_status(deal_id, "завершена")
        
        pay = deal['payment']
        if "Рубли" in pay: await update_balance(deal['seller'], "balance_rub", deal['price'])
        elif "USDT" in pay: await update_balance(deal['seller'], "balance_usd", deal['price'])
        else: await update_balance(deal['seller'], "balance_stars", deal['price'])
        
        display_id = deal_id + 458
        confirm_ok_txt = await get_text(uid, "confirm_ok", id=display_id)
        await query.edit_message_text(confirm_ok_txt)
        
        seller_notify_txt = await get_text(deal['seller'], "seller_notify_confirm", id=display_id, price=deal['price'], pay=pay)
        await context.bot.send_message(deal['seller'], seller_notify_txt)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    unknown_txt = await get_text(uid, "unknown")
    kb = await main_menu_keyboard(uid)
    await update.message.reply_text(unknown_txt, reply_markup=kb)

async def post_init(application: Application):
    await init_db()

def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rub", rub_command))
    app.add_handler(CommandHandler("usd", usd_command))
    app.add_handler(CommandHandler("stars", stars_command))
    
    button_filter = r"^(💼 Профиль|➕ Создать сделку|📊 Реферальная ссылка|🌐 Change language|🆘 Поддержка|💼 Profile|➕ Create deal|📊 Referral link|🆘 Support|🇷🇺 Рубли \(карта\)|💵 USDT \(крипта\)|⭐ Звёзды \(Telegram\)|🇷🇺 RUB \(card\)|💵 USDT \(crypto\)|⭐ Stars \(Telegram\)|🔙 Назад|🔙 Back)$"
    
    app.add_handler(MessageHandler(filters.Regex(button_filter), handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("🏔️ NORDNFT Bot запущен. Используется aiosqlite...")
    app.run_polling()

if __name__ == "__main__":
    main()
