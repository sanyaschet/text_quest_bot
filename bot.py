import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

ANSWER_OK = {"тайланд", "thailand", "thai", "таиланд", "тай"}

HINTS = [
    """ПОДСКАЗКА 1
Обнаружены признаки внешнего следа, не относящегося к визуальному типу данных. Анализ показывает несоответствие между формой носителя и его содержимым. Система фиксирует вероятность присутствия ароматического маркера. Источник сигнала может быть связан с памятью места происхождения.""",
    """ПОДСКАЗКА 2
Декодирование невозможно в текущем режиме наблюдения. Для извлечения сигнала требуется нарушение целостности носителя. Доступ к данным открывается только после прямого контакта с внутренним слоем.""",
    """ПОДСКАЗКА 3
Сигнал относится к категории внешних сувенирных маркеров. Фиксируется устойчивая связь с юго-восточным региональным контуром. В архиве присутствует соответствие с ранее зафиксированным подарочным объектом: ароматическая мазь.""",
]

user_hint_level = {}  # user_id -> 0..3


def keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💡 подсказка 💡", callback_data="hint")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_hint_level[user_id] = 0

    await update.message.reply_text(
        """Добро пожаловать в ТАЙНЫЙ АРХИВ СКРЫТЫХ СЛОЁВ.
Предоставьте источник происхождения зафиксированного следа. Система принимает только идентификатор события, с которым он совпадает. Он извлекается отдельно через внешний контур подтверждения. При успешном совпадении будет выдан фрагмент восстановленного сообщения.""",
        reply_markup=keyboard()
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = (update.message.text or "").strip().lower()

    if any(ans in text for ans in ANSWER_OK):
        await update.message.reply_text("""✔️ СОВПАДЕНИЕ ПОДТВЕРЖДЕНО
Внешний след идентифицирован корректно. Источник сигнала: тайский региональный контур

<b>Фрагмент следа из архива восстановлен: А Д М С Е Н И Г Я</b>


Доступ к следующему узлу открыт. Идентификатор следующей проверки закреплён в системе.
Точка перехода: БОЯТЬСЯ ВСЕМ
""", parse_mode="HTML")
    else:
        await update.message.reply_text("""❌ СОВПАДЕНИЕ НЕ ОБНАРУЖЕНО
Источник не соответствует зафиксированному следу. Система отклоняет результат. Попробуй иначе. След остаётся неизменным.""", reply_markup=keyboard())


async def handle_hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    level = user_hint_level.get(user_id, 0)

    if level >= len(HINTS):
        await query.message.reply_text("Подсказок больше нет")
        return

    await query.message.reply_text(HINTS[level])
    user_hint_level[user_id] = level + 1


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CallbackQueryHandler(handle_hint, pattern="hint"))

app.run_polling()