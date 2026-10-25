# ****************************************
# Mã sinh viên: 20237381
# Họ tên: Đỗ Đình Quân
# ****************************************
"""Các ngoại lệ dùng trong hệ thống quản lý thiết bị phòng dạy."""

from device_status import DeviceStatus


class DuplicateIdException(Exception):
    """Phát sinh khi thêm phần tử có mã (Id) đã tồn tại trong kho."""

    def __init__(self, duplicate_id: str):
        self.duplicate_id = duplicate_id
        super().__init__(f"Mã '{duplicate_id}' đã tồn tại trong kho")


class NoSuitableItemException(Exception):
    """Phát sinh khi không có ứng viên nào phù hợp để chọn."""

    def __init__(self, message: str = "Không có thiết bị phù hợp để cấp phát"):
        super().__init__(message)


class DeviceNotReadyException(Exception):
    """Phát sinh khi thao tác mượn/trả không hợp lệ với trạng thái hiện tại của thiết bị."""

    def __init__(self, device_id: str, current_status: DeviceStatus, message: str = ""):
        self.device_id = device_id
        self.current_status = current_status
        text = message or "Thiết bị chưa sẵn sàng"
        super().__init__(f"{text} (Id={device_id}, trạng thái={current_status.value})")