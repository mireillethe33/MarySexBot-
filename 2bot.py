import asyncio
import html
import random

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, User

TOKEN = "8632369243:AAH_ShawSOsllVkuFuL0M4-YOv1l36_uAiI"

bot = Bot(token=TOKEN, default=None)
dp = Dispatcher()

# {a} — кто отправил команду, {b} — на кого направлена
REPLIES = [
    "😏 {a} подмигнул(а) {b} и предложил(а) сбежать на свидание.",
    "💘 {a} дарит {b} букет виртуальных роз.",
    "🔥 Между {a} и {b} пробежала искра! Пожарные уже выехали.",
    "🍷 {a} приглашает {b} на романтический ужин при свечах.",
    "🙈 {b} покраснел(а), когда {a} сделал(а) такое предложение.",
    "😳 {a} смутил(а) {b} так, что у бота перегрелся процессор.",
    "💌 {a} отправил(а) {b} любовное письмо на 10 страниц.",
    "🌚 {a} и {b} гуляют под луной и болтают обо всём на свете.",
    "🎲 Бросаю кубик для {a} и {b}... выпало: «Сначала чай!»",
    "😎 {a} включил(а) всё своё обаяние на {b}. Эффективность 100%.",
    "🐱 {a} мурлычет в сторону {b}. Мяу!",
    "🧯 {a} зажёг(ла), а {b} ищет огнетушитель.",
    "🍫 {a} протягивает {b} шоколадку и говорит: «Ты душка».",
    "🎭 {a} разыгрывает сцену из мелодрамы для {b}.",
    "🚀 {a} похищает {b} на ракете в страну романтики.",
    "👀 {b}, кажется, {a} на тебя положил(а) глаз...",
    "🤖 Бот-сваха говорит: {a} + {b} = идеальная пара!",
    "💃 {a} приглашает {b} на танец. Играет медляк.",
    "😇 {a} клянётся, что намерения у него(неё) самые честные, {b}.",
    "🥂 {a} поднимает бокал за {b}: «За тебя, красавчик(ца)!»",
]

COMMANDS = ("sex", "minet")


def mention(user: User) -> str:
    name = html.escape(user.full_name)
    return f'<a href="tg://user?id={user.id}">{name}</a>'


def get_target(message: Message, command: CommandObject):
    """Возвращает HTML-упоминание цели: из reply или из @username."""
    if message.reply_to_message and message.reply_to_message.from_user:
        return mention(message.reply_to_message.from_user)

    # Упоминания @username и text_mention в тексте сообщения
    for ent in message.entities or []:
        if ent.type == "text_mention" and ent.user:
            return mention(ent.user)
        if ent.type == "mention":
            username = message.text[ent.offset : ent.offset + ent.length]
            return html.escape(username)

    if command.args and command.args.strip().startswith("@"):
        return html.escape(command.args.split()[0])
    return None


@dp.message(Command(*COMMANDS))
async def cmd_action(message: Message, command: CommandObject):
    target = get_target(message, command)
    if not target:
        await message.answer(
            f"Используй так: /{command.command} @username\n"
            "или ответь командой на сообщение человека."
        )
        return

    text = random.choice(REPLIES).format(a=mention(message.from_user), b=target)
    await message.answer(text, parse_mode="HTML")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
