def kiem_tra_du_lieu(n, canh):
    """Báo ValueError nếu dữ liệu vi phạm quy định DT080."""
    if type(n) is not int or not 1 <= n <= 30:
        raise ValueError(
            "So dinh n phai la so nguyen tu 1 den 30."
        )

    if not isinstance(canh, (list, tuple)):
        raise ValueError(
            "Danh sach canh phai la list hoac tuple."
        )

    da_gap = set()

    for i, e in enumerate(canh, start=1):
        if not isinstance(e, (list, tuple)) or len(e) != 3:
            raise ValueError(
                f"Canh {i} phai co dung 3 gia tri (u, v, w)."
            )

        u, v, w = e

        if any(type(x) is not int for x in (u, v, w)):
            raise ValueError(
                f"Canh {i}: u, v, w phai la so nguyen."
            )

        if not (1 <= u <= n and 1 <= v <= n):
            raise ValueError(
                f"Canh {i}: dinh phai nam trong khoang 1 den {n}."
            )

        if u == v:
            raise ValueError(
                f"Canh {i}: khong chap nhan canh tu noi mot dinh."
            )

        if not 0 <= w <= 1000:
            raise ValueError(
                f"Canh {i}: trong so phai tu 0 den 1000."
            )

        cap_dinh = (min(u, v), max(u, v))

        if cap_dinh in da_gap:
            raise ValueError(
                f"Canh {i}: trung cap dinh {cap_dinh}."
            )

        da_gap.add(cap_dinh)