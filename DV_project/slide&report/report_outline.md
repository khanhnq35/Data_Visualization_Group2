# Dàn ý sơ bộ báo cáo — FIFA World Cup Dashboard

## 0. Thông tin định hướng

- **Ngôn ngữ báo cáo:** Tiếng Việt.
- **Định dạng làm việc:** Viết Markdown trước, sau đó chuyển sang `.docx`.
- **Độ dài mục tiêu:** Tối đa khoảng 20 trang.
- **Đối tượng đọc:** Giảng viên, người cần hiểu nhóm đã chọn dữ liệu gì, thiết kế dashboard ra sao, áp dụng kỹ thuật trực quan hóa như thế nào, và rút ra insight gì.
- **Góc nhìn báo cáo:** Báo cáo của cả nhóm, không cần phần phân công thành viên.
- **Công cụ dashboard:** Dash + Plotly + Pandas.
- **Dashboard final:** 4 page:
  1. Executive Overview
  2. Dominance
  3. Upsets & Competitiveness
  4. Tournament Detail
- **Trọng tâm đặc biệt:** Phần **Technique Application** theo chapter của môn học.

---

## 1. Đề xuất cấu trúc báo cáo tổng thể

Báo cáo nên đi theo mạch:

1. **Introduction** — giới thiệu bài toán, mục tiêu, câu hỏi phân tích.
2. **Dataset Description** — mô tả nguồn dữ liệu, phạm vi, biến chính, xử lý dữ liệu.
3. **Dashboard Design** — mô tả cấu trúc dashboard, từng page, chart, interaction.
4. **Insight Analysis** — tổng hợp các insight chính rút ra từ dashboard.
5. **Technique Application** — phân tích các kỹ thuật visualization theo từng chapter.
6. **Conclusion** — kết luận, hạn chế, hướng phát triển.
7. **References / Appendix** — nguồn dữ liệu, GitHub, screenshot phụ nếu cần.

---

## 2. Ước lượng độ dài theo trang

| Phần | Số trang gợi ý | Ghi chú |
|---|---:|---|
| Cover + mục lục | 1–2 | Nếu format Word yêu cầu |
| 1. Introduction | 1.5–2 | Nêu bài toán và mục tiêu |
| 2. Dataset Description | 2–3 | Có bảng mô tả dataset |
| 3. Dashboard Design | 4–5 | Có screenshot 4 page |
| 4. Insight Analysis | 2–3 | Tập trung insight chính |
| 5. Technique Application | 6–8 | Phần quan trọng nhất |
| 6. Conclusion | 1–1.5 | Kết luận + future work |
| References / Appendix | 1–2 | Kaggle, GitHub, ảnh phụ |
| **Tổng** | **18–20** | Phù hợp giới hạn 20 trang |

---

# 1. Introduction

## 1.1. Bối cảnh

Viết ngắn gọn về FIFA World Cup như một giải đấu có lịch sử dài, dữ liệu phong phú và phù hợp để phân tích trực quan. World Cup có nhiều chiều dữ liệu: thời gian, đội tuyển, quốc gia chủ nhà, nhà vô địch, bàn thắng, ranking và kết quả từng trận.

Gợi ý nội dung:

- World Cup là giải đấu bóng đá quốc tế lớn, có lịch sử từ năm 1930 đến 2022 trong phạm vi dữ liệu.
- Dữ liệu World Cup không chỉ cho biết đội nào vô địch, mà còn cho phép phân tích xu hướng phát triển của giải đấu.
- Dashboard được xây dựng để giúp người xem khám phá câu chuyện: World Cup mở rộng về quy mô, nhưng danh hiệu vô địch có thật sự phân tán hơn không?

## 1.2. Mục tiêu dự án

Mục tiêu chính:

- Xây dựng một dashboard tương tác để phân tích dữ liệu FIFA World Cup.
- Trực quan hóa xu hướng dài hạn về quy mô giải đấu, bàn thắng và nhà vô địch.
- Phân tích sự thống trị của các đội tuyển/khu vực.
- Phân tích mức độ khó đoán của các trận đấu thông qua FIFA ranking và kết quả thực tế.
- Cung cấp trang drilldown để xem chi tiết từng kỳ World Cup, tập trung case study World Cup 2022.

## 1.3. Câu hỏi phân tích chính

Câu hỏi trung tâm của dashboard:

> World Cup đã thật sự trở thành một giải đấu toàn cầu hơn, hay chức vô địch vẫn nằm trong tay một nhóm đội tuyển elite?

Các câu hỏi phụ:

1. Quy mô World Cup thay đổi như thế nào từ 1930 đến 2022?
2. Những đội tuyển nào thống trị lịch sử World Cup?
3. Thành công ở World Cup có tập trung theo châu lục không?
4. FIFA ranking có phản ánh chắc chắn kết quả từng trận đấu không?
5. World Cup 2022 thể hiện những đặc điểm gì đáng chú ý?

## 1.4. Phạm vi báo cáo

- Báo cáo tập trung vào dashboard final gồm 4 page.
- Dữ liệu được phân tích trong phạm vi năm có trong dataset.
- Phần `international_matches.csv` chỉ dùng trong phạm vi dữ liệu có sẵn, không suy rộng ra ngoài dataset.
- Báo cáo tập trung vào thiết kế visualization, interaction và insight, không đi sâu vào code implementation.

