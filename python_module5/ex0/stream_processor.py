from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return f"Output: Processed {result}"


class NumericProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        res: str = ""
        print(f"Processing data: {data}")
        if self.validate(data) is True:
            print("Validation: Numeric data verified")
            _values: int = len(data)
            _sum: int = sum(data)
            _avg: float = round(_sum / _values, 2)
            res = f"{_values} numeric values , sum={_sum}, avg={_avg}"
        else:
            res = "[Error]"
        return self.format_output(res)

    def validate(self, data: Any) -> bool:
        try:
            iter(data)
            for element in data:
                int(element)
            return True
        except Exception:
            return False

    def format_output(self, result: str) -> str:
        return super().format_output(result)


class TextProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        print(f"Processing data: \"{data}\"")
        res: str = ""
        if self.validate(data) is True:
            print("Validation: Text data verified")
            words: int = data.split(" ")
            carachters: int = len(data)
            res = f" text: {carachters} characters, {len(words)} words"
        else:
            res = "[Error]"
        return self.format_output(res)

    def validate(self, data: Any) -> bool:
        try:
            data.capitalize()
            return True
        except Exception:
            return False

    def format_output(self, result: str) -> str:
        return super().format_output(result)


class LogProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        if self.validate(data) is True:
            pass
        else:
            print("Error LogProcess")

    def validate(self, data: Any) -> bool:
        try:
            logs: list[str] = ["ERROR", "INFO", "WARNING"]
            _data = data.split(":")
            for log in logs:
                if _data[0] == log:
                    return True
            return False
        except Exception:
            return False

    def format_output(self, result: str) -> str:
        return super().format_output(result)


def stream_processor() -> None:
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")

    # initializing: list[str] = [
    #     "Initializing Numeric Processor...",
    #     "Initializing Text Processor...",
    #     "Initializing Log Processor..."
    # ]

    # for initializ in zip(initializing):
    print("=== Polymorphic Processing Demo ===")


def main() -> None:
    stream_processor()


if __name__ == "__main__":
    main()
