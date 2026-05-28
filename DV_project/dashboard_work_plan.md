# Kế hoạch phân công Dashboard Dash - FIFA World Cup

## 1. Tóm tắt

Deadline tổng phần dashboard: **31/05/2026**.

Dashboard dùng **Dash + Plotly**, chia theo component/page để 4 người làm độc lập nhất có thể. Mỗi người tự xử lý dữ liệu cần cho phần của mình, tự làm visual, filter, callback và kiểm tra output. Trưởng nhóm chịu trách nhiệm app shell, style chung, merge và kiểm thử tích hợp.

Story tổng thể:

> World Cup ngày càng mở rộng toàn cầu, nhưng chức vô địch vẫn tập trung ở nhóm elite; dữ liệu trận đấu hiện đại cho thấy vẫn có nhiều bất ngờ.

Điều chỉnh quan trọng:

- Phần từng gọi là **2022 Drilldown** đổi thành **Tournament Detail Template**.
- Page này có dropdown chọn năm World Cup để trực quan hóa theo cùng một template.
- Dashboard có thể xem nhiều năm, nhưng phần phân tích chính trong report/slides chỉ tập trung vào **World Cup 2022**.

## 2. Phân công công việc

## Khánh - Team Leader + Overview Page

### Vai trò

- Làm trưởng nhóm kỹ thuật.
- Tạo khung app Dash chung.
- Làm page tổng quan World Cup.
- Merge các component của nhóm.

### Đầu việc

- Tạo cấu trúc project Dash:
  - `app.py`
  - `pages/`
  - `assets/`
  - `src/`
- Cài navigation/sidebar/topbar để chuyển giữa 4 page:
  - Overview
  - Dominance
  - Upsets & Competitiveness
  - Tournament Detail
- Tạo theme chung:
  - Color palette.
  - Font.
  - Spacing.
  - Card style.
  - Plotly chart template.
- Làm **Overview Page** gồm:
  - KPI cards: số kỳ World Cup, tổng số đội, tổng số trận, tổng số bàn thắng, số đội từng vô địch.
  - Line chart: teams/matches/goals theo year.
  - Line chart: average goals per game theo year.
  - Champion timeline: year, host, champion.
  - Filter: year range, host, champion.
- Merge code của 3 người còn lại.
- Kiểm tra app chạy end-to-end trước deadline.

### Definition of Done

- App chạy được bằng một lệnh:

```bash
python app.py
```

- Có navigation đủ 4 page.
- Overview có ít nhất 3 chart, KPI row và filter hoạt động.
- Style chung được áp dụng nhất quán cho toàn bộ dashboard.
- Không lỗi callback khi chuyển page hoặc reset filter.

### Cần gửi feedback cho leader

Vì người 1 là leader, cần yêu cầu các thành viên gửi lại:

- File page hoặc branch/code phần mình làm.
- Data fields đã dùng.
- Callback ids.
- Ảnh chụp màn hình page.
- Lỗi còn tồn tại nếu có.

Leader cần gửi lại nhóm:

- Bản dashboard tổng hợp sau khi merge.
- Danh sách lỗi còn lại.
- Các điểm cần sửa trước khi demo.

## Dương - Dominance Page

### Vai trò

Làm page phân tích sự thống trị của các đội/khu vực trong lịch sử World Cup.

### Đầu việc

- Đọc `FIFA - World Cup Summary.csv`.
- Đọc và combine các file `FIFA - {year}.csv`.
- Combine standings các năm thành một dataframe có cột `year`.
- Tạo các field:
  - `position_group`: Champion, Top 4, Top 8, Other.
  - `team_appearances`.
  - `best_position`.
  - `total_goals_for`.
  - `total_points`.
  - `continent`: lookup từ `international_matches.csv` hoặc mapping thủ công.
- Làm **Dominance Page** gồm:
  - Bar chart: số lần vô địch theo đội.
  - Stacked bar hoặc heatmap: top 4 theo continent qua các kỳ.
  - Ranked table: team, appearances, best position, goals for, points.
  - Insight card: Europe vs South America title count.
