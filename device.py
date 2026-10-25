# ****************************************
# Mã sinh viên: 20237381
# Họ tên: Đỗ Đình Quân
# ****************************************
"""Interface nhận diện đối tượng, lớp trừu tượng TeachingDevice và các lớp dẫn xuất."""

from abc import ABC, abstractmethod

from device_status import DeviceStatus
from exceptions import DeviceNotReadyException


# ---------------------------------------------------------------
# Các hàm kiểm tra dữ liệu đầu vào (dùng chung)
# ---------------------------------------------------------------
def _check_text(value: str, field_name: str) -> str:
    """Kiểm tra chuỗi hợp lệ (không None, không rỗng)."""
    if value is None or not str(value).strip():
        raise ValueError(f"{field_name} không được để trống")
    return str(value).strip()


def _check_percent(value: int, field_name: str) -> int:
    """Kiểm tra giá trị phần trăm nằm trong khoảng 0..100."""
    if not isinstance(value, int) or not 0 <= value <= 100:
        raise ValueError(f"{field_name} phải là số nguyên từ 0 đến 100")
    return value


# ---------------------------------------------------------------
# Interface nhận diện đối tượng
# ---------------------------------------------------------------
class IIdentifiable(ABC):
    """Interface cho mọi đối tượng có mã định danh (Id)."""

    @property
    @abstractmethod
    def id(self) -> str:
        """Mã định danh của đối tượng."""


# ---------------------------------------------------------------
# Lớp trừu tượng TeachingDevice
# ---------------------------------------------------------------
class TeachingDevice(IIdentifiable):
    """Lớp cơ sở trừu tượng của mọi thiết bị dùng trong phòng dạy.

    Chứa phần chung (mã, tên, vị trí, trạng thái, mượn/trả).
    Phần thay đổi theo loại thiết bị (kiểm tra sẵn sàng, tính điểm)
    được khai báo abstract để lớp dẫn xuất ghi đè (đa hình).
    """

    def __init__(self, device_id: str, name: str, storage_location: str):
        self._id = _check_text(device_id, "Id")
        self._name = _check_text(name, "Name")
        self._storage_location = _check_text(storage_location, "StorageLocation")
        self._status = DeviceStatus.AVAILABLE  # Trạng thái ban đầu

    # --- Các thuộc tính chỉ đọc ---
    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def storage_location(self) -> str:
        return self._storage_location

    @property
    def status(self) -> DeviceStatus:
        return self._status  # Chỉ lớp trong hệ thống đổi qua _status (protected)

    # --- Hành vi thay đổi theo loại thiết bị (đa hình) ---
    @abstractmethod
    def is_ready_for_use(self) -> bool:
        """Thiết bị có sẵn sàng cấp phát hay không."""

    @abstractmethod
    def get_default_priority_score(self) -> float:
        """Điểm ưu tiên mặc định khi cấp phát."""

    # --- Hành vi chung cho mọi thiết bị ---
    def borrow(self) -> None:
        """Mượn thiết bị: chỉ thành công khi thiết bị sẵn sàng."""
        if not self.is_ready_for_use():  # Gọi đa hình theo loại thiết bị
            raise DeviceNotReadyException(
                self._id, self._status, "Không thể mượn thiết bị")
        self._status = DeviceStatus.BORROWED

    def return_device(self) -> None:
        """Trả thiết bị về kho: chỉ thành công khi đang ở trạng thái Borrowed."""
        if self._status != DeviceStatus.BORROWED:
            raise DeviceNotReadyException(
                self._id, self._status, "Không thể trả thiết bị chưa được mượn")
        self._status = DeviceStatus.AVAILABLE

    def _extra_info(self) -> str:
        """Thông tin riêng của từng loại (lớp con ghi đè nếu cần)."""
        return ""

    def __str__(self) -> str:
        extra = self._extra_info()
        extra = f", {extra}" if extra else ""
        return (f"{type(self).__name__}[{self._id}] {self._name} "
                f"({self._storage_location}), {self._status.value}{extra}")


