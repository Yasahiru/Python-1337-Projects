from collections.abc import Callable
from functools import wraps
import time


def spell_timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Casting {func.__name__}...")
        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()
        print(f"Spell completed in {end - start:.3f} seconds")

        return result
    return wrapper


def power_validator(min_power: int) -> Callable:
    ...


def retry_spell(max_attempts: int) -> Callable:
    ...


class MageGuild:
    ...

    @staticmethod
    def validate_mage_name(name: str) -> bool:
        ...

    def cast_spell(self, spell_name: str, power: int) -> str:
        ...


def main() -> None:
    ...


if __name__ == "__main__":
    main()
