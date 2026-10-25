# ****************************************
# Mã sinh viên: 20237381
# Họ tên: Đỗ Đình Quân
# ****************************************
"""Các chiến lược lựa chọn (Strategy) dạng generic."""

from abc import ABC, abstractmethod
from typing import Callable, Generic, Sequence, TypeVar

from exceptions import NoSuitableItemException

T = TypeVar("T")  # Kiểu phần tử được chọn


class ISelectionStrategy(ABC, Generic[T]):
    """Interface chiến lược chọn một phần tử tốt nhất từ danh sách ứng viên."""

    @abstractmethod
    def select(self, candidates: Sequence[T]) -> T:
        """Chọn một phần tử. Ném NoSuitableItemException nếu danh sách rỗng."""


class HighestPriorityStrategy(ISelectionStrategy[T]):
    """Chọn phần tử có điểm ưu tiên cao nhất (hàm tính điểm truyền từ ngoài)."""

    def __init__(self, score_selector: Callable[[T], float]):
        if score_selector is None:
            raise ValueError("score_selector không được None")
        self._score_selector = score_selector

    def select(self, candidates: Sequence[T]) -> T:
        if not candidates:
            raise NoSuitableItemException()
        # max() không sửa danh sách đầu vào; điểm bằng nhau thì lấy phần tử đứng trước
        return max(candidates, key=self._score_selector)


class FirstAvailableStrategy(ISelectionStrategy[T]):
    """Chọn phần tử đầu tiên trong danh sách ứng viên."""

    def select(self, candidates: Sequence[T]) -> T:
        if not candidates:
            raise NoSuitableItemException()
        return candidates[0]