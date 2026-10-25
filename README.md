# Quản lý thiết bị phòng dạy

Bài thực hành OOP tuần 7: đa hình và generic (Python).

## Thông tin sinh viên

- Họ tên: Đỗ Đình Quân
- Mã sinh viên: 20237381

## Giới thiệu

Chương trình mô phỏng việc quản lý và cấp phát các thiết bị dùng trong phòng dạy: điều khiển máy chiếu, điều khiển điều hòa và micro không dây. Mỗi thiết bị có mã, tên, vị trí lưu trữ và trạng thái (Available, Borrowed, UnderMaintenance). Mỗi loại thiết bị có cách kiểm tra khả năng sẵn sàng và cách tính điểm ưu tiên riêng.

## Chức năng

- Lưu trữ, tìm kiếm thiết bị theo mã và lọc thiết bị theo điều kiện.
- Chọn thiết bị tốt nhất theo chiến lược (điểm ưu tiên cao nhất hoặc phần tử đầu tiên).
- Cấp phát thiết bị cho người mượn và nhận thiết bị trả về kho.
- Thêm loại thiết bị hoặc chiến lược mới mà không phải sửa các lớp cũ.

## Thiết kế

- **Đa hình:** lớp trừu tượng `TeachingDevice` có 3 lớp con (`ProjectorRemote`, `AirConditionerRemote`, `WirelessMicrophone`) ghi đè cách kiểm tra sẵn sàng và cách tính điểm. Các chiến lược chọn cùng cài đặt interface `ISelectionStrategy` nên có thể đổi lúc chạy.
- **Generic:** kho `IRepository[T]` / `InMemoryRepository[T]` dùng chung cho mọi loại thiết bị có mã định danh (`IIdentifiable`). `AllocationService[T]` phối hợp kho và chiến lược mà không cần kiểm tra loại thiết bị cụ thể.
- **Ngoại lệ:** `DuplicateIdException`, `NoSuitableItemException`, `DeviceNotReadyException`.

## Cấu trúc

- `device_status.py`: enum trạng thái thiết bị
- `exceptions.py`: các ngoại lệ
- `device.py`: `IIdentifiable`, `TeachingDevice` và 3 lớp thiết bị
- `repository.py`: kho lưu trữ generic
- `strategy.py`: các chiến lược chọn thiết bị
- `allocation_service.py`: dịch vụ cấp phát
- `main.py`: chương trình kiểm thử
- `ket_qua_chay.txt`: kết quả chạy chương trình

## Cách chạy

```
python main.py
```

## Báo cáo

Sơ đồ lớp, phân tích thiết kế, kết quả chạy và kiểm thử chi tiết nằm trong file báo cáo nộp kèm.