---

# 2. Dataset Description

## 2.1. Nguồn dữ liệu

Dữ liệu lấy từ Kaggle:

1. FIFA Football World Cup Dataset  
   https://www.kaggle.com/datasets/iamsouravbanerjee/fifa-football-world-cup-dataset/data

2. FIFA World Cup 2022 Dataset  
   https://www.kaggle.com/datasets/brenda89/fifa-world-cup-2022/data

Cần coding agent kiểm tra lại trong project để xác nhận chính xác file nào đang được dùng.

## 2.2. Các nhóm dữ liệu chính

| Nhóm dữ liệu | Phạm vi | Vai trò trong dashboard |
|---|---|---|
| `FIFA - World Cup Summary.csv` | Các kỳ World Cup từ 1930–2022 | Phân tích xu hướng dài hạn, KPI, champion timeline |
| `FIFA - {year}.csv` | Bảng xếp hạng đội tuyển theo từng kỳ World Cup | Phân tích standings, top 4, bàn thắng, điểm số |
| `international_matches.csv` | Các trận quốc tế hiện đại trong dataset | Phân tích ranking gap, upset, sân nhà/sân trung lập |

## 2.3. Các biến chính

### Biến định danh / nominal

- `team`
- `champion`
- `runner-up`
- `host`
- `continent`
- `tournament`
- `home_team`
- `away_team`

### Biến thứ bậc / ordinal

- `position`
- `position_group`
- `rank`
- `best_position`

### Biến định lượng / quantitative

- `year`
- `teams`
- `matches`
- `goals`
- `average_goals_per_game`
- `goals_for`
- `goals_against`
- `points`
- `home_team_score`
- `away_team_score`
- `home_team_fifa_rank`
- `away_team_fifa_rank`
- `rank_gap`
- `goal_difference`

## 2.4. Tiền xử lý dữ liệu

Cần coding agent đọc code để xác nhận chính xác. Dựa trên thiết kế dashboard, báo cáo nên có các nội dung sau:

- Đọc dữ liệu bằng Pandas.
- Chuẩn hóa tên cột để dễ xử lý.
- Kết hợp các file standings từng năm thành một dataframe chung có cột `year`.
- Tạo các field mới phục vụ visualization:
  - `goals_per_game`
  - `position_group`
  - `team_appearances`
  - `best_position`
  - `total_goals_for`
  - `total_points`
  - `rank_gap`
  - `home_goal_diff`
  - `winner`
  - `is_upset`
  - `upset_rank_gap`
- Dùng cache để tăng hiệu năng load dữ liệu.
- Người dùng cho biết dữ liệu không có missing value, nhưng coding agent cần kiểm tra lại bằng code.

## 2.5. Hạn chế dữ liệu

Gợi ý viết:

- Phân tích chỉ nằm trong phạm vi dữ liệu có sẵn.
- Dữ liệu `international_matches.csv` có phạm vi thời gian riêng, không bao phủ toàn bộ lịch sử World Cup từ 1930.
- Một số tên đội có yếu tố lịch sử như Germany / West Germany cần được xử lý hoặc giải thích rõ nếu giữ tách riêng.
- Dataset phù hợp cho phân tích visualization, nhưng không nhằm xây dựng mô hình dự đoán chính thức.

---

# 3. Dashboard Design

## 3.1. Tổng quan thiết kế dashboard

Dashboard được thiết kế theo mạch kể chuyện:

1. **Overview:** World Cup mở rộng theo thời gian.
2. **Dominance:** Lớn hơn không có nghĩa là cân bằng hơn.
3. **Upsets & Competitiveness:** Từng trận đấu vẫn có nhiều bất ngờ.
4. **Tournament Detail:** Phân tích chi tiết từng kỳ World Cup, đặc biệt là 2022.

## 3.2. Công nghệ sử dụng

Nội dung cần viết:

- **Pandas:** đọc, làm sạch và biến đổi dữ liệu.
- **Plotly:** tạo biểu đồ tương tác.
- **Dash:** xây dựng web dashboard nhiều trang.
- **CSS:** tạo layout, card, spacing và responsive UI.

Không cần đi quá sâu vào code, chỉ cần nêu vai trò của từng công cụ.

## 3.3. Cấu trúc dashboard

Có thể mô tả theo sơ đồ:

```text
CSV Data
   ↓
Pandas Data Processing
   ↓
Plotly Figures
   ↓
Dash Multi-page App
   ↓
Interactive Dashboard
```

Các page chính:

| Page | Mục đích | Visual chính |
|---|---|---|
| Executive Overview | Tóm tắt quy mô, xu hướng ghi bàn, lịch sử nhà vô địch | KPI cards, line chart, champion timeline |
| Dominance | Phân tích đội/khu vực thống trị | Bar chart, stacked bar, ranked table |
| Upsets & Competitiveness | Phân tích bất ngờ và tính cạnh tranh | Scatter plot, top upset bar, stacked bar |
| Tournament Detail | Drilldown từng kỳ World Cup | Top 4 cards, goals bar, scatter, ranking table |

