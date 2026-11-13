"""Diễn giải ảnh chụp trạng thái do src.prim phát ra."""

def ly_do(item, heap_truoc, bo_qua):
    if item is None:
        return "Đưa phần tử nguồn vào hàng ưu tiên."
    w, v, cha = item
    if cha == 0:
        return f"Nhận đỉnh nguồn {v}. Phần tử nguồn không tạo cạnh."
    parts = [f"Lấy {item}."]
    if len(heap_truoc) == 1:
        parts.append("Đây là ứng viên duy nhất trong heap.")
    else:
        doi_thu = heap_truoc[1]
        w2, v2, cha2 = doi_thu
        if w != w2:
            parts.append(f"So với {doi_thu}, trọng số {w} < {w2}.")
        elif v != v2:
            parts.append(f"So với {doi_thu}, cùng trọng số {w}. Ưu tiên đỉnh mới {v} vì {v} < {v2}.")
        else:
            parts.append(f"So với {doi_thu}, cùng trọng số {w} và cùng đỉnh mới {v}. Ưu tiên cha {cha} vì {cha} < {cha2}.")
    if bo_qua:
        parts.append(f"Đỉnh {v} đã thuộc cây nên bỏ cạnh {cha}–{v}.")
    else:
        parts.append(f"Đỉnh {v} chưa thuộc cây. Nhận cạnh {cha}–{v} và cộng {w} vào tổng.")
    return " ".join(parts)


def noi_dung(steps, index, size, result):
    action, item, heap, nodes, tree, total = steps[index]
    before = steps[index-1][2] if index else ()
    them = sorted(set(heap) - set(before))
    lines = [f"Bước {index}/{len(steps)-1}  ·  {action}",
             ly_do(item, before, action=="Bỏ qua"),
             f"Đã nhận {len(nodes)}/{size} đỉnh  ·  Tổng hiện tại {total}"]
    if index == len(steps)-1:
        if result is None:
            missing = sorted(set(range(1,size+1))-set(nodes))
            lines += [f"KHÔNG LIÊN THÔNG. Heap đã rỗng. Các đỉnh chưa tới được: {missing}."]
        else:
            lines += [f"Hoàn tất · Tổng trọng số MST = {total}"]
    lines += [f"Đỉnh đã nhận: {list(nodes)}", f"Cạnh đã chọn (cha, đỉnh, w): {list(tree)}",
              "Thứ tự ưu tiên: (w, đỉnh mới, cha).",
              f"Vừa lấy: {item if item is not None else '—'}",
              f"Vừa thêm: {them}", f"Heap sau bước ({len(heap)} phần tử): {list(heap)}",
              f"Heap trước bước: {list(before)}"]
    return "\n\n".join(lines)
