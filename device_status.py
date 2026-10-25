# ****************************************
# Mã sinh viên: 20237381
# Họ tên: Đỗ Đình Quân
# ****************************************
"""Định nghĩa trạng thái của thiết bị."""

from enum import Enum


class DeviceStatus(Enum):
    """Các trạng thái có thể có của một thiết bị."""
    AVAILABLE = "Available"                 # Đang sẵn sàng cho mượn
    BORROWED = "Borrowed"                   # Đang được mượn
    UNDER_MAINTENANCE = "UnderMaintenance"  # Đang bảo trì