---

## 3.4. Page 1 — Executive Overview

### Mục tiêu

Giúp người xem nắm bức tranh tổng quan về lịch sử World Cup.

### Thành phần chính

- Filter: year range, host, champion.
- KPI cards:
  - Tournaments
  - Team entries
  - Matches
  - Goals
  - Champion nations
- Line chart:
  - Số đội tham dự.
  - Số trận đấu.
  - Tổng bàn thắng.
- Line chart average goals per game.
- Champion timeline.

### Screenshot cần chèn

- Ảnh Overview phần KPI + line charts.
- Ảnh Champion Timeline.

### Insight chính

- World Cup mở rộng mạnh về số đội và số trận.
- Tổng số bàn thắng tăng theo quy mô giải đấu.
- Trung bình bàn thắng/trận dao động theo từng giai đoạn.
- Lịch sử vô địch vẫn xoay quanh một nhóm đội quen thuộc.

---

## 3.5. Page 2 — Dominance

### Mục tiêu

Phân tích sự tập trung quyền lực trong lịch sử World Cup.

### Thành phần chính

- Filter:
  - year range
  - team
  - continent
  - position group
- KPI cards:
  - tournaments
  - teams
  - titles
  - top 4 finishes
- Bar chart tổng bàn thắng theo đội.
- Các chart khác cần coding agent xác nhận từ code:
  - số lần vô địch theo đội
  - top 4 theo châu lục
  - ranked table

### Screenshot cần chèn

- Ảnh Dominance page.

### Insight chính

- Dù World Cup ngày càng mở rộng, danh hiệu vẫn tập trung.
- Một số đội như Brazil, Argentina, France, Germany/West Germany, Italy có thành tích nổi bật.
- Dominance không chỉ thể hiện ở số chức vô địch mà còn ở số lần vào sâu, tổng bàn thắng và điểm số.

---

## 3.6. Page 3 — Upsets & Competitiveness

### Mục tiêu

Cho thấy FIFA ranking không quyết định hoàn toàn kết quả trận đấu.

### Thành phần chính

- KPI cards:
  - Matches
  - Upsets
  - Home win rate
  - Draw rate
  - Away win rate
  - Neutral matches
- Scatter plot:
  - X: chênh lệch hạng FIFA.
  - Y: chênh lệch bàn thắng.
  - Màu: upset vs kết quả thông thường.
- Bar chart:
  - Top 5 upset lớn nhất theo chênh lệch hạng.
- Stacked bar:
  - Kết quả trận theo loại địa điểm thi đấu.
- Click detail / hover tooltip.

### Screenshot cần chèn

- Ảnh Upsets & Competitiveness page.

### Insight chính

- Có nhiều trận đội bị đánh giá thấp hơn vẫn thắng.
- Chênh lệch FIFA ranking có liên quan tới kết quả, nhưng không phải yếu tố quyết định tuyệt đối.
- Địa điểm thi đấu có ảnh hưởng tới tỷ lệ kết quả.

---

## 3.7. Page 4 — Tournament Detail

### Mục tiêu

Cho phép người dùng drilldown vào từng kỳ World Cup, với World Cup 2022 làm case study chính.

### Thành phần chính

- Dropdown chọn năm.
- Top 4 cards:
  - Champion
  - Runner-up
  - 3rd place
  - 4th place
- KPI cards:
  - host country
  - teams
  - matches played
  - total goals
  - average goals / match
- Bar chart:
  - Bàn ghi được theo đội.
  - Bàn thủng lưới theo đội.
- Scatter plot:
  - Bàn ghi vs bàn thủng.
  - Màu theo position group.
  - Đường tham chiếu GF = GA.
- Ranking table.

### Screenshot cần chèn

- Ảnh Tournament Detail 2022 phần top cards + goals charts.
- Ảnh scatter bàn ghi vs bàn thủng năm 2022.

### Insight chính

- Argentina vô địch World Cup 2022.
- France có sức tấn công nổi bật.
- Croatia tiếp tục ổn định trong nhóm đầu.
- Morocco là outsider nổi bật khi lọt vào top 4.
- Scatter GF vs GA giúp so sánh cân bằng tấn công/phòng ngự.

---

# 4. Insight Analysis

## 4.1. Insight 1 — World Cup mở rộng mạnh về quy mô

Dựa trên Overview page:

- Số đội tham dự tăng theo thời gian.
- Số trận đấu tăng cùng quá trình mở rộng thể thức.
- Tổng bàn thắng tăng một phần do số trận nhiều hơn.

Cách viết:

> Dashboard cho thấy World Cup đã thay đổi từ một giải đấu quy mô nhỏ thành một sự kiện toàn cầu với số đội và số trận tăng đáng kể. Việc dùng line chart theo thời gian giúp người xem nhận ra các giai đoạn mở rộng của giải đấu.

## 4.2. Insight 2 — Mở rộng không đồng nghĩa với cân bằng danh hiệu

Dựa trên Dominance page:

- Số đội từng vô địch thấp so với số đội đã tham dự.
- Một nhóm đội elite vẫn chiếm phần lớn danh hiệu.
- Thành tích nổi bật có thể đo bằng nhiều chỉ số: titles, top 4, goals, points.

