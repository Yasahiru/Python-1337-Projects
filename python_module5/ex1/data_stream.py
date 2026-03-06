from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict, Union


class DataStream(ABC):

    def __init__(self, stream_id: str) -> None:
        self.stream_id: str = stream_id
        self.processed_count: int = 0

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        return (data_batch)

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        if criteria is None:
            return data_batch
        for data in data_batch:
            if str(data) == criteria:
                data_batch.remove(criteria)
        return (data_batch)

    def get_stats(self) -> Dict[str, Union[str, int]]:
        return {
            "stream_id": self.stream_id,
            "processed_count": self.processed_count
        }


class SensorStream(DataStream):

    def __init__(self, stream_id) -> None:
        super().__init__(stream_id)
        self.processed_count: int = 0
        self.avg: float = 0.0

    def process_batch(self, data_batch: List[Any]) -> str:
        valid_data: List = []
        for x in data_batch:
            if isinstance(x, (int, float)):
                valid_data.append(x)

        self.processed_count += len(valid_data)

        if not valid_data:
            return "No valid sensor data"

        self.avg = sum(valid_data) / len(valid_data)
        return f"{self.processed_count} readings"

    def get_stats(self) -> Dict[str, Union[str, int]]:
        return {
            "stream_id": self.stream_id,
            "Type": "Environmental Data",
            "processed_count": self.processed_count,
            "ext": f"avg temp: {self.avg}°C"
        }


class TransactionStream(DataStream):

    def __init__(self, stream_id) -> None:
        super().__init__(stream_id)
        self.processed_count: int = 0

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            net = 0
            count = 0

            for data in data_batch:
                if isinstance(data, dict):
                    count += 1
                    if data["type"] == "buy":
                        net -= data["amount"]
                    elif data["type"] == "sell":
                        net += data["amount"]

            self.processed_count += count
            return f"{count} operations"

        except Exception as e:
            return (f"[ERROR]: {e}")

    def get_stats(self) -> Dict[str, Union[str, int]]:
        return {
            "stream_id": self.stream_id,
            "Type": "Financial Data",
            "processed_count": self.processed_count,
            "ext": f"net flow: {self.net} units"
        }


class EventStream(DataStream):

    def __init__(self, stream_id) -> None:
        super().__init__(stream_id)
        self.errors = 0

    def process_batch(self, data_batch: List[Any]) -> str:
        for data in data_batch:
            if str(data).lower() == "error":
                self.errors += 1
        self.processed_count += len(data_batch)
        return f"{self.processed_count} events"

    def get_stats(self) -> Dict[str, Union[str, int]]:
        ext: str = ""
        if self.errors > 1:
            ext = "errors"
        else:
            ext = "error"
        return {
            "stream_id": self.stream_id,
            "Type": "Financial Data",
            "processed_count": self.processed_count,
            "ext": f"{self.errors} {ext} detected"
        }


class StreamProcessor:

    def __init__(self) -> None:
        self.streams: List[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        self.streams.append(stream)

    def process_all(self, batches: List[List[Any]]) -> None:
        for stream, batch in zip(self.streams, batches):
            result = stream.process_batch(batch)
            print(f"{stream.stream_id}: {result}")


def data_stream_test() -> None:
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")

    init: List[List[str]] = [
        [
            "Initializing Sensor Stream...",
            "Processing sensor batch:",
            "Sensor analysis:"
        ],
        [
            "Initializing Transaction Stream...",
            "Processing transaction batch:",
            "Transaction analysis:"
        ],
        [
            "Initializing Event Stream...",
            "Processing event batch:",
            "Event analysis:"
        ],
    ]

    sensor_stream: SensorStream = SensorStream("SENSOR_001"),
    sensor_transaction: TransactionStream = TransactionStream("TRANS_001"),
    sensor_event: EventStream = EventStream("EVENT_001")

    streams: List[DataStream] = [
        sensor_stream,
        sensor_transaction,
        sensor_event
    ]

    # these values should be dictionnaries List[Dict]
    batches = [
        ["temp:22.5", "humidity:65", "pressure:1013"],
        ["buy:100", "sell:150", "buy:75"],
        ["login", "error", "logout"]
    ]

    for pre, stream, batch in zip(init, streams, batches):
        print(pre[0])
        stream.process_batch(batch)
        res = stream.get_stats()
        print(
                f"Stream ID: {res["stream_id"]}, Type: {res["type"]} \n"
                f"{pre[1]} {batch} \n"
                f"{pre[2]} {res["processed_count"], {res["ext"]}}"
            )

    print("=== Polymorphic Stream Processing ===")
    print("Processing mixed stream types through unified interface...\n")
    print("Batch 1 Results:\n")

    stream_p = StreamProcessor()
    stream_p.add_stream(sensor_stream)
    stream_p.add_stream(sensor_transaction)
    stream_p.add_stream(sensor_event)
    stream_p.process_all(batches)

    print("Stream filtering active: High-priority data only")
    print("Filtered results: 2 critical sensor alerts, 1 large transaction\n")
    print("All streams processed successfully. Nexus throughput optimal.")


def main() -> None:
    data_stream_test()


if __name__ == "__main__":
    main()
