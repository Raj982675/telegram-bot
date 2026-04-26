from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ChatJoinRequestHandler, ContextTypes

BOT_TOKEN = "8326537665:AAFMAuwNAFPVxrraucX07TXZ17SAFN1g-Yo"

verified_users = set()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ I am not a robot", callback_data="verify")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Click below to verify 👇",
        reply_markup=reply_markup
    )

# button click
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    verified_users.add(user_id)

    await query.answer()
    await query.edit_message_text("✅ You are verified! Now join the channel.")

# join request handler
async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request
    user_id = req.from_user.id

    if user_id in verified_users:
        await context.bot.approve_chat_join_request(req.chat.id, user_id)
    else:
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ IF YOU WANT TO EARN DAILY 5K-10K EASY THEN CONTACT @sonu2662."
            )
        except:
            pass

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(verify, pattern="verify"))
app.add_handler(ChatJoinRequestHandler(join_request))

app.run_polling()
