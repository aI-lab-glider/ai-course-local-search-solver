from typing import Generic, List, TypeVar
THistoryItem = TypeVar("THistoryItem")


class History(Generic[THistoryItem]):
    def __init__(self, size: int):
        self._max_size = size
        self._items: List[THistoryItem] = []

    def append(self, item: THistoryItem) -> None:
        if len(self._items) == self._max_size:
            self._items = [item] + self._items[1:]
        else:
            self._items.append(item)

    def __getitem__(self, index: int) -> THistoryItem:
        return self._items[index]

    def __iter__(self):
        return iter(self._items)

    def is_full(self):
        return len(self._items) == self._max_size
