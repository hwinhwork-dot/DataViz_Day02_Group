# Trực quan hoá dữ liệu — Day 02 (Bài nhóm)

**Tên nhóm:** _(chưa đặt)_

## Thành viên & nhánh làm việc

| Thành viên | Nhánh riêng |
|---|---|
| Nguyễn Hoàng Minh (leader) | `hwinh` |
| Phạm Quang Minh | `quang-minh` |
| Phạm Tuấn Anh | `tuan-anh` |
| Trần Nhã Đoan | `nha-doan` |
| Nguyễn Minh Nguyệt | `minh-nguyet` |
| Trần Nguyễn Thanh Thảo | `thao` |

## Quy trình làm việc

```
nhánh riêng ──PR──▶ dev ──(chỉ hwinh)──▶ main
```

- `main`: bản nộp cuối. **Chỉ nhận PR từ `dev`**, do hwinh merge. Không ai push thẳng được,
  PR từ nhánh khác bị chặn (check `chi-nhan-tu-dev` báo lỗi).
- `dev`: nhánh tích hợp chung. Thành viên **chỉ tạo Pull Request**; **chỉ hwinh merge**.
- Nhánh riêng: mỗi người chỉ làm trên nhánh của mình.

PR nhắm vào `main` do thành viên khác tạo sẽ bị **tự động đóng** — hãy chọn base là `dev`.

### Các bước

```bash
# 1. Clone và chuyển sang nhánh của mình (ví dụ: thao)
git clone https://github.com/hwinhwork-dot/DataViz_Day02_Group.git
cd DataViz_Day02_Group
git checkout thao

# 2. Trước khi làm, cập nhật code mới nhất từ dev
git pull origin dev

# 3. Làm bài, rồi commit & push lên nhánh của mình
git add .
git commit -m "Mô tả ngắn thay đổi"
git push origin thao
```

4. Lên GitHub → **Pull requests** → **New pull request** → chọn `base: dev` ← `compare: <nhánh của mình>`.

## Cấu trúc thư mục

```
.
├── activities/       # Activity A–D của Session 2 (mỗi activity 1 file .py + file chạy tổng)
├── homework/         # 2 bài nhóm Session 2: mới có khung, chưa làm
├── data/
│   ├── raw/          # Dữ liệu gốc, không chỉnh sửa
│   └── processed/    # Dữ liệu đã làm sạch / biến đổi
├── notebooks/        # Jupyter notebooks phân tích & vẽ biểu đồ
├── src/              # Hàm Python dùng lại (style.py: style chung cho mọi biểu đồ)
├── outputs/
│   └── figures/      # Biểu đồ xuất ra (PNG/SVG/HTML)
├── reports/          # Báo cáo / bài nộp
└── requirements.txt
```

## Cài đặt

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

## Nội dung bài làm

### Activity A–D (Session 2 · Data and visualization models)

Mỗi activity là một file độc lập, chạy xong lưu 1 hình vào `outputs/figures/`.

| Activity | File | Hình | Kết luận chính |
|---|---|---|---|
| A · Which dataset type? | [activity_a_dataset_types.py](activities/activity_a_dataset_types.py) | [png](outputs/figures/activity_a_dataset_types.png) | 6 tình huống, 5 loại dataset; chỉ đơn hàng giao đến “ngay lúc này” là stream (mục 2 và 4 có thể lập luận theo hai cách) |
| B · Classify the attributes | [activity_b_attribute_types.py](activities/activity_b_attribute_types.py) | [png](outputs/figures/activity_b_attribute_types.png) | 11 cột chia 3 nhóm: 4 định danh, 3 thứ bậc, 4 định lượng; key duy nhất là `order_id`; không lấy trung bình `order_id`, `rating` còn tranh luận |
| C · Reshape on paper | [activity_c_reshape.py](activities/activity_c_reshape.py) | [png](outputs/figures/activity_c_reshape.png) | `melt` cho 6 dòng (key: branch + category); thêm ngày: long thêm 1 cột, wide thêm 3 cột mỗi ngày |
| D · From vague to precise | [activity_d_vague_to_precise.py](activities/activity_d_vague_to_precise.py) | [png](outputs/figures/activity_d_vague_to_precise.png) | 4 yêu cầu mơ hồ → 5 task → 5 biểu đồ vẽ từ dữ liệu thật |

Chạy cả 4 một lần: [activities/run_all_activities.py](activities/run_all_activities.py).

```bash
python activities/run_all_activities.py          # cả A–D
python activities/activity_c_reshape.py          # hoặc từng activity
```

Style kế thừa từ bài Session 1 (`src/style.py`): font serif Georgia, mực đen + xám, một màu nhấn,
tiêu đề nói thẳng kết luận, phụ đề nghiêng, chú thích nguồn ở cuối. Bảng màu đã được kiểm tra cho
người mù màu. Dữ liệu là dữ liệu mô phỏng của khoá học (`data/raw/`).

### Bài nhóm · Group Homework 2 (GoMart)

Đã xong Task 0–4 (team card, Look, Name, Clean, Merge); còn **Task 5–7** cho cả nhóm.
Bài nộp: [homework/gh2_gomart/GH2_TeamName.ipynb](homework/gh2_gomart/GH2_TeamName.ipynb).
Dữ liệu đã làm sạch để vẽ Task 5: [homework/gh2_gomart/gomart_orders_clean.csv](homework/gh2_gomart/gomart_orders_clean.csv).
Chi tiết và việc còn lại: [homework/README.md](homework/README.md).
