# Bài nhóm Session 2 · đã xong Task 0–7

Hai bài nhóm của buổi 2 (slide 58–59).

| # | Bài | File | Nộp |
|---|---|---|---|
| 1 | Project kick-off · team card (3 dataset ứng viên, mỗi dataset 2 câu hỏi dạng action + target) | [project_kickoff_team_card.md](project_kickoff_team_card.md) | là Task 0 của GH2; proposal 1 trang ở Session 4 |
| 2 | Group Homework 2 · GoMart deliveries | [gh2_gomart/GH2_TeamName.ipynb](gh2_gomart/GH2_TeamName.ipynb) (bản nộp) · [gh2_gomart/gh2_gomart.py](gh2_gomart/gh2_gomart.py) (tạo tự động từ notebook, cùng nội dung, dạng `.py`) | `GH2_TeamName.ipynb` lên LMS trong 7 ngày sau buổi 2 |

Dữ liệu GoMart đã có sẵn trong `data/raw/` (`gomart_orders_2025.csv`, `gomart_districts.csv`).

**Tiến độ GH2:** Task 0 (team card nháp: điền mã SV, vai trò, tên nhóm) · Task 1 Look · Task 2 Name
· Task 3 Clean · Task 4 Merge đã xong. Chạy notebook sẽ tạo ra
[gh2_gomart/gomart_orders_clean.csv](gh2_gomart/gomart_orders_clean.csv): 5.913 đơn đã làm sạch,
có thêm `zone`, `km_to_hub`, `hour`, `weekday`, `month`, là dữ liệu cho Task 5.
Task 5 (Q1–Q4, mỗi bạn một câu), Task 6 (memo 2 Big Idea) và Task 7 (bảng phân công + AI log) cũng đã xong. Bài nộp là `gh2_gomart/GH2_TeamName.ipynb`, đã chạy sẵn nên mở ra là thấy biểu đồ. Ảnh của 4 câu Q nằm trong `gh2_visuals/` (chạy `export_visuals.py` để tạo lại).

## GH2 cần làm gì (tóm tắt brief)

Quản lý vận hành hỏi 4 câu: **giao chậm ở đâu**, **chuyển sang ví điện tử có thật không**,
**giao chậm có làm mất đánh giá tốt không (từ bao nhiêu phút)**, **giờ cao điểm là khi nào**.

| Task | Nội dung | Rubric |
|---|---|---|
| 0 | Team card | Team & AI 10% |
| 1 | Look: checklist, liệt kê **≥ 6 vấn đề dữ liệu** kèm lệnh phát hiện | Look & clean 25% |
| 2 | Name: loại attribute, hướng, key/value cho **mọi** cột; 2 kiểu “missing” | Abstraction 20% |
| 3 | Clean: `clean_orders(df)` → `(clean_df, log)`, mỗi bước ghi số dòng + lý do | Look & clean 25% |
| 4 | Merge bảng quận (`validate`), tạo `hour`, `weekday` (có thứ tự), `month` | Chart choice 30% |
| 5 | 4 câu hỏi → 4 task → 4 biểu đồ khác nhau + 1 câu diễn giải mỗi biểu đồ | Chart choice 30% |
| 6 | Memo ≤ 120 chữ + Big Idea + 1 biểu đồ giải thích (đặt đầu notebook) | Communication 15% |
| 7 | Bảng phân công + khai báo dùng AI | Team & AI 10% |

Notebook phải chạy được từ đầu đến cuối (*Restart and run all*), nếu không cả bài bị giới hạn ở mức Average.

## Cần chốt khi brainstorm

- **Số người mỗi nhóm**: brief yêu cầu 3–4 người, repo hiện có 6 thành viên. Hỏi giảng viên
  hoặc tách 2 team.
- Chia việc theo Task 1–5 (ai Look, ai Clean, ai vẽ Q1–Q4), người viết memo làm cuối cùng.
- Làm trên `.py` hay trên notebook: `.py` dễ merge khi mỗi người một nhánh; cuối cùng chép
  vào `GH2_TeamName.ipynb` để nộp.
- Có thể dùng lại `src/style.py` (style chung của các activity) để biểu đồ đồng bộ.
