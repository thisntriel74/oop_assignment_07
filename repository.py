# ****************************************
# Mã sinh viên: 20237381
# Họ tên: Đỗ Đình Quân
# ****************************************
"""Kho lưu trữ tổng quát (generic repository)."""

from abc import ABC, abstractmethod
from typing import Callable, Generic, List, Optional, TypeVar

from device import IIdentifiable
from exceptions import DuplicateIdException

# Tham số kiểu T: bắt buộc là kiểu có Id (constraint giống where T : IIdentifiable)
T = TypeVar("T", bound=IIdentifiable)


class IRepository(ABC, Generic[T]):
    """Interface kho lưu trữ cho mọi kiểu đối tượng có Id."""

    @abstractmethod
    def add(self, item: T) -> None:
        """Thêm phần tử vào kho."""

    @abstractmethod
    def remove(self, item_id: str) -> bool:
        """Xóa phần tử theo mã. Trả về False nếu không tìm thấy."""

    @abstractmethod
    def find_by_id(self, item_id: str) -> Optional[T]:
        """Tìm theo mã. Trả về None nếu không tìm thấy."""

    @abstractmethod
    def get_all(self) -> List[T]:
        """Lấy toàn bộ phần tử (bản sao, không lộ collection nội bộ)."""

    @abstractmethod
    def find_all(self, condition: Callable[[T], bool]) -> List[T]:
        """Lọc các phần tử thỏa điều kiện."""


class InMemoryRepository(IRepository[T]):
    """Kho lưu trữ trong bộ nhớ, cài đặt bằng dict {Id: phần tử}.

    Dùng dict để tìm theo mã nhanh (O(1)) và kiểm tra trùng Id dễ dàng.
    """

    def __init__(self):
        self._items = {}  # dict[str, T]

    def add(self, item: T) -> None:
        if item is None:                      # Không chấp nhận null
            raise ValueError("Không được thêm phần tử None vào kho")
        if item.id in self._items:            # Không cho trùng Id
            raise DuplicateIdException(item.id)
        self._items[item.id] = item

    def remove(self, item_id: str) -> bool:
        # pop trả về None nếu không có -> dùng giá trị mặc định để phân biệt
        return self._items.pop(item_id, None) is not None

    def find_by_id(self, item_id: str) -> Optional[T]:
        return self._items.get(item_id)

    def get_all(self) -> List[T]:
        return list(self._items.values())     # Trả về bản sao, sửa bên ngoài không ảnh hưởng kho

    def find_all(self, condition: Callable[[T], bool]) -> List[T]:
        # Điều kiện lọc truyền từ ngoài, kho không cần biết loại thiết bị cụ thể
        return [item for item in self._items.values() if condition(item)]