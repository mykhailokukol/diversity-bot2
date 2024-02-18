from pymongo import MongoClient
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.config import settings
from bot.keyboards import (
    action_keyboard,
    action_keyboard_ru,
    language_keyboard,
    set_geo_keyboard,
    set_geo_keyboard_ru,
)

ACTION, NICKNAME, GEO, SOURCE, VOLUME, FINISH = range(6)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    client = MongoClient(settings.MONGODB_CLIENT_URL)
    db = client["empirepartnersbot"]
    participants = db["participants"]
    participant = participants.find_one({"user_id": update.effective_user.id})
    if participant:
        await update.message.reply_text(
            "Вы уже учавствуете в розыгрыше.\n\nYou already take a part in the draw."
        )
        return ConversationHandler.END

    reply_markup = ReplyKeyboardMarkup(language_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Выберите язык/Choose your language",
        reply_markup=reply_markup,
    )
    return ACTION


async def action(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    context.user_data["localization"] = update.message.text

    match context.user_data["localization"]:
        case "Русский":
            text = "Привет!\nЕсли ты здесь, значит принял участие в арбитражном турнире для партнеров от Empire Partners!\nЧтобы поучаствовать в розыгрыше, нужно выполнить всего одно простое действие – заполнить анкету"
            keyboard = action_keyboard_ru
        case "English":
            text = "Hey!\nIf you are here, it means you took part in the arbitration tournament for partners from Empire Partners!\nTo participate in a draw you need to do only one simple step – fill out the form"
            keyboard = action_keyboard

    reply_markup = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
    )
    return NICKNAME


async def set_nickname(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:

    match context.user_data["localization"]:
        case "Русский":
            text = "Укажите Ваш логин в Telegram"
        case "English":
            text = "Provide your Telegram login"

    reply_markup = ReplyKeyboardRemove()
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
    )

    return GEO


async def set_geo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    context.user_data["nickname"] = update.message.text

    match context.user_data["localization"]:
        case "Русский":
            text = "Укажите Ваше ГЕО"
            reply_markup = ReplyKeyboardMarkup(set_geo_keyboard_ru)
        case "English":
            text = "Specify your GEO"
            reply_markup = ReplyKeyboardMarkup(set_geo_keyboard)

    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
    )

    return SOURCE


async def set_source(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    context.user_data["geo"] = update.message.text

    match context.user_data["localization"]:
        case "Русский":
            text = "Укажите Ваш источник трафика"
        case "English":
            text = "Specify your traffic source"

    reply_markup = ReplyKeyboardRemove()
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
    )

    return VOLUME


async def set_volume(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    context.user_data["source"] = update.message.text

    match context.user_data["localization"]:
        case "Русский":
            text = "Укажите Ваш объем трафика в месяц"
        case "English":
            text = "Specify you traffic volume per month"

    reply_markup = ReplyKeyboardRemove()
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
    )

    return FINISH


async def finish(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    context.user_data["volume"] = update.message.text

    participant = {
        "user_id": update.effective_user.id,
        "langauge": context.user_data["localization"],
        "nickname": context.user_data["nickname"],
        "geo": context.user_data["geo"],
        "source": context.user_data["source"],
        "volume": context.user_data["volume"],
    }

    client = MongoClient(settings.MONGODB_CLIENT_URL)
    db = client["empirepartnersbot"]
    participants = db["participants"]
    participants.insert_one(participant)

    match context.user_data["localization"]:
        case "Русский":
            text = "Готово!\nОсталась самая тяжелая часть – ожидание...\nМы обязательно вернемся и сообщим тебе о результатах!\nСпасибо за участие!"
        case "English":
            text = "All done!\nWe will return with the results soon!\nThanks for taking part!"

    await update.message.reply_text(text)

    return ConversationHandler.END


async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> ConversationHandler.END:
    print("cancel")
    return ConversationHandler.END
