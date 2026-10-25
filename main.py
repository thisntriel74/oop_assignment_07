# ****************************************
# Mã sinh viên: 20237381
# Họ tên: Đỗ Đình Quân
# ****************************************
"""Chương trình kiểm thử hệ thống quản lý thiết bị phòng dạy."""

from allocation_service import AllocationService
from device import AirConditionerRemote, ProjectorRemote, WirelessMicrophone
from exceptions import (DeviceNotReadyException, DuplicateIdException,
                        NoSuitableItemException)
from repository import InMemoryRepository
from strategy import FirstAvailableStrategy, HighestPriorityStrategy


def title(text: str) -> None:
    """In tiêu đề của một nhóm kiểm thử."""
    print(f"\n=== {text} ===")


def check(description: str, condition: bool) -> None:
    """In kết quả kiểm tra PASS/FAIL cho một khẳng định."""
    print(f"  [{'PASS' if condition else 'FAIL'}] {description}")


def main() -> None:
    # ---------- Test 1: Thêm thiết bị vào repository ----------
    title("Test 1: Thêm thiết bị vào repository")
    projector_repo = InMemoryRepository[ProjectorRemote]()
    ac_repo = InMemoryRepository[AirConditionerRemote]()
    mic_repo = InMemoryRepository[WirelessMicrophone]()

    projector_repo.add(ProjectorRemote("PJ01", "Remote Epson", "Kho A", 90))
    projector_repo.add(ProjectorRemote("PJ02", "Remote Sony", "Kho A", 55))
    projector_repo.add(ProjectorRemote("PJ03", "Remote BenQ", "Kho B", 15))  # pin yếu

    ac_repo.add(AirConditionerRemote("AC01", "Remote Daikin", "Kho B", {"A203", "A204"}))
    ac_repo.add(AirConditionerRemote("AC02", "Remote Panasonic", "Kho B", {"B101"}))

    mic_repo.add(WirelessMicrophone("MIC01", "Micro Shure", "Kho C", 50, 45))
    mic_repo.add(WirelessMicrophone("MIC02", "Micro Sony", "Kho C", 25, 90))  # pin yếu
    mic_repo.add(WirelessMicrophone("MIC03", "Micro Boya", "Kho C", 80, 70))

    for repo in (projector_repo, ac_repo, mic_repo):
        for device in repo.get_all():
            print("  ", device)
    check("Số máy chiếu = 3, điều hòa = 2, micro = 3",
          (len(projector_repo.get_all()), len(ac_repo.get_all()),
           len(mic_repo.get_all())) == (3, 2, 3))

    # ---------- Test 2: Thêm hai thiết bị trùng mã ----------
    title("Test 2: Thêm thiết bị trùng mã")
    try:
        projector_repo.add(ProjectorRemote("PJ01", "Remote trùng", "Kho A", 70))
        check("Phải ném DuplicateIdException", False)
    except DuplicateIdException as e:
        print("  Bắt được ngoại lệ:", e)
        check("Ném DuplicateIdException, DuplicateId = PJ01", e.duplicate_id == "PJ01")
    check("Kho vẫn còn 3 máy chiếu", len(projector_repo.get_all()) == 3)

    # ---------- Test 3: Tìm thiết bị theo mã ----------
    title("Test 3: Tìm thiết bị theo mã")
    found = projector_repo.find_by_id("PJ02")
    print("  find_by_id('PJ02') =", found)
    check("Tìm thấy PJ02", found is not None and found.id == "PJ02")
    check("Không tìm thấy PJ99 -> None", projector_repo.find_by_id("PJ99") is None)
    check("remove('PJ99') -> False", projector_repo.remove("PJ99") is False)

    # ---------- Test 4: Lọc các thiết bị sẵn sàng ----------
    title("Test 4: Lọc các thiết bị sẵn sàng")
    ready_pj = projector_repo.find_all(lambda d: d.is_ready_for_use())
    ready_ac = ac_repo.find_all(lambda d: d.is_ready_for_use())
    ready_mic = mic_repo.find_all(lambda d: d.is_ready_for_use())
    print("  Máy chiếu sẵn sàng :", [d.id for d in ready_pj])
    print("  Điều hòa sẵn sàng  :", [d.id for d in ready_ac])
    print("  Micro sẵn sàng     :", [d.id for d in ready_mic])
    check("Máy chiếu sẵn sàng = PJ01, PJ02 (PJ03 pin 15% < 20%)",
          [d.id for d in ready_pj] == ["PJ01", "PJ02"])
    check("Micro sẵn sàng = MIC01, MIC03 (MIC02 pin 25% < 30%)",
          [d.id for d in ready_mic] == ["MIC01", "MIC03"])
    # Kiểm tra get_all() không lộ collection nội bộ
    projector_repo.get_all().clear()
    check("Sửa list trả về từ get_all() không ảnh hưởng kho",
          len(projector_repo.get_all()) == 3)

    # ---------- Test 5: Máy chiếu có điểm cao nhất ----------
    title("Test 5: Chọn điều khiển máy chiếu có điểm cao nhất")
    projector_service = AllocationService[ProjectorRemote](
        projector_repo,
        HighestPriorityStrategy(lambda d: d.get_default_priority_score()))
    selected_pj = projector_service.allocate(lambda d: True)
    print("  Được cấp phát:", selected_pj)
    check("Chọn PJ01 (pin 90 cao nhất)", selected_pj.id == "PJ01")

    # ---------- Test 6: Điều hòa tương thích với phòng ----------
    title("Test 6: Chọn điều khiển điều hòa tương thích phòng A203")
    ac_service = AllocationService[AirConditionerRemote](
        ac_repo,
        HighestPriorityStrategy(lambda d: d.get_default_priority_score()))
    selected_ac = ac_service.allocate(lambda d: d.is_compatible_with("A203"))
    print("  Được cấp phát:", selected_ac)
    check("Chọn AC01 (hỗ trợ phòng A203)", selected_ac.id == "AC01")

    # ---------- Test 7: Micro đầu tiên sẵn sàng ----------
    title("Test 7: Chọn micro đầu tiên sẵn sàng (FirstAvailableStrategy)")
    mic_service = AllocationService[WirelessMicrophone](
        mic_repo, FirstAvailableStrategy())
    first_mic = mic_service.allocate()
    print("  Được cấp phát:", first_mic)
    check("Chọn MIC01 (micro sẵn sàng đầu tiên)", first_mic.id == "MIC01")

    # ---------- Test 8: Đổi chiến lược trong lúc chạy ----------
    title("Test 8: Đổi chiến lược trong thời gian chạy")
    first_mic.return_device()  # Trả MIC01 để cả MIC01, MIC03 cùng sẵn sàng
    print("  Đã trả", first_mic.id, "->", first_mic.status.value)
    mic_service.change_strategy(
        HighestPriorityStrategy(lambda d: d.get_default_priority_score()))
    best_mic = mic_service.allocate()
    print("  Sau khi đổi sang HighestPriorityStrategy:", best_mic)
    check("Kết quả đổi từ MIC01 sang MIC03 (điểm 75 > 47.5)", best_mic.id == "MIC03")

    # ---------- Test 9: Không có ứng viên phù hợp ----------
    title("Test 9: Cấp phát khi không có ứng viên phù hợp")
    try:
        ac_service.allocate(lambda d: d.is_compatible_with("Z999"))
        check("Phải ném NoSuitableItemException", False)
    except NoSuitableItemException as e:
        print("  Bắt được ngoại lệ:", e)
        check("Ném NoSuitableItemException (không có điều hòa hợp phòng Z999)", True)
    try:
        FirstAvailableStrategy().select([])
        check("Chiến lược với danh sách rỗng phải ném ngoại lệ", False)
    except NoSuitableItemException:
        check("Chiến lược với danh sách rỗng ném NoSuitableItemException", True)

    # ---------- Test 10: Thiết bị chuyển sang Borrowed ----------
    title("Test 10: Thiết bị được chọn chuyển sang Borrowed")
    pj01 = projector_repo.find_by_id("PJ01")
    print("  Trạng thái PJ01:", pj01.status.value)
    check("PJ01 đang Borrowed", pj01.status.value == "Borrowed")
    check("PJ01 không còn sẵn sàng", not pj01.is_ready_for_use())
    try:
        pj01.borrow()
        check("Mượn lại thiết bị đang Borrowed phải ném ngoại lệ", False)
    except DeviceNotReadyException as e:
        print("  Bắt được ngoại lệ:", e)
        check("Mượn lại -> DeviceNotReadyException", e.device_id == "PJ01")
    pj01.return_device()
    check("Sau khi trả, PJ01 về Available", pj01.status.value == "Available")
    try:
        pj01.return_device()
        check("Trả thiết bị chưa mượn phải ném ngoại lệ", False)
    except DeviceNotReadyException as e:
        print("  Bắt được ngoại lệ:", e)
        check("Trả thiết bị chưa mượn -> DeviceNotReadyException", True)

    # ---------- Test 11: Repository tổng quát dùng cho nhiều loại ----------
    title("Test 11: Một lớp InMemoryRepository dùng cho nhiều loại thiết bị")
    print("  Kiểu của 3 kho :", {type(r).__name__ for r in (projector_repo, ac_repo, mic_repo)})
    check("Cả 3 kho cùng một lớp InMemoryRepository (không sao chép mã)",
          type(projector_repo) is type(ac_repo) is type(mic_repo))
    check("Mỗi kho chứa đúng loại thiết bị của nó",
          all(isinstance(d, ProjectorRemote) for d in projector_repo.get_all())
          and all(isinstance(d, WirelessMicrophone) for d in mic_repo.get_all()))

    # ---------- Kiểm tra dữ liệu không hợp lệ ----------
    title("Kiểm tra dữ liệu không hợp lệ")
    for label, make in (
            ("Pin = 120", lambda: ProjectorRemote("PJ10", "X", "Kho", 120)),
            ("Id rỗng", lambda: WirelessMicrophone("", "X", "Kho", 50, 50))):
        try:
            make()
            check(f"{label} phải bị từ chối", False)
        except ValueError as e:
            print(f"  {label}:", e)
            check(f"{label} bị từ chối bằng ValueError", True)


if __name__ == "__main__":
    main()