from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict, Union


class DataStream(ABC):

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        ...

    @abstractmethod
    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        ...

    @abstractmethod
    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        ...


class SensorStream(DataStream):
    ...


class TransactionStream(DataStream):
    ...


class EventStream(DataStream):
    ...


class StreamProcessor(DataStream):
    ...


class StreamManager():
    ...


def main():
    DataStream


if __name__ == "__main__":
    main()
