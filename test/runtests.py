from src.prim import tao_danh_sach_ke, prim
from src.kiem_cay import kiem_cay


# Kết quả kỳ vọng được xác định trước, không lấy từ hàm Prim.
CAC_CA = [
    (
        "TC01", "Vi du 1 tren phieu",
        3,
        [(1, 2, 4), (1, 3, 1), (2, 3, 2)],
        ([(1, 3, 1), (3, 2, 2)], 3),
    ),
    (
        "TC02", "Vi du 2 - hai thanh phan roi",
        4,
        [(1, 2, 1), (3, 4, 2)],
        None,
    ),
    (
        "TC03", "Mot dinh, khong canh",
        1, [],
        ([], 0),
    ),
    (
        "TC04", "Hai dinh, mot canh",
        2, [(1, 2, 7)],
        ([(1, 2, 7)], 7),
    ),
    (
        "TC05", "Hoa trong so, dung thu tu uu tien",
        3,
        [(1, 2, 1), (1, 3, 1), (2, 3, 1)],
        ([(1, 2, 1), (1, 3, 1)], 2),
    ),
    (
        "TC06", "Canh trong so 0",
        3,
        [(1, 2, 0), (1, 3, 5), (2, 3, 0)],
        ([(1, 2, 0), (2, 3, 0)], 0),
    ),
    (
        "TC07", "Do thi bon dinh tu thiet ke",
        4,
        [
            (1, 2, 1), (1, 3, 4), (2, 3, 2),
            (2, 4, 5), (3, 4, 3),
        ],
        ([(1, 2, 1), (2, 3, 2), (3, 4, 3)], 6),
    ),
    (
        "TC08", "Bien tren: 30 dinh, trong so 1000",
        30,
        [(i, i + 1, 1000) for i in range(1, 30)],
        ([(i, i + 1, 1000) for i in range(1, 30)], 29000),
    ),
    (
        "TC09", "Tu choi trong so am",
        3, [(1, 2, -5), (2, 3, 2)],
        ValueError,
    ),
    (
        "TC10", "Tu choi canh tu noi",
        2, [(1, 1, 5)],
        ValueError,
    ),
    (
        "TC11", "Tu choi canh trung nguoc chieu",
        2, [(1, 2, 4), (2, 1, 7)],
        ValueError,
    ),
    (
        "TC12", "Tu choi dinh vuot pham vi",
        3, [(1, 4, 2)],
        ValueError,
    ),
]


def chuan_hoa_canh(u, v, w):
    """Cạnh vô hướng: (u, v, w) và (v, u, w) là cùng một cạnh."""
    return min(u, v), max(u, v), w


def main():
    so_dat = 0
    so_phep_kiem = 0

    print("DT080 - BO KIEM THU TU DONG")
    print("=" * 70)

    for ma, muc_tieu, n, canh, ky_vong in CAC_CA:
        chi_tiet_loi = ""

        try:
            ke = tao_danh_sach_ke(n, canh)
            thuc_te = prim(ke, s=1)
        except ValueError as loi:
            thuc_te = ValueError
            chi_tiet_loi = str(loi)
        except Exception as loi:
            thuc_te = f"LOI NGOAI DU KIEN: {type(loi).__name__}: {loi}"

        cac_kiem_tra = [
            ("Ket qua dung ky vong", thuc_te == ky_vong)
        ]

        # Các ca kỳ vọng có MST được kiểm tra thêm 3 điều kiện.
        if isinstance(ky_vong, tuple):
            hop_le = False
            dung_canh = False
            dung_tong = False

            try:
                canh_chon, tong = thuc_te

                hop_le = kiem_cay(n, canh_chon)

                canh_goc = {
                    chuan_hoa_canh(u, v, w)
                    for u, v, w in canh
                }

                dung_canh = all(
                    chuan_hoa_canh(u, v, w) in canh_goc
                    for u, v, w in canh_chon
                )

                dung_tong = tong == sum(
                    w for u, v, w in canh_chon
                )
            except Exception as loi:
                chi_tiet_loi = (
                    f"Khong kiem tra duoc ket qua: "
                    f"{type(loi).__name__}: {loi}"
                )

            cac_kiem_tra.extend([
                ("Cac canh tao thanh cay", hop_le),
                ("Canh va trong so thuoc do thi goc", dung_canh),
                ("Tong bang tong trong so canh chon", dung_tong),
            ])

        so_phep_kiem += len(cac_kiem_tra)
        dat = all(ket_qua for _, ket_qua in cac_kiem_tra)

        if dat:
            so_dat += 1
            print(
                f"{ma} | PASS | {muc_tieu}"
                f" | {len(cac_kiem_tra)} phep kiem"
            )
        else:
            print(f"{ma} | FAIL | {muc_tieu}")
            print(f"  Ky vong: {ky_vong}")
            print(f"  Thuc te: {thuc_te}")

            for ten, ket_qua in cac_kiem_tra:
                if not ket_qua:
                    print(f"  Khong dat: {ten}")

            if chi_tiet_loi:
                print(f"  Chi tiet: {chi_tiet_loi}")

    tong_ca = len(CAC_CA)

    print("=" * 70)
    print(f"So ca kiem thu doc lap: {tong_ca}")
    print(f"So phep kiem tra: {so_phep_kiem}")
    print(f"PASS: {so_dat}")
    print(f"FAIL: {tong_ca - so_dat}")

    return 0 if so_dat == tong_ca else 1


if __name__ == "__main__":
    raise SystemExit(main())