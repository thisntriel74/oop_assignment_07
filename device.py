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


# ---------------------------------------------------------------
# Điều khiển máy chiếu
# ---------------------------------------------------------------
class ProjectorRemote(TeachingDevice):
    """Điều khiển máy chiếu: có mức pin 0..100."""
 
    MIN_BATTERY = 20  # Pin tối thiểu để cấp phát
 
    def __init__(self, device_id: str, name: str, storage_location: str,
                 battery_level: int):
        super().__init__(device_id, name, storage_location)
        self._battery_level = _check_percent(battery_level, "BatteryLevel")
 
    @property
    def battery_level(self) -> int:
        return self._battery_level
 
    def is_ready_for_use(self) -> bool:
        # Sẵn sàng khi Available và pin >= 20%
        return (self._status == DeviceStatus.AVAILABLE
                and self._battery_level >= self.MIN_BATTERY)
 
    def get_default_priority_score(self) -> float:
        # Điểm ưu tiên = mức pin
        return float(self._battery_level)
 
    def _extra_info(self) -> str:
        return f"pin={self._battery_level}%"
 
 
# ---------------------------------------------------------------
# Điều khiển điều hòa
# ---------------------------------------------------------------
class AirConditionerRemote(TeachingDevice):
    """Điều khiển điều hòa: có tập phòng tương thích."""
 
    def __init__(self, device_id: str, name: str, storage_location: str,
                 compatible_rooms):
        super().__init__(device_id, name, storage_location)
        if compatible_rooms is None:
            raise ValueError("CompatibleRooms không được None")
        # frozenset: tập chỉ đọc, bên ngoài không sửa được
        self._compatible_rooms = frozenset(compatible_rooms)
 
    @property
    def compatible_rooms(self) -> frozenset:
        return self._compatible_rooms
 
    def is_compatible_with(self, room_id: str) -> bool:
        """Điều khiển có tương thích với phòng room_id hay không."""
        return room_id in self._compatible_rooms
 
    def is_ready_for_use(self) -> bool:
        # Chỉ cần trạng thái Available
        return self._status == DeviceStatus.AVAILABLE
 
    def get_default_priority_score(self) -> float:
        # Không biết phòng cụ thể nên: có hỗ trợ ít nhất một phòng -> 100, ngược lại 0.
        # (Việc lọc đúng phòng được thực hiện qua điều kiện bổ sung khi Allocate)
        return 100.0 if self._compatible_rooms else 0.0
 
    def _extra_info(self) -> str:
        return f"phòng={sorted(self._compatible_rooms)}"
 
 
# ---------------------------------------------------------------
# Micro không dây
# ---------------------------------------------------------------
class WirelessMicrophone(TeachingDevice):
    """Micro không dây: có mức pin và chất lượng tín hiệu (0..100)."""
 
    MIN_BATTERY = 30   # Pin tối thiểu
    MIN_SIGNAL = 40    # Tín hiệu tối thiểu
 
    def __init__(self, device_id: str, name: str, storage_location: str,
                 battery_level: int, signal_quality: int):
        super().__init__(device_id, name, storage_location)
        self._battery_level = _check_percent(battery_level, "BatteryLevel")
        self._signal_quality = _check_percent(signal_quality, "SignalQuality")
 
    @property
    def battery_level(self) -> int:
        return self._battery_level
 
    @property
    def signal_quality(self) -> int:
        return self._signal_quality
 
    def is_ready_for_use(self) -> bool:
        # Sẵn sàng khi Available, pin >= 30% và tín hiệu >= 40%
        return (self._status == DeviceStatus.AVAILABLE
                and self._battery_level >= self.MIN_BATTERY
                and self._signal_quality >= self.MIN_SIGNAL)
 
    def get_default_priority_score(self) -> float:
        # Điểm ưu tiên = trung bình của pin và tín hiệu
        return (self._battery_level + self._signal_quality) / 2
 
    def _extra_info(self) -> str:
        return f"pin={self._battery_level}%, tín hiệu={self._signal_quality}%"