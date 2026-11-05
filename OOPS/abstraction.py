from abc import ABC, abstractmethod
from datetime import datetime

class Logger(ABC):
    def __init__(self, level: str):
        self._level = level

    # Abstract method: subclasses decide HOW to deliver the message
    @abstractmethod
    def log(self, message: str) -> None:
        pass

    # Concrete method: shared formatting logic inherited by all subclasses
    def format_message(self, message: str) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] [{self._level}] {message}"

class ConsoleLogger(Logger):
    def __init__(self, level: str):
        super().__init__(level)

    def log(self, message: str) -> None:
        print(self.format_message(message))

class FileLogger(Logger):
    def __init__(self, level: str, file_path: str):
        super().__init__(level)
        self._file_path = file_path

    def log(self, message: str) -> None:
        # In production, this would write to a file
        print(f"Writing to {self._file_path}: {self.format_message(message)}")