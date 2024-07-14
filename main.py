import logging
import asyncio
from pathlib import Path
import importlib
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token="Ваш ТОКЕН")
dp = Dispatcher(bot=bot, storage=MemoryStorage())

def load_modules(module_name, dp):
    try:
        for filename in module_name.glob('*.py'):
            try:
                if hasattr(importlib.import_module(f"{module_name.relative_to(Path('.')).with_suffix('')}.{filename.stem}".replace("\\", '.').replace('/', '.')), 'setup'):
                    importlib.import_module(f"{module_name.relative_to(Path('.')).with_suffix('')}.{filename.stem}".replace("\\", '.').replace('/', '.')).setup(dp)
            except ImportError as e:
                logging.error(f"Ошибка при импорте модуля " +
                              f"{module_name.relative_to(Path('.')).with_suffix('')}.{filename.stem}".replace("\\", '.').replace('/', '.')+f" : {e}")
    except Exception as e:
        logging.error(f"Ошибка при загрузке модуля {module_name}: {e}")

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        logging.info("Загрузка модулей...")
        for module_name in ["commands", "button"]:
            load_modules(Path(f'./{module_name}'), dp)
            for subdirectory in Path(f'./{module_name}').glob('*/'):
                load_modules(subdirectory, dp)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except Exception as e:
        logging.error(f"Ошибка при загрузке модуля: {e}")
    finally:
        logging.info("Модули загружены.")
