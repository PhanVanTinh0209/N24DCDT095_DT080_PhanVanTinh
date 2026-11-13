# DT080 – Thuật toán Prim tìm cây khung nhỏ nhất

## Thông tin sinh viên

- Họ và tên: Phan Văn Tịnh
- MSSV: N24DCDT095
- Lớp: D24CQDT01-N
- Mã đề: DT080
- Ngôn ngữ: Python

## 1. Mô tả bài toán

Tìm cây khung nhỏ nhất của đồ thị vô hướng đơn có trọng số,
bắt đầu từ đỉnh 1.

Quy định dữ liệu:
- Số đỉnh n là số nguyên từ 1 đến 30.
- Các đỉnh được đánh số từ 1 đến n.
- Trọng số cạnh là số nguyên từ 0 đến 1000.
- Không chấp nhận cạnh tự nối hoặc cạnh trùng, kể cả ngược chiều.

Các ứng viên trong hàng đợi ưu tiên được sắp theo:
(trọng số, đỉnh mới, đỉnh cha).

Nếu đồ thị liên thông, chương trình trả về các cạnh được chọn
theo thứ tự của Prim và tổng trọng số.

Nếu đồ thị không liên thông, chương trình hiển thị:
KHONG LIEN THONG

Đồ thị chỉ có một đỉnh trả về danh sách cạnh rỗng và tổng bằng 0.

## 2. Môi trường và thư viện

Chương trình sử dụng Python 3 và các thư viện chuẩn.
Không cần cài thêm thư viện bằng pip.

Kiểm tra phiên bản Python đang chạy:

```powershell
python --version
```

Chạy tất cả lệnh dưới đây từ thư mục gốc của dự án.

## 3. Các tệp chính

- src/kiem_tra.py: kiểm tra tính hợp lệ của dữ liệu đầu vào.
- src/prim.py: tạo danh sách kề, thực hiện Prim, truy vết và đếm thao tác.
- src/kiem_cay.py: kiểm tra các cạnh có tạo thành cây hay không.
- test/runtests.py: bộ kiểm thử tự động.
- demo.py: chạy ví dụ hoặc nhập đồ thị từ bàn phím.
- truy_vet.py: hiển thị từng bước Prim trên ví dụ 1.
- khao_sat.py: khảo sát số thao tác với 5, 10, 20 đỉnh.
- docs/anh_ket_qua/: lưu ảnh minh chứng chạy chương trình.

## 4. Chạy các ví dụ

```powershell
python demo.py
```

Chương trình chạy:
- Ví dụ 1: chọn [(1, 3, 1), (3, 2, 2)], tổng bằng 3.
- Ví dụ 2: hiển thị KHONG LIEN THONG.
- Một trường hợp trọng số âm: hiển thị thông báo dữ liệu không hợp lệ.

## 5. Nhập đồ thị từ bàn phím

```powershell
python demo.py --nhap
```

Nhập lần lượt:
1. Số đỉnh n.
2. Số cạnh m.
3. Mỗi cạnh trên một dòng, theo dạng u v w.

Ví dụ nhập:

```text
3
3
1 2 4
1 3 1
2 3 2
```

Kết quả mong đợi:
- Các cạnh được chọn: [(1, 3, 1), (3, 2, 2)].
- Tổng trọng số: 3.

## 6. Chạy truy vết

```powershell
python truy_vet.py
```

Chương trình hiển thị phần tử lấy khỏi heap, cạnh được chọn,
tập đỉnh đã nhận, tổng hiện tại và các lần bỏ qua.

## 7. Chạy kiểm thử tự động

```powershell
python -m test.runtests
```

Bộ kiểm thử gồm 12 ca độc lập và 33 phép kiểm tra.

Với các ca có cây, chương trình kiểm tra:
- Kết quả khớp kết quả kỳ vọng đã xác định trước.
- Các cạnh tạo thành cây.
- Các cạnh và trọng số thuộc đồ thị đầu vào.
- Tổng trả về bằng tổng trọng số các cạnh được chọn.

Các ca còn lại kiểm tra đồ thị không liên thông và dữ liệu sai.

Kết quả mong đợi:
- PASS: 12.
- FAIL: 0.

Chương trình kiểm thử trả mã thoát 0 nếu tất cả ca đạt,
trả mã thoát 1 nếu có ca không đạt.

## 8. Chạy khảo sát

Từ thư mục gốc của dự án, chạy:

```powershell
python khao_sat.py
```

Chương trình khảo sát hai dạng đồ thị với `n = 5, 10, 20`:

- **Đồ thị đường đi:** gồm `n - 1` cạnh, mỗi cạnh có trọng số 1.
- **Đồ thị đầy đủ:** các cạnh nối hai đỉnh liên tiếp có trọng số 1, các cạnh còn lại có trọng số 10.

Ở cả hai dạng, `n - 1` cạnh nối các đỉnh liên tiếp tạo thành một cây bao trùm có tổng trọng số `n - 1`. Vì mỗi cạnh có trọng số ít nhất là 1, đây cũng là tổng trọng số MST kỳ vọng.

Các bộ đếm trong kết quả khảo sát:

- `day_canh`: số cạnh được đẩy vào heap, không tính phần tử nguồn.
- `lay_canh`: số cạnh được lấy khỏi heap, kể cả cạnh bị bỏ qua.
- `lay_heap`: số lần lấy phần tử khỏi heap, tính cả phần tử nguồn.
- `nhan_dinh`: số đỉnh được nhận vào cây.
- `bo_qua`: số phần tử bị bỏ qua vì đỉnh đích đã được nhận.

Phiên bản hiện tại xử lý đến khi heap rỗng.

### Chạy mô phỏng trực quan thuật toán Prim

Từ thư mục gốc của dự án, chạy:

```powershell
python mo_phong.py
```

Chọn một đồ thị mẫu hoặc bấm **Sửa đồ thị…** để nhập đồ thị. Mỗi dòng trong danh sách cạnh gồm ba số nguyên theo thứ tự `u v w`, trong đó `u`, `v` là hai đầu mút và `w` là trọng số cạnh.

Bấm **Tiếp** để theo dõi từng bước hoặc **Chạy** để chương trình chạy tự động. Hai tab **Heap trước** và **Heap sau** cho phép đối chiếu các ứng viên trước và sau bước đang xét. Tab **Cạnh cây** liệt kê các cạnh đã chọn.

## 9. Độ phức tạp

Khi tắt truy vết, với đồ thị đơn liên thông và n >= 2:
- Thời gian: O(m log n).
- Bộ nhớ: O(n + m).

Trong đó n là số đỉnh, m là số cạnh.

Chế độ truy vết có thêm chi phí tạo và in thông tin từng bước.