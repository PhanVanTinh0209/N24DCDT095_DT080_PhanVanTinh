from src.prim import tao_danh_sach_ke, prim


def main():
    n = 3
    canh = [
        (1, 2, 4),
        (1, 3, 1),
        (2, 3, 2),
    ]

    print("DT080 - LAN VET PRIM - VI DU 1")
    print(f"So dinh: {n}")
    print(f"Danh sach canh: {canh}")
    print("Dinh bat dau: 1")

    ke = tao_danh_sach_ke(n, canh)
    ket_qua = prim(ke, s=1, lan_vet=True)

    print("\nKET QUA CUOI CUNG")

    if ket_qua is None:
        print("KHONG LIEN THONG")
    else:
        canh_chon, tong = ket_qua
        print(f"chon = {canh_chon}")
        print(f"tong = {tong}")


if __name__ == "__main__":
    main()