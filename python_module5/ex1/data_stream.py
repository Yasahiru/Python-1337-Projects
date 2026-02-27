from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict, Union


class DataStream(ABC):

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        ...

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        ...

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        ...


class SensorStream(DataStream):
    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        ...

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        try:
            for data in data_batch:
                if isinstance(data, Union[int, float]) is not True:
                    pass
        except Exception as e:
            print(e)


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

# SUUNY123456789@ha.