Cách viết:

> Mặc dù số đội tham dự World Cup tăng lên, chức vô địch vẫn không phân bổ đều. Điều này cho thấy sự toàn cầu hóa về quy mô không nhất thiết đồng nghĩa với sự cân bằng về thành tích.

## 4.3. Insight 3 — Từng trận đấu vẫn có nhiều bất ngờ

Dựa trên Upsets page:

- Có nhiều điểm upset được highlight trên scatter plot.
- Top upset chart cho thấy vẫn tồn tại các trận đội có ranking thấp hơn thắng đội mạnh hơn.
- Ranking có giá trị tham khảo nhưng không phải yếu tố quyết định tuyệt đối.

Cách viết:

> Ở cấp độ từng trận, bóng đá vẫn giữ tính khó đoán. Một đội có FIFA ranking thấp hơn vẫn có thể giành chiến thắng, đặc biệt trong các bối cảnh thi đấu cụ thể.

## 4.4. Insight 4 — World Cup 2022 minh họa tốt cho toàn bộ câu chuyện

Dựa trên Tournament Detail:

- Argentina và France đại diện cho nhóm elite vẫn rất mạnh.
- Croatia cho thấy sự ổn định.
- Morocco là outsider nổi bật.
- Top 4 năm 2022 phản ánh sự kết hợp giữa quyền lực truyền thống và bất ngờ.

Cách viết:

> World Cup 2022 cho thấy cả hai mặt của câu chuyện: nhóm đội mạnh truyền thống vẫn giữ vị trí cao, nhưng một đội ngoài nhóm elite như Morocco vẫn có thể tạo ra đột phá đáng chú ý.

---

# 5. Technique Application

Đây là phần quan trọng nhất của báo cáo. Nên trình bày theo từng chapter liên quan. Không cần cover tất cả chapter nếu không áp dụng.

## 5.1. Chapter 1 — Visualization Purpose and Dataset Choice

### Techniques / Principles Applied

- Visualization dùng để biến dữ liệu dạng bảng thành insight dễ hiểu.
- Dashboard có thể phục vụ cả exploratory analysis và explanatory storytelling.
- Chọn dataset phù hợp với câu hỏi phân tích.

### How Applied in the Dashboard

Dashboard được thiết kế để trả lời câu hỏi về sự phát triển và mức độ tập trung quyền lực trong lịch sử World Cup. Dữ liệu World Cup phù hợp để trực quan hóa vì có nhiều biến theo thời gian, đội tuyển, quốc gia, khu vực và kết quả trận đấu.

Các page kết hợp hai mục đích:

- **Explanatory:** dẫn dắt người xem theo story Overview → Dominance → Upsets → Tournament Detail.
- **Exploratory:** cho phép người dùng lọc năm, đội, châu lục, tournament và tự khám phá dữ liệu.

### Notes / Adjustments

- Dashboard không nhằm dự đoán kết quả bóng đá.
- Mục tiêu chính là giải thích và khám phá dữ liệu lịch sử.

---

## 5.2. Chapter 2 — Data Types, Marks, and Visual Channels

### Techniques / Principles Applied

- Phân loại dữ liệu:
  - Nominal: đội tuyển, châu lục, nhà vô địch, chủ nhà.
  - Ordinal: thứ hạng, nhóm vị trí.
  - Quantitative: bàn thắng, số trận, điểm số, rank gap.
- Visual marks:
  - Line
  - Point
  - Bar
  - Card
  - Table
- Visual channels:
  - Position
  - Length
  - Color
  - Shape
  - Size

### How Applied in the Dashboard

| Dashboard element | Data type | Mark / channel | Lý do |
|---|---|---|---|
| Line chart quy mô World Cup | Year + quantitative values | Line + position | Phù hợp để thể hiện trend theo thời gian |
| Bar chart tổng bàn thắng / số lần vô địch | Team + quantitative values | Bar + length | So sánh amount/ranking rõ ràng |
| Champion timeline | Year + champion | Point + position + shape | Thể hiện nhà vô địch theo thời gian |
| Upset scatter | Rank gap + goal difference | Point + position + color | Thể hiện quan hệ 2 biến định lượng và highlight upset |
| Tournament scatter | Goals for + goals against | Point + position + color | So sánh cân bằng tấn công/phòng ngự |
| KPI cards | Quantitative summaries | Text/card | Tóm tắt nhanh chỉ số quan trọng |

### Notes / Adjustments

- Color chủ yếu dùng cho phân nhóm và highlight, không dùng để mã hóa quá nhiều biến cùng lúc.
- Dashboard ưu tiên position và length vì đây là các kênh dễ đọc hơn size/area/angle.
- Nếu có chart dùng size cho điểm scatter, cần giải thích size chỉ mang tính hỗ trợ, không phải kênh đọc chính.

---

## 5.3. Chapter 3 — Perception, Pre-attentive Processing, and Gestalt

### Techniques / Principles Applied

- Pre-attentive attributes:
  - Color highlight.
  - Bar length.
  - Position.
  - Shape marker.
- Gestalt principles:
  - Proximity.
  - Similarity.
  - Continuity.
  - Common region.
