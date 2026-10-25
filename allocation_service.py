# ****************************************
# Mã sinh viên: 20237381
# Họ tên: Đỗ Đình Quân
# ****************************************
"""Dịch vụ cấp phát thiết bị tổng quát."""

from typing import Callable, Generic, Optional, TypeVar

from device import TeachingDevice
from repository import IRepository
from strategy import ISelectionStrategy

# T phải là TeachingDevice hoặc lớp con của nó
T = TypeVar("T", bound=TeachingDevice)


class AllocationService(Generic[T]):
    """Phối hợp kho lưu trữ và chiến lược chọn để cấp phát thiết bị.

    Chỉ phụ thuộc vào abstraction (IRepository, ISelectionStrategy),
    không có if/else kiểm tra loại thiết bị cụ thể.
    """

    def __init__(self, repository: IRepository[T], strategy: ISelectionStrategy[T]):
        if repository is None or strategy is None:
            raise ValueError("repository và strategy không được None")
        self._repository = repository
        self._strategy = strategy

    def change_strategy(self, new_strategy: ISelectionStrategy[T]) -> None:
        """Đổi chiến lược chọn ngay trong lúc chạy."""
        if new_strategy is None:
            raise ValueError("new_strategy không được None")
        self._strategy = new_strategy

    def allocate(self, additional_condition: Optional[Callable[[T], bool]] = None) -> T:
        """Cấp phát một thiết bị cho người mượn.

        Các bước: lấy từ kho -> giữ thiết bị sẵn sàng -> áp dụng điều kiện bổ sung
        -> chọn bằng chiến lược -> mượn -> trả về thiết bị.
        """
        # Bước 1-3: lọc qua repository (is_ready_for_use gọi đa hình theo loại thiết bị)
        candidates = self._repository.find_all(
            lambda d: d.is_ready_for_use()
            and (additional_condition is None or additional_condition(d)))
        # Bước 4: chọn bằng chiến lược hiện tại (đa hình theo chiến lược)
        selected = self._strategy.select(candidates)
        # Bước 5: chuyển trạng thái sang Borrowed
        selected.borrow()
        # Bước 6
        return selected