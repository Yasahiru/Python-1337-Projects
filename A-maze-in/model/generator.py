from abc import ABC, abstractmethod


class Generator(ABC):
    @abstractmethod
    def generate() -> None:
        ...
