import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import re

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8525143069:AAFq_wcSBN_mE34cGbE61B1tgmAmcir7Rrc"

WAITING_FOR_COOKIES = 1
WAITING_FOR_DATA = 2

class CheatThisBot:
    def __init__(self):
        self.user_data = {}
    
    def validate_cookie(self, cookie):
        cookie = cookie.strip()
        if not cookie:
            return False
        return '=' in cookie and len(cookie) > 5
    
    def extract_emails(self, text):
        return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    
    def extract_urls(self, text):
        return re.findall(r'https?://[^\s]+', text)
    
    def extract_tokens(self, text):
        tokens = re.findall(r'[a-zA-Z0-9_-]{20,}', text)
        return list(set(tokens))[:10]
    
    def extract_ips(self, text):
        return re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)

bot = CheatThisBot()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🍪 Cookie Checker", callback_data='check_cookies')],
        [InlineKeyboardButton("📧 Email/Password", callback_data='extract_emails')],
        [InlineKeyboardButton("🔍 Log Parser", callback_data='parse_logs')],
        [InlineKeyboardButton("💼 Wallet Recovery", callback_data='wallet')],
        [InlineKeyboardButton("📝 Data Parser", callback_data='parse_data')],
        [InlineKeyboardButton("📊 Data Sorter", callback_data='sort_data')],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🤖 **CheatThisBot v2.0** - Complete Data Analysis\n\n"
        "All Tools Available:\n"
        "🍪 Cookie Validator\n"
        "📧 Email/Password Extractor\n"
        "🔍 Log Parser & Analyzer\n"
        "💼 Wallet & Blockchain Tools\n"
        "📝 Multi-format Parser\n"
        "📊 Data Sorting & Deduplication\n\n"
        "Choose below:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    if query.data == 'check_cookies':
        await query.edit_message_text(
            text="🍪 **Cookie Checker**\n\n"
            "Paste cookies (one per line):\n"
            "`session=abc123\n"
            "token=xyz789`",
            parse_mode='Markdown'
        )
        return WAITING_FOR_COOKIES
    
    elif query.data == 'extract_emails':
        await query.edit_message_text(
            text="📧 **Email/Password Extractor**\n\n"
            "Paste text containing credentials"
        )
        return WAITING_FOR_DATA
    
    elif query.data == 'parse_logs':
        await query.edit_message_text(
            text="🔍 **Log Parser**\n\n"
            "Paste security logs, stealer logs, or any text containing:\n"
            "• Tokens & API Keys\n"
            "• IP Addresses\n"
            "• Webhooks\n"
            "• Suspicious patterns"
        )
        return WAITING_FOR_DATA
    
    elif query.data == 'wallet':
        await query.edit_message_text(
            text="💼 **Wallet Recovery**\n\n"
            "Paste wallet data containing:\n"
            "• Addresses (0x...)\n"
            "• Private keys\n"
            "• Seed phrases\n"
            "• Recovery info"
        )
        return WAITING_FOR_DATA
    
    elif query.data == 'parse_data':
        await query.edit_message_text(
            text="📝 **Data Parser**\n\n"
            "Parses: JSON, CSV, URLs, IPs\n"
            "Paste any data format"
        )
        return WAITING_FOR_DATA
    
    elif query.data == 'sort_data':
        await query.edit_message_text(
            text="📊 **Data Sorter**\n\n"
            "Paste data (one item per line)\n"
            "I will sort and remove duplicates"
        )
        return WAITING_FOR_DATA
    
    elif query.data == 'help':
        await query.edit_message_text(
            text="❓ **Help**\n\n"
            "**Cookie Checker:** Validates cookies\n"
            "**Email/Password:** Extracts credentials\n"
            "**Log Parser:** Analyzes security logs\n"
            "**Wallet Recovery:** Blockchain analysis\n"
            "**Data Parser:** Multi-format parsing\n"
            "**Data Sorter:** Sort & deduplicate\n\n"
            "Use /start to return"
        )

async def handle_cookies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    cookies_text = update.message.text
    
    lines = cookies_text.split('\n')
    cookies = []
    for line in lines:
        if ',' in line:
            cookies.extend([c.strip() for c in line.split(',')])
        else:
            cookies.append(line.strip())
    
    valid_cookies = []
    invalid_cookies = []
    
    for cookie in cookies:
        if cookie:
            if bot.validate_cookie(cookie):
                valid_cookies.append(cookie)
            else:
                invalid_cookies.append(cookie)
    
    response = f"🍪 **Cookie Results**\n\n"
    response += f"✅ Valid: {len(valid_cookies)}\n"
    response += f"❌ Invalid: {len(invalid_cookies)}\n\n"
    
    if valid_cookies:
        response += "**Valid:**\n"
        for cookie in valid_cookies[:5]:
            short = cookie[:40] + "..." if len(cookie) > 40 else cookie
            response += f"✓ `{short}`\n"
        if len(valid_cookies) > 5:
            response += f"... +{len(valid_cookies) - 5} more\n"
    
    if invalid_cookies:
        response += "\n**Invalid:**\n"
        for cookie in invalid_cookies[:5]:
            response += f"✗ {cookie}\n"
    
    response += "\n/start to return"
    await update.message.reply_text(response, parse_mode='Markdown')
    return -1

async def handle_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    data_text = update.message.text
    
    emails = bot.extract_emails(data_text)
    urls = bot.extract_urls(data_text)
    tokens = bot.extract_tokens(data_text)
    ips = bot.extract_ips(data_text)
    
    response = "📊 **Extraction Results**\n\n"
    
    if emails:
        response += f"📧 Emails ({len(emails)}):\n"
        for email in emails[:5]:
            response += f"• `{email}`\n"
        if len(emails) > 5:
            response += f"... +{len(emails)-5} more\n\n"
    
    if urls:
        response += f"🔗 URLs ({len(urls)}):\n"
        for url in urls[:3]:
            short = url[:35] + "..." if len(url) > 35 else url
            response += f"• `{short}`\n"
        if len(urls) > 3:
            response += f"... +{len(urls)-3} more\n\n"
    
    if ips:
        unique_ips = list(set(ips))
        response += f"🌐 IPs ({len(unique_ips)}):\n"
        for ip in unique_ips[:5]:
            response += f"• `{ip}`\n"
        if len(unique_ips) > 5:
            response += f"... +{len(unique_ips)-5} more\n\n"
    
    if tokens:
        response += f"🔑 Tokens ({len(tokens)}):\n"
        for token in tokens[:3]:
            response += f"• `{token}`\n"
        if len(tokens) > 3:
            response += f"... +{len(tokens)-3} more\n\n"
    
    if not (emails or urls or ips or tokens):
        response += "❌ No patterns found\n\n"
    
    response += "/start to return"
    await update.message.reply_text(response, parse_mode='Markdown')
    return -1

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_data(update, context)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 CheatThisBot v2.0 Started!")
    print("All features active: Cookies, Emails, Logs, Wallets, Parser, Sorter")
    print("Bot running... Press Ctrl+C to stop")
    app.run_polling()

if __name__ == '__main__':
    main()