- Magnitude estimation:
  - Ưu tiên length/position thay vì area/angle khi cần so sánh định lượng.

### How Applied in the Dashboard

- **Upsets page:** điểm upset được tô màu cam nổi bật trên nền điểm thường màu xám, giúp người xem nhận ra bất ngờ nhanh.
- **Tournament Detail:** nhóm Champion, Top 4, Top 8, Other được mã hóa bằng màu nhất quán.
- **KPI cards:** các chỉ số cùng loại được đặt gần nhau và có style giống nhau, áp dụng proximity và similarity.
- **Line charts:** continuity giúp người xem theo dõi xu hướng qua thời gian.
- **Horizontal bar charts:** dùng độ dài thanh để so sánh thành tích đội tuyển, tránh dùng pie chart vì angle/area khó so sánh hơn.

### Notes / Adjustments

- Các màu highlight phải được dùng tiết chế để không gây rối.
- Một số biểu đồ có nhiều điểm dữ liệu, nên cần hover tooltip để xem chi tiết thay vì hiển thị toàn bộ label trên chart.

---

## 5.4. Chapter 4 — Chart Types and Analytical Tasks

### Techniques / Principles Applied

Các chart type được chọn theo nhiệm vụ phân tích:

| Analytical task | Chart type phù hợp |
|---|---|
| Trend over time | Line chart |
| Amount / ranking | Bar chart |
| Relationship | Scatter plot |
| Composition / comparison by group | Stacked bar chart |
| Detail lookup | Table |
| Summary | KPI cards |

### How Applied in the Dashboard

- **Overview:** line chart dùng cho xu hướng số đội, số trận, tổng bàn thắng và average goals per game.
- **Dominance:** bar chart dùng để so sánh thành tích giữa các đội.
- **Upsets:** scatter plot dùng để xem quan hệ giữa rank gap và goal difference.
- **Tournament Detail:** scatter GF vs GA dùng để phân tích cân bằng tấn công/phòng ngự.
- **Tables:** dùng khi cần xem chi tiết standings hoặc thống kê tổng hợp.

### Notes / Adjustments

- Không dùng uncertainty visualization vì dataset không có trường uncertainty/confidence interval.
- Không dùng 3D chart vì không cần thiết và có thể làm sai lệch nhận thức.
- Coordinate system chủ yếu là Cartesian, phù hợp với bar, line và scatter chart.

---

## 5.5. Chapter 5 — Graph Data

### Techniques / Principles Applied

Chapter 5 không phải trọng tâm vì dashboard không sử dụng graph/network data.

### How Applied in the Dashboard

Không có node-edge relationship, không có force-directed layout, không có hierarchical graph.

### Notes / Adjustments

Có thể bỏ qua chapter này trong báo cáo chính hoặc viết ngắn:

> Dự án không sử dụng graph/network visualization vì dữ liệu chính là dữ liệu bảng theo năm, đội tuyển, trận đấu và chỉ số thống kê. Do đó các kỹ thuật node-edge layout trong Chapter 5 không được áp dụng.

---

## 5.6. Chapter 6 — Visual Design, Proportional Ink, Color, and Accessibility

### Techniques / Principles Applied

- Proportional ink.
- Avoid unnecessary 3D.
- Color palette consistency.
- Accessibility / CVD-safe color.
- Data-context balance.
- Title và caption rõ ràng.
- Multi-panel layout.
- Handling overlap.

### How Applied in the Dashboard

- **Bar charts:** bắt đầu từ baseline 0 để đảm bảo proportional ink.
- **Không dùng 3D chart:** tránh làm méo nhận thức độ dài/diện tích.
- **Color palette:** dùng teal, amber, purple, gray nhất quán trên toàn dashboard.
- **CVD-safe colors:** upset dùng orange, home/away dùng blue-orange-gray, position group dùng amber/teal/purple/gray.
- **Titles:** chart title ngắn, mô tả đúng nội dung.
- **Annotations/reference line:** dùng để bổ sung context trực tiếp trên chart.
- **Scatter plot:** dùng opacity/hover để xử lý nhiều điểm dữ liệu.
- **Layout:** các chart được đặt trong card, có spacing rõ ràng và responsive design.

### Notes / Adjustments

- Một số chart có nhiều điểm dữ liệu nên không hiển thị label cho tất cả điểm, tránh clutter.
- Insight không được nhồi vào title quá dài; thay vào đó dùng annotation, highlight và insight card.
- Nếu chưa có reset filter ở tất cả page, có thể nêu là improvement hoặc kiểm tra code final.

---

## 5.7. Chapter 7 — Map Visualization

### Techniques / Principles Applied

Chapter 7 chỉ liên quan nếu dashboard có map.

### How Applied in the Dashboard

Dashboard final không sử dụng map visualization.

### Notes / Adjustments

Lý do không dùng map:

- Dashboard tập trung vào xu hướng lịch sử, đội tuyển, ranking và kết quả trận đấu hơn là phân tích địa lý chi tiết.
- Dữ liệu hiện tại chưa được chuẩn hóa đầy đủ cho geospatial encoding.
- Việc thêm map có thể là hướng phát triển tương lai, ví dụ:
  - choropleth map số lần vô địch theo quốc gia
  - symbol map cho host countries
  - map phân bố top 4 theo châu lục/quốc gia

