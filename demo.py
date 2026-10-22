import sys

from src.prim import tao_danh_sach_ke, prim
from src.kiem_tra import kiem_tra_du_lieu


def chay_vi_du(ten, n, canh):
    """Chạy Prim và in đầu vào, kết quả hoặc lý do dữ liệu sai."""
    print("=" * 50)
    print(ten)
    print(f"So dinh: {n}")
    print(f"Danh sach canh: {canh}")
    print("Dinh bat dau: 1")

    try:
        ke = tao_danh_sach_ke(n, canh)
    except ValueError as loi:
        print(f"DU LIEU KHONG HOP LE: {loi}")
        print()
        return

    ket_qua = prim(ke, s=1)

    if ket_qua is None:
        print("KHONG LIEN THONG")
    else:
        canh_chon, tong = ket_qua
        print(f"chon = {canh_chon}")
        print(f"tong = {tong}")

    print()


def nhap_do_thi():
    """Đọc và kiểm tra đồ thị do người dùng nhập."""
    try:
        n = int(input("Nhap so dinh n (1..30): "))
    except ValueError:
        raise ValueError(
            "So dinh n phai la so nguyen."
        ) from None

    # Kiểm tra n trước khi hỏi số cạnh.
    kiem_tra_du_lieu(n, [])

    # Số cạnh tối đa của đồ thị vô hướng đơn.
    toi_da = n * (n - 1) // 2

    try:
        m = int(input(f"Nhap so canh m (0..{toi_da}): "))
    except ValueError:
        raise ValueError(
            "So canh m phai la so nguyen."
        ) from None

    if not 0 <= m <= toi_da:
        raise ValueError(
            f"So canh m phai tu 0 den {toi_da}."
        )

    canh = []

    for i in range(1, m + 1):
        du_lieu = input(
            f"Canh {i} - nhap u v w: "
        ).split()

        if len(du_lieu) != 3:
            raise ValueError(
                f"Canh {i}: can nhap dung 3 so u v w."
            )

        try:
            u, v, w = map(int, du_lieu)
        except ValueError:
            raise ValueError(
                f"Canh {i}: u, v, w phai la so nguyen."
            ) from None

        canh.append((u, v, w))

    kiem_tra_du_lieu(n, canh)

    return n, canh


def main():
    tham_so = sys.argv[1:]

    # Chế độ nhập đồ thị bằng bàn phím.
    if tham_so == ["--nhap"]:
        print("DT080 - NHAP DO THI TU BAN PHIM")

        try:
            n, canh = nhap_do_thi()
        except ValueError as loi:
            print(f"DU LIEU KHONG HOP LE: {loi}")
            return
        except EOFError:
            print("DA DUNG: Chua nhap du du lieu.")
            return

        chay_vi_du("DT080 - DU LIEU TU NHAP", n, canh)
        return

    # Thông báo khi truyền tham số không được hỗ trợ.
    if tham_so:
        print("Tham so khong hop le.")
        print("Chay vi du: python demo.py")
        print("Nhap du lieu: python demo.py --nhap")
        return

    # Mặc định: chạy hai ví dụ của đề và một ca dữ liệu sai.
    chay_vi_du(
        "DT080 - VI DU 1",
        3,
        [(1, 2, 4), (1, 3, 1), (2, 3, 2)],
    )

    chay_vi_du(
        "DT080 - VI DU 2",
        4,
        [(1, 2, 1), (3, 4, 2)],
    )

    chay_vi_du(
        "DT080 - KIEM TRA INPUT SAI",
        3,
        [(1, 2, -5), (2, 3, 2)],
    )


if __name__ == "__main__":
    main()