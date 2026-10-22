from src.prim import tao_danh_sach_ke, prim
from src.kiem_cay import kiem_cay


def tao_do_thi(n, dang):
    """Tạo dữ liệu cố định để mỗi lần chạy đều tái lập được."""
    if dang == "Duong di":
        return [
            (u, u + 1, 1)
            for u in range(1, n)
        ]

    if dang == "Day du":
        return [
            (u, v, 1 if v == u + 1 else 10)
            for u in range(1, n + 1)
            for v in range(u + 1, n + 1)
        ]

    raise ValueError("Dang do thi khong hop le.")


def main():
    print("DT080 - KHAO SAT SO THAO TAC PRIM")
    print("Dinh bat dau: 1")
    print("Trong so: canh lien tiep = 1; canh khac = 10.")
    print("Tong MST ky vong: n - 1.")
    print("Day/Lay canh khong tinh phan tu nguon.")
    print("Lay heap co tinh phan tu nguon.")
    print()

    print(
        f"{'Dang':<10} {'n':>3} {'m':>4} "
        f"{'Tong':>5} {'Day':>5} {'Lay canh':>8} "
        f"{'Lay heap':>8} {'Nhan':>5} "
        f"{'Bo qua':>6} {'KQ':>5}"
    )
    print("-" * 80)

    tat_ca_dat = True

    for dang in ("Duong di", "Day du"):
        for n in (5, 10, 20):
            canh = tao_do_thi(n, dang)
            ke = tao_danh_sach_ke(n, canh)
            dem = {}

            ket_qua = prim(ke, s=1, thong_ke=dem)

            if ket_qua is None:
                tat_ca_dat = False
                print(f"{dang}, n={n}: FAIL - KHONG LIEN THONG")
                continue

            canh_chon, tong = ket_qua

            canh_goc = {
                (min(u, v), max(u, v), w)
                for u, v, w in canh
            }

            dung_canh = all(
                (min(u, v), max(u, v), w) in canh_goc
                for u, v, w in canh_chon
            )

            dat = (
                kiem_cay(n, canh_chon)
                and dung_canh
                and tong == sum(w for _, _, w in canh_chon)
                and tong == n - 1
            )

            tat_ca_dat = tat_ca_dat and dat
            trang_thai = "PASS" if dat else "FAIL"

            print(
                f"{dang:<10} {n:>3} {len(canh):>4} "
                f"{tong:>5} {dem['day_canh']:>5} "
                f"{dem['lay_canh']:>8} "
                f"{dem['lay_heap']:>8} "
                f"{dem['nhan_dinh']:>5} "
                f"{dem['bo_qua']:>6} {trang_thai:>5}"
            )

    print("-" * 80)
    print("Hoan tat: 6 truong hop khao sat.")
    print("Ket qua:", "TAT CA DAT" if tat_ca_dat else "CO LOI")

    return 0 if tat_ca_dat else 1


if __name__ == "__main__":
    raise SystemExit(main())