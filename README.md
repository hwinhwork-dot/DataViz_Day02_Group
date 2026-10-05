# Trực quan hoá dữ liệu — Day 02 (Bài nhóm)

**Tên nhóm:** _(chưa đặt)_

## Thành viên & nhánh làm việc

| Thành viên  | Nhánh riêng   |
|-------------|---------------|
| hwinh       | `hwinh`       |
| Quang Minh  | `quang-minh`  |
| Tuấn Anh    | `tuan-anh`    |
| Nhã Đoan    | `nha-doan`    |
| Minh Nguyệt | `minh-nguyet` |
| Thảo        | `thao`        |

## Quy trình làm việc

```
nhánh riêng ──PR──▶ dev ──(chỉ hwinh)──▶ main
```

- `main`: bản nộp cuối. **Chỉ hwinh** được merge/push vào `main`.
- `dev`: nhánh tích hợp chung. Không push thẳng — mọi thay đổi vào qua **Pull Request**.
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
├── data/
│   ├── raw/          # Dữ liệu gốc, không chỉnh sửa
│   └── processed/    # Dữ liệu đã làm sạch / biến đổi
├── notebooks/        # Jupyter notebooks phân tích & vẽ biểu đồ
├── src/              # Hàm Python dùng lại (load, clean, plot)
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

_(Sẽ cập nhật theo yêu cầu của bài lab.)_