- Filter:
  - Year range.
  - Team.
  - Continent.
  - Position group.

### Definition of Done

- Page chạy độc lập khi import vào app.
- Có ít nhất 3 visual.
- Table sort được theo appearances, goals, points, best position.
- Click/filter không làm chart bị rỗng lỗi.
- Có ít nhất 2 insight ngắn để dùng cho report/slides.

### Cần gửi feedback cho leader

- Danh sách field mới đã tạo.
- Mapping continent nếu có sửa tay.
- Ảnh chụp page sau khi chọn filter mặc định.
- Quyết định xử lý Germany/West Germany là gộp hay tách.
- Lỗi dữ liệu hoặc chart còn tồn tại nếu có.

## Trọng - Upsets & Competitiveness Page

### Vai trò

Làm page phân tích mức độ cạnh tranh và các trận upset từ `international_matches.csv`.

### Đầu việc

- Đọc `international_matches.csv`.
- Tạo các field:
  - `year`.
  - `home_goal_diff = home_team_score - away_team_score`.
  - `rank_gap = home_team_fifa_rank - away_team_fifa_rank`.
  - `winner`.
  - `winner_rank`.
  - `loser_rank`.
  - `is_upset`: đội thắng có FIFA rank kém hơn.
  - `upset_rank_gap`.
- Làm **Upsets & Competitiveness Page** gồm:
  - KPI cards: total matches, home win rate, draw rate, neutral matches, shoot-out matches.
  - Scatter plot: rank gap vs goal difference.
  - Bar chart: top biggest upsets by rank gap.
  - Stacked bar: result by neutral location.
  - Detail panel hoặc table: thông tin trận được click.
- Filter:
  - Year range.
  - Tournament.
  - Team.
  - Continent.
  - Neutral location.
  - Shoot-out.

### Definition of Done

- Page load được dataset lớn mà không quá chậm.
- Scatter có hover tooltip rõ: date, teams, score, ranks, tournament.
- Top upset chart đúng logic: chỉ lấy trận đội rank kém hơn thắng.
- Có thể click một trận/upset để xem chi tiết.
- Filter không gây lỗi khi không có dữ liệu phù hợp.

### Cần gửi feedback cho leader

- Định nghĩa chính xác của `is_upset`.
- Danh sách top 5 upset mặc định để nhóm kiểm tra logic.
- Báo nếu cần giới hạn số điểm scatter để tối ưu hiệu năng.
- Ảnh chụp page với filter mặc định.
- Lỗi dữ liệu hoặc callback còn tồn tại nếu có.

## Đức - Tournament Detail Template + Story/QA

### Vai trò

- Làm page template chi tiết theo từng kỳ World Cup.
- Tập trung phân tích sâu World Cup 2022 cho report và presentation.
- Hỗ trợ QA storytelling toàn dashboard.

### Đầu việc

- Đọc toàn bộ file `FIFA - {year}.csv`.
- Combine thành dataframe có cột `year`.
- Tạo dropdown chọn `year`.
- Làm **Tournament Detail Template** gồm:
  - Dropdown chọn năm World Cup.
  - Ranking table theo năm được chọn.
  - Bar chart: goals for theo team.
  - Bar chart: goals against theo team.
  - Scatter plot: goals for vs goals against, color theo position group.
  - Highlight cards cho top 4 của năm được chọn.
- Mặc định dropdown chọn **2022**.
- Viết phần phân tích riêng cho 2022:
  - Argentina vô địch.
  - France có sức tấn công mạnh.
  - Croatia ổn định trong top 3.
  - Morocco là case outsider nổi bật khi vào top 4.
- Hỗ trợ QA nội dung storytelling toàn dashboard:
  - Mạch kể chuyện có rõ không.
  - Tiêu đề chart có dễ hiểu không.
  - Insight có khớp với visual không.

