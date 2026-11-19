#Журнал ошибок ввода пользователя с сохранением в память и файл.

import datetime
from constants import LOG_FILE

_entries: list[str] = []


def log_error(message: str) -> None:
    "Добавить запись об ошибке в журнал и дописать в файл LOG_FILE."
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] {message}"
    _entries.append(entry)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except OSError:
        pass


def get_entries() -> list[str]:
    """Вернуть копию журнала в памяти."""
    return list(_entries)


def clear() -> None:
    """Очистить журнал (используется в тестах)."""
    _entries.clear()