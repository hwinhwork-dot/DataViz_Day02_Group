# Project kick-off · Team card (Session 2, slide 58)

> Đây cũng là **Task 0** của Group Homework 2 (bản trong notebook là bản nộp). Mốc tiếp theo:
> **Session 4** nộp proposal 1 trang (dataset + câu hỏi). 3 dataset dưới đây là **bản nháp đề xuất**,
> nhóm thống nhất lại hoặc thay.

**Tên nhóm:** _(chưa đặt)_

## Thành viên

| Student ID | Họ tên | Vai trò |
|---|---|---|
| 31221020403 | Phạm Tuấn Anh | |
| 31241027205 | Trần Nhã Đoan | |
| 31221021575 | Nguyễn Hoàng Minh | Leader |
| 31221021576 | Phạm Quang Minh | |
| 31241021154 | Nguyễn Minh Nguyệt | |
| 31241026554 | Trần Nguyễn Thanh Thảo | |

_Brief yêu cầu nhóm 3–4 người: hỏi lại giảng viên._

## 3 dataset ứng viên

> Kiểm tra trước khi chọn (slide 58): có gọi tên được **key**, **value** và **loại của từng
> attribute** không? Nếu không, chọn dataset khác.

### Dataset 1 · World Development Indicators (World Bank Open Data)
<https://data.worldbank.org/indicator/IT.NET.USER.ZS>

| | |
|---|---|
| Dataset type | multidimensional table, static |
| Key(s) | country + year |
| Values chính | internet users (% dân số), GDP per capita · quantitative · sequential |
| Câu hỏi 1 | *Summarize* the *trend* of internet use in Viet Nam and its ASEAN neighbours, 2000–2024 |
| Câu hỏi 2 | *Discover* the *correlation* between GDP per capita and internet use across ASEAN countries |

### Dataset 2 · Brazilian E-Commerce Public Dataset by Olist (Kaggle)
<https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce>

| | |
|---|---|
| Dataset type | nhiều bảng phẳng nối bằng key, static (~99.000 đơn, 2016–2018) |
| Key(s) | order_id, customer_id |
| Values chính | mốc thời gian giao hàng (quantitative) · review score 1–5 (ordinal) · bang của khách (categorical) |
| Câu hỏi 1 | *Discover* the *dependency* of the review score on late delivery |
| Câu hỏi 2 | *Compare* the *distribution* of delivery time across customer states |

Giống bài GoMart nên dùng lại được kỹ năng làm sạch và vẽ của GH2.

### Dataset 3 · Số liệu thống kê theo tỉnh (Cục Thống kê, trước là GSO)
<https://www.nso.gov.vn>

| | |
|---|---|
| Dataset type | multidimensional table, static; nối được với ranh giới tỉnh (geometry) để vẽ bản đồ |
| Key(s) | province + year |
| Values chính | dân số, thu nhập bình quân đầu người/tháng · quantitative; vùng · categorical |
| Câu hỏi 1 | *Compare* the *extremes* of income per capita across provinces |
| Câu hỏi 2 | *Summarize* the *trend* of income by region |

Lưu ý: năm 2025 các tỉnh đã sáp nhập, nên các bảng có thể dùng danh sách tỉnh khác nhau. Kiểm tra trước khi nối các năm.

---
Mẫu câu hỏi đúng dạng *action + target*: “**Compare** the **extremes** of revenue across branches”.
Sai dạng: “Show sales” (không có action, không có target).
