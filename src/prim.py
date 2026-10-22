from heapq import heappush, heappop

from .kiem_tra import kiem_tra_du_lieu


def tao_danh_sach_ke(n, canh):
    """Tạo danh sách kề cho đồ thị vô hướng hợp lệ."""
    kiem_tra_du_lieu(n, canh)

    ke = [[] for _ in range(n + 1)]

    for u, v, w in canh:
        ke[u].append((v, w))
        ke[v].append((u, w))

    return ke


def them_ung_vien(hang, u, ke, da_chon):
    """Thêm cạnh tới đỉnh chưa chọn; trả về số cạnh đã đẩy."""
    so_day = 0

    for v, w in ke[u]:
        if not da_chon[v]:
            # Ưu tiên: trọng số, đỉnh mới, đỉnh cha.
            heappush(hang, (w, v, u))
            so_day += 1

    return so_day


def prim(ke, s=1, lan_vet=False, thong_ke=None):
    """
    Trả về (canh_chon, tong), hoặc None nếu không liên thông.

    Nếu truyền một dict vào thong_ke, hàm ghi các bộ đếm
    của lần chạy hiện tại vào dict đó.
    """
    n = len(ke) - 1

    if type(s) is not int or not 1 <= s <= n:
        raise ValueError("Dinh bat dau khong hop le.")

    if thong_ke is not None and not isinstance(thong_ke, dict):
        raise ValueError("thong_ke phai la dict hoac None.")

    dem = {
        "day_canh": 0,
        "lay_heap": 0,
        "lay_canh": 0,
        "nhan_dinh": 0,
        "bo_qua": 0,
    }

    da_chon = [False] * (n + 1)
    hang = [(0, s, 0)]
    canh_chon = []
    tong = 0

    while hang:
        w, u, cha = heappop(hang)
        dem["lay_heap"] += 1

        # Phần tử nguồn (0, s, 0) không đại diện cho một cạnh.
        if cha != 0:
            dem["lay_canh"] += 1

        if lan_vet:
            print(
                f"\nBuoc {dem['lay_heap']}: "
                f"lay (w, dinh, cha) = {(w, u, cha)}"
            )

        if da_chon[u]:
            dem["bo_qua"] += 1

            if lan_vet:
                print(f"Bo qua: dinh {u} da nam trong cay.")

            continue

        da_chon[u] = True
        dem["nhan_dinh"] += 1

        if cha != 0:
            canh_chon.append((cha, u, w))
            tong += w

            if lan_vet:
                print(f"Chon canh {cha} - {u}, trong so {w}.")
        elif lan_vet:
            print(f"Nhan dinh nguon {u}, khong them canh.")

        dem["day_canh"] += them_ung_vien(
            hang, u, ke, da_chon
        )

        if lan_vet:
            tap_dinh = [
                v for v in range(1, n + 1) if da_chon[v]
            ]
            print(f"Dinh da nhan: {tap_dinh}")
            print(f"Tong hien tai: {tong}")

    if thong_ke is not None:
        thong_ke.update(dem)

    if dem["nhan_dinh"] != n:
        if lan_vet:
            print(f"\nChi nhan duoc {dem['nhan_dinh']}/{n} dinh.")

        return None

    return canh_chon, tong