Có thể viết ngắn trong báo cáo hoặc đưa vào future work.

---

## 5.8. Chapter 8 — Interaction Techniques

### Techniques / Principles Applied

- Filter.
- Select.
- Change view.
- Hover tooltip.
- Click detail.
- Sorting table.
- Multi-page navigation.

### How Applied in the Dashboard

| Interaction | Page áp dụng | Vai trò |
|---|---|---|
| Year range filter | Overview, Dominance, Upsets | Giới hạn phạm vi thời gian |
| Host/champion filter | Overview | So sánh theo chủ nhà/nhà vô địch |
| Team/continent/position filter | Dominance | Khám phá dominance theo nhóm |
| Tournament/team/neutral filter | Upsets | Lọc trận theo ngữ cảnh |
| Dropdown chọn year | Tournament Detail | Chuyển đổi kỳ World Cup |
| Hover tooltip | Hầu hết chart | Xem thông tin chi tiết |
| Click detail panel | Upsets | Drilldown vào trận cụ thể |
| Sort table | Dominance/Tournament | Tra cứu và so sánh chi tiết |

### Notes / Adjustments

- Interaction hỗ trợ exploratory analysis, nhưng dashboard vẫn giữ story flow cố định qua thứ tự page.
- Không dùng animation vì không cần thiết cho mục tiêu phân tích chính và có thể làm giảm khả năng so sánh tĩnh.
- Empty state nên được xử lý để khi filter không có dữ liệu, người dùng không thấy chart trống khó hiểu.

---

## 5.9. Chapter 9 — Storytelling and Narrative Visualization

### Techniques / Principles Applied

- Narrative structure.
- Guided storytelling.
- Overview first, details later.
- Annotation và insight cards.
- Kết hợp giữa guided story và user exploration.

### How Applied in the Dashboard

Dashboard đi theo narrative:

1. **Overview:** thiết lập bức tranh lớn — World Cup mở rộng.
2. **Dominance:** đặt vấn đề — mở rộng nhưng danh hiệu vẫn tập trung.
3. **Upsets:** cân bằng câu chuyện — từng trận vẫn có bất ngờ.
4. **Tournament Detail:** minh họa bằng case study 2022.

Các yếu tố storytelling:

- Thứ tự page phản ánh logic kể chuyện.
- Chart title mô tả ngắn gọn.
- Insight cards giúp người xem hiểu “so what”.
- Annotations/reference lines giúp dẫn dắt người xem ngay trên biểu đồ.
- Filter/dropdown cho phép người xem tự khám phá sau khi nắm narrative chính.

### Notes / Adjustments

- Dashboard không phải slideshow tuyến tính hoàn toàn; nó là sự kết hợp giữa narrative dashboard và exploratory dashboard.
- Báo cáo nên nhấn mạnh rằng story không khóa người dùng vào một đường duy nhất, mà cung cấp mạch chính để khám phá dữ liệu.

---

# 6. Conclusion

## 6.1. Tổng kết kết quả

Gợi ý viết:

> Dự án đã xây dựng một dashboard tương tác phân tích dữ liệu FIFA World Cup bằng Dash, Plotly và Pandas. Dashboard tổ chức dữ liệu theo 4 page chính, đi từ xu hướng tổng quan đến phân tích dominance, upset và drilldown từng kỳ World Cup. Kết quả cho thấy World Cup ngày càng mở rộng về quy mô, nhưng chức vô địch vẫn tập trung trong nhóm elite; đồng thời, ở cấp độ từng trận, bóng đá vẫn có nhiều bất ngờ.

## 6.2. Đóng góp chính của dashboard

- Tổ chức dữ liệu World Cup thành một câu chuyện trực quan rõ ràng.
- Sử dụng nhiều loại biểu đồ phù hợp với từng nhiệm vụ phân tích.
- Áp dụng filter, hover, click detail và dropdown để hỗ trợ exploration.
- Áp dụng nguyên tắc visualization về encoding, perception, color, proportional ink và storytelling.

## 6.3. Hạn chế

- Chưa có map visualization cho chiều địa lý.
- Phân tích ranking/upset phụ thuộc vào phạm vi dữ liệu `international_matches.csv`.
- Một số mapping như continent hoặc chuẩn hóa tên đội cần xác nhận kỹ từ code.
- Dashboard không nhằm dự đoán kết quả, chỉ phục vụ phân tích trực quan.

## 6.4. Hướng phát triển

- Thêm choropleth/symbol map để phân tích địa lý thành công.
- Thêm small multiples cho so sánh khu vực theo giai đoạn.
- Thêm phần export report hoặc snapshot dashboard.
- Tối ưu thêm performance nếu số điểm scatter lớn.
- Bổ sung thêm dữ liệu World Cup mới khi có.

---

# 7. References

Cần đưa vào báo cáo:

1. Kaggle — FIFA Football World Cup Dataset  
   https://www.kaggle.com/datasets/iamsouravbanerjee/fifa-football-world-cup-dataset/data