### Definition of Done

- Page dùng được cho nhiều năm, không hard-code riêng 2022 trong chart.
- Mặc định mở page là năm 2022.
- Khi đổi năm, table, bar charts, scatter và highlight cards cập nhật đúng.
- Phần report/slides chỉ phân tích sâu năm 2022.
- Có ít nhất 1 screenshot cho trạng thái năm 2022.

### Cần gửi feedback cho leader

- Danh sách năm có thể chọn.
- Ảnh chụp page ở trạng thái mặc định 2022.
- Báo nếu năm nào thiếu field hoặc dữ liệu bất thường.
- Đoạn insight 2022 ngắn để đưa vào slide/report.
- Lỗi UI/storytelling còn tồn tại nếu có.

## 3. Chuẩn chung cho mọi component

Mỗi người phải đảm bảo:

- File page không phụ thuộc trực tiếp vào code chưa merge của người khác, trừ theme/helper chung do leader cung cấp.
- Tất cả chart có title, axis label và hover tooltip.
- Tên component id trong Dash phải có prefix theo page để tránh trùng:
  - `overview-`
  - `dominance-`
  - `upsets-`
  - `tournament-`
- Không sửa dữ liệu gốc trong `Data/`.
- Nếu cần cleaned data, ưu tiên tạo dataframe trong code. Chỉ export file cleaned data khi thống nhất với leader.
- Filter mặc định phải hiển thị dữ liệu có ý nghĩa, không để trang mở ra bị trống.
- Mỗi page có ít nhất 3 visual.
- Mỗi page có ít nhất 2 tương tác, ví dụ:
  - Filter.
  - Sort.
  - Hover tooltip.
  - Click detail.
  - Dropdown chọn năm.

## 4. Quy trình feedback và merge

### Thành viên gửi lại cho leader

Mỗi người cần gửi:

- File page hoặc branch/code phần mình làm.
- Ảnh chụp màn hình page.
- Mô tả ngắn:
  - Dữ liệu dùng.
  - Field tạo thêm.
  - Callback chính.
  - Lỗi còn tồn tại.
- Checklist Definition of Done đã tick.
- Các quyết định xử lý dữ liệu quan trọng.

### Leader chỉ merge khi

- Page chạy được riêng.
- Không trùng callback id.
- Không làm app chính crash.
- Visual không bị lỗi layout rõ ràng.
- Có screenshot và mô tả insight đi kèm.
- Các field/callback quan trọng đã được ghi lại.

## 5. Test plan trước deadline

Trước deadline **31/05/2026**, nhóm cần kiểm tra:

- Chạy `python app.py` mở được dashboard.
- Chuyển qua lại 4 page không lỗi.
- Tất cả filter hoạt động.
- Click/hover/detail panel hoạt động ở các page có tương tác.
- Dropdown năm ở Tournament Detail Template đổi được nhiều năm.
- Tournament Detail mặc định là năm 2022.
- Dashboard không bị trắng khi filter về dữ liệu ít.
- Screenshot cho report gồm:
  - Overview.
  - Dominance.
  - Upsets & Competitiveness.
  - Tournament Detail năm 2022.
- Các số liệu quan trọng khớp với data local:
  - 22 kỳ World Cup.
  - 9 đội từng vô địch.
  - Brazil 5 lần vô địch.
  - Europe 12 titles.
  - South America 10 titles.
  - `international_matches.csv` có 23,921 trận.

## 6. Assumptions

- Deadline dashboard là **31/05/2026**.
- Công cụ chính là **Dash + Plotly + pandas**.
- Không cần chia timeline chi tiết theo ngày.
- Mỗi người làm end-to-end một component/page.
- Khánh là leader và chịu trách nhiệm merge.
- Page phân tích 2022 được đổi thành template chọn năm, nhưng nội dung phân tích chính vẫn là World Cup 2022.
- Report và slides có thể làm sau dựa trên dashboard final và `dashboard_storytelling.md`.
