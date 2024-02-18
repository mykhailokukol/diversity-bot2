import logging

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.base import (
    ACTION,
    FINISH,
    GEO,
    NICKNAME,
    SOURCE,
    VOLUME,
    action,
    cancel,
    finish,
    set_geo,
    set_nickname,
    set_source,
    set_volume,
    start,
)
from bot.config import settings

logging.basicConfig(
    format="%(levelname)s | %(name)s | %(asctime)s | %(message)s", level=logging.INFO
)
log = logging.getLogger(__name__)


def main() -> None:
    app = ApplicationBuilder().token(settings.TG_API_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ACTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, action)],
            NICKNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_nickname)],
            GEO: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_geo)],
            SOURCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_source)],
            VOLUME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_volume)],
            FINISH: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    app.add_handler(conv_handler)

    app.run_polling()


if __name__ == "__main__":
    main()
