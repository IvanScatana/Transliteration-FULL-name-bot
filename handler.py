import logging 

from aiogram.filters import CommandStart, Command
from aiogram import Router, F
from aiogram.types import Message

logger = logging.getLogger(__name__)

router = Router()

transliteration_dict = {
    "а":"a",
    "б":"b",
    "в":"v",
    "г":"g",
    "д":"d",
    "е":"e",
    "ё":"e",
    "ж":"zh",
    "з":"z",
    "и":"i",
    "й":"i",
    "к":"k",
    "л":"l",
    "м":"m",
    "н":"n",
    "о":"o",
    "п":"p",
    "р":"r",
    "с":"s",
    "т":"t",
    "у":"u",
    "ф":"f",
    "х":"kh",
    "ц":"ts",
    "ч":"ch",
    "ш":"sh",
    "щ":"shch",
    "ы":"y",
    "ъ":"ie",
    "э":"e",
    "ю":"iu",
    "я":"ia" 
}


def append_to_file(message, path = "messages.txt"):
    with open(path, mode = "a", encoding = "utf-8") as file:
        file.write(message + "\n")
    return True


@router.message(CommandStart()) # /start
async def cmd_start(message:Message):
    user = message.from_user
    logger.info(f"Пользователь @{user.username} запустил бота")
    await message.answer("Привет!\n" \
    "Я помогу тебе перевести ФИО c русского на английский язык.\n" \
    "Введи ФИО:")

@router.message(F.text) # <ФИО>
async def transliteration_full_name(message:Message):
    user = message.from_user
    original_text = message.text.strip()
    logger.info(f"Получено сообщение от @{user.username}: {original_text}")
    full_name = original_text.lower()
    if len(full_name.split()) == 3:
        english_full_name = ""
        valid_input = True
        for char  in full_name:
            if char  == " " or char == "-":
                english_full_name += char 
            else:
                try:
                    english_full_name += transliteration_dict[char]
                except KeyError:
                    logger.warning(f"Пользователь @{user.username} ввёл недопустимый символ: {char}")
                    await message.answer("Вы ввели некорректные знаки, ая-яй, используй бот по назначению.\n" \
                    "Попробуй ещё:")
                    valid_input = False
                    break
        if valid_input:
            name_parts = english_full_name.split()
            capitalized_parts = []
            for part in name_parts:
                if '-' in part:
                    subparts = part.split('-')
                    capitalized_subparts = [sub.capitalize() for sub in subparts]
                    capitalized_parts.append('-'.join(capitalized_subparts))
                else:
                    capitalized_parts.append(part.capitalize())
            result = " ".join(capitalized_parts)
            logger.info(f"Транслитерация для @{user.username}: {original_text} -> {result}")
            await message.answer(result)
    else:
        logger.warning(f"Пользователь @{user.username} ввёл ФИО в неверном формате: {original_text}")
        await message.answer("Извини, но возможно ты ошибся при наборе ФИО.\n" \
        "Попробуй ещё:")


    text = f"{user.first_name} {user.last_name}: {message.text}"
    append_to_file(text)    