2. Kaggle — FIFA World Cup 2022 Dataset  
   https://www.kaggle.com/datasets/brenda89/fifa-world-cup-2022/data

3. GitHub source code  
   `[Điền link GitHub project]`

4. Tài liệu bài giảng / course chapters  
   `[Điền tên môn học hoặc slide/chapter nếu thầy yêu cầu]`

---

# 8. Appendix gợi ý

## Appendix A — Screenshot dashboard

Nên chèn:

1. Executive Overview — KPI + line charts.
2. Executive Overview — Champion timeline.
3. Dominance page.
4. Upsets & Competitiveness page.
5. Tournament Detail 2022 — top cards + goals charts.
6. Tournament Detail 2022 — GF vs GA scatter.

## Appendix B — Data fields

Sau khi coding agent đọc code, có thể bổ sung bảng:

| Field | Source | Description | Used in page |
|---|---|---|---|

## Appendix C — Derived fields

Sau khi coding agent đọc code, có thể bổ sung bảng:

| Derived field | Formula / logic | Purpose |
|---|---|---|

---

# 9. Các chỗ cần coding agent xác nhận thêm

Do hiện tại chưa đọc trực tiếp toàn bộ source code final, cần coding agent kiểm tra các điểm sau trước khi viết báo cáo hoàn chỉnh:

1. Chính xác các file dữ liệu đang được load.
2. Số dòng, số cột của từng dataset.
3. Có thật sự không có missing value không.
4. Các field được tạo thêm trong `src/data.py` hoặc các page.
5. Logic chuẩn hóa tên đội, nếu có.
6. Logic mapping continent, nếu có.
7. Chính xác danh sách chart final trong từng page.
8. Các interaction final trong từng page.
9. Đường reference line, annotation, CVD-safe color đã áp dụng ở đâu.
10. Link GitHub final.
11. Vị trí screenshot trong repository hoặc thư mục báo cáo.

---

# 10. Prompt cho coding agent hoàn thiện báo cáo

