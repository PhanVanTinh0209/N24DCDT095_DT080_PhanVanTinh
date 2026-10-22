def kiem_cay(n, canh_chon):
    """Trả về True nếu các cạnh tạo thành cây trên các đỉnh 1..n."""
    if type(n) is not int or not 1 <= n <= 30:
        return False

    if not isinstance(canh_chon, (list, tuple)):
        return False

    if len(canh_chon) != n - 1:
        return False

    # Ban đầu mỗi đỉnh thuộc một nhóm riêng.
    cha = list(range(n + 1))

    def tim_goc(u):
        while cha[u] != u:
            cha[u] = cha[cha[u]]
            u = cha[u]
        return u

    for canh in canh_chon:
        if not isinstance(canh, (list, tuple)) or len(canh) != 3:
            return False

        u, v, w = canh

        if any(type(x) is not int for x in (u, v, w)):
            return False

        if not (1 <= u <= n and 1 <= v <= n):
            return False

        if not 0 <= w <= 1000:
            return False

        goc_u = tim_goc(u)
        goc_v = tim_goc(v)

        # Hai đầu đã cùng nhóm: thêm cạnh sẽ tạo chu trình.
        if goc_u == goc_v:
            return False

        cha[goc_v] = goc_u

    # Mọi đỉnh phải cùng nhóm với đỉnh 1.
    return all(tim_goc(v) == tim_goc(1) for v in range(1, n + 1))