```text
Bạn là coding/report agent hỗ trợ hoàn thiện báo cáo cho dự án Data Visualization Dashboard.

Ngữ cảnh dự án:
- Dự án là FIFA World Cup Dashboard.
- Dashboard được xây dựng bằng Dash + Plotly + Pandas.
- Báo cáo cần viết bằng tiếng Việt, tối đa khoảng 20 trang khi chuyển sang Word.
- Báo cáo sẽ viết bằng Markdown trước, sau đó convert sang `.docx`.
- Báo cáo là của cả nhóm, không cần phần phân công thành viên.
- Báo cáo cần giúp giảng viên hiểu:
  1. Nhóm chọn bài toán gì.
  2. Dữ liệu lấy từ đâu và xử lý như thế nào.
  3. Dashboard được thiết kế ra sao.
  4. Các biểu đồ/interaction dùng để rút ra insight gì.
  5. Nhóm đã áp dụng các kỹ thuật visualization trong môn học như thế nào.

Nguồn dữ liệu:
1. Kaggle — FIFA Football World Cup Dataset:
   https://www.kaggle.com/datasets/iamsouravbanerjee/fifa-football-world-cup-dataset/data
2. Kaggle — FIFA World Cup 2022 Dataset:
   https://www.kaggle.com/datasets/brenda89/fifa-world-cup-2022/data

Dashboard final có 4 page:
1. Executive Overview
2. Dominance
3. Upsets & Competitiveness
4. Tournament Detail

Các screenshot dashboard đã có/hoặc sẽ được đặt trong thư mục report, gồm:
- Executive Overview: KPI + line charts
- Executive Overview: Champion timeline
- Dominance page
- Upsets & Competitiveness page
- Tournament Detail 2022: top cards + goals charts
- Tournament Detail 2022: GF vs GA scatter

Yêu cầu nhiệm vụ:
1. Đọc toàn bộ project source code, đặc biệt:
   - `app.py`
   - `pages/overview.py`
   - `pages/dominance.py`
   - `pages/upsets.py`
   - `pages/tournament.py`
   - `src/data.py`
   - `src/theme.py`
   - `src/components.py`
   - `assets/styles.css`
   - các file markdown plan/report hiện có nếu có
2. Không được đoán bừa. Mọi mô tả về chart, field, transformation, interaction phải kiểm chứng từ code hoặc dữ liệu.
3. Chạy kiểm tra dữ liệu bằng script hoặc notebook ngắn:
   - Liệt kê file dữ liệu được sử dụng.
   - Đếm số dòng/số cột từng dataset.
   - Kiểm tra missing values.
   - Liệt kê các field gốc quan trọng.
   - Liệt kê các field được tạo thêm và công thức/logic tạo ra chúng.
4. Chạy dashboard bằng `python app.py` nếu môi trường cho phép, hoặc ít nhất đọc code để xác nhận app có 4 page và các callback chính.
5. Hoàn thiện báo cáo Markdown theo cấu trúc dưới đây:

# [Tên báo cáo]
## 1. Introduction
- Bối cảnh World Cup và lý do chọn chủ đề.
- Mục tiêu dashboard.
- Câu hỏi phân tích chính:
  “World Cup đã thật sự trở thành một giải đấu toàn cầu hơn, hay chức vô địch vẫn nằm trong tay một nhóm đội tuyển elite?”
- Phạm vi phân tích.

## 2. Dataset Description
- Nguồn dữ liệu Kaggle.
- Bảng mô tả từng file dataset.
- Số dòng/số cột thực tế.
- Các biến chính theo nhóm nominal/ordinal/quantitative.
- Tiền xử lý dữ liệu:
  - đọc data
  - combine standings theo năm
  - chuẩn hóa tên cột/tên đội nếu có
  - mapping continent nếu có
  - derived fields: goals_per_game, position_group, rank_gap, is_upset, upset_rank_gap, goal_difference, v.v.
- Hạn chế dữ liệu.

## 3. Dashboard Design
- Công nghệ sử dụng: Dash, Plotly, Pandas, CSS.
- Cấu trúc multi-page dashboard.
- Storytelling flow:
  Overview → Dominance → Upsets & Competitiveness → Tournament Detail.
- Mô tả từng page:
  ### 3.1 Executive Overview
  - Mục tiêu page.
  - Screenshot.
  - Chart/KPI/filter.
  - Insight chính.
  ### 3.2 Dominance
  - Mục tiêu page.
  - Screenshot.
  - Chart/KPI/filter/table.
  - Insight chính.
  ### 3.3 Upsets & Competitiveness
  - Mục tiêu page.
  - Screenshot.
  - Chart/KPI/filter/click detail.
  - Insight chính.
  ### 3.4 Tournament Detail
  - Mục tiêu page.
  - Screenshot.
  - Dropdown chọn năm.
  - World Cup 2022 case study.
  - Chart/KPI/table.
  - Insight chính.

## 4. Insight Analysis
Viết thành các đoạn phân tích có liên kết, không chỉ bullet.
Các insight nên gồm:
1. World Cup mở rộng mạnh về quy mô.
2. Mở rộng không đồng nghĩa với cân bằng danh hiệu.
3. Europe/South America và nhóm elite vẫn thống trị.
4. Từng trận đấu vẫn có nhiều bất ngờ; FIFA ranking không quyết định tuyệt đối.
5. World Cup 2022 minh họa tốt cho câu chuyện: Argentina, France, Croatia, Morocco.

## 5. Technique Application
Đây là phần quan trọng nhất. Viết theo từng chapter liên quan. Mỗi chapter dùng cấu trúc:
### Chapter X: [Chapter Title]
#### Techniques / Principles Applied
- Liệt kê nguyên tắc/kỹ thuật.
#### How Applied in the Dashboard
- Nêu page/chart cụ thể dùng kỹ thuật đó.
- Giải thích vì sao chart type, encoding, layout hoặc interaction được chọn.
- Chèn screenshot nếu phù hợp.
#### Notes / Adjustments
- Nếu không áp dụng hoặc có trade-off, giải thích rõ.

Các chapter cần cover:
- Chapter 1: Visualization purpose, dataset choice, exploratory/explanatory analysis.
- Chapter 2: Data types, visual marks, visual channels.
- Chapter 3: Pre-attentive processing, Gestalt, magnitude estimation.
- Chapter 4: Chart types for trend, amount, relationship, composition, detail lookup.
- Chapter 5: Graph data — không áp dụng, viết ngắn lý do hoặc bỏ nếu không cần.
- Chapter 6: Proportional ink, color palette, CVD-safe colors, handling overlap, titles/captions, avoiding 3D.
- Chapter 7: Maps — không áp dụng, viết ngắn lý do và đưa vào future work.
- Chapter 8: Interaction techniques: filter, hover, click detail, dropdown, table sort, multi-page navigation.
- Chapter 9: Storytelling: narrative structure, guided story + user exploration, insight cards, annotations.

## 6. Conclusion
- Tóm tắt dashboard đã làm được gì.
- Tóm tắt insight chính.
- Tóm tắt các kỹ thuật visualization đã áp dụng.
- Hạn chế.
- Future work:
  - thêm map visualization
  - thêm small multiples
  - tối ưu scatter performance nếu cần
  - cập nhật dữ liệu mới

## References
- Kaggle datasets
- GitHub project link
- Course materials / chapter slides nếu có

6. Cách viết:
- Viết bằng tiếng Việt học thuật, rõ ràng, không quá dài dòng.
- Ưu tiên đoạn văn có liên kết, hạn chế bullet quá nhiều ở phần phân tích.
- Không viết như README kỹ thuật thuần code.
- Không phóng đại, không khẳng định điều chưa kiểm chứng.
- Nếu chưa có dữ liệu chính xác, ghi TODO rõ ràng thay vì tự bịa.
- Mỗi screenshot phải có caption rõ: “Hình X. ...”.
- Bảng nên có tiêu đề và giải thích ngắn.

7. Output mong muốn:
- Tạo file `report/fifa_worldcup_dashboard_report.md`.
- Nếu có thể, tạo thêm `report/fifa_worldcup_dashboard_report.docx` bằng pandoc hoặc công cụ phù hợp.
- Đảm bảo Markdown có cấu trúc heading rõ ràng để convert sang Word.
- Kiểm tra chính tả và format trước khi kết thúc.
```
