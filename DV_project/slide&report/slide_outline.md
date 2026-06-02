# Outline nội dung slide — FIFA World Cup Dashboard

## Thông tin chung

- **Chủ đề:** FIFA World Cup Dashboard: Tăng trưởng, Thống trị và Bất ngờ
- **Ngôn ngữ slide:** Tiếng Việt
- **Thời lượng phần slide:** Khoảng 10 phút
- **Sau slide:** 5–10 phút dashboard demo + 5–10 phút Q&A
- **Người thuyết trình:** 1 người
- **Công cụ dashboard:** Dash + Plotly + Pandas
- **Hướng trình bày:** Giới thiệu bài toán → thiết kế dashboard/visualization → phân tích insight → chuyển sang demo
- **Định dạng slide dự kiến:** HTML slide 16:9

---

## Style chung cho HTML slide

### 1. Layout tổng thể

- Nên dùng format **16:9**.
- Mỗi slide chỉ tập trung vào **1 ý chính**.
- Ưu tiên bố cục:
  - Hero slide.
  - Two-column layout.
  - KPI card layout.
  - Timeline layout.
  - Screenshot + insight cards.
  - Grid cards.
- Các slide nói về dashboard page nên dùng **screenshot thật** để người xem dễ liên hệ khi sang phần demo.

### 2. Gợi ý màu sắc

- **Teal / accent chính:** `#007c89`
- **Amber / highlight:** `#d98324`
- **Purple / phụ trợ:** `#7c3aed`
- **Gray text:** `#64727d`
- **Background:** `#f6f8fb`
- **Surface card:** `#ffffff`

### 3. Font và hierarchy

- Title slide: 44–56px.
- Slide title: 32–40px.
- Subtitle / section label: 20–24px.
- Body text: 18–22px.
- Speaker-friendly bullet: tối đa 3–5 bullet mỗi slide.
- Không nên đưa quá nhiều chữ; phần giải thích chi tiết để nói khi thuyết trình.

### 4. Screenshot cần chuẩn bị

Nên chuẩn bị screenshot final của các page sau:

- Overview page.
- Dominance page.
- Upsets & Competitiveness page.
- Tournament Detail page ở năm 2022.
- Nếu có thể, chụp thêm crop riêng:
  - Line chart scale / average goals.
  - Champion bar chart.
  - Upset scatter plot.
  - Tournament GF vs GA scatter.

---

# Slide 1 — Title

## Tiêu đề

**FIFA World Cup Dashboard**  
**Tăng trưởng, Thống trị và Bất ngờ**

## Mục tiêu slide

Mở đầu bài thuyết trình, giới thiệu nhanh chủ đề dashboard và hướng phân tích.

## Bố cục HTML đề xuất

- Layout: **full-screen hero**.
- Background:
  - Ảnh sân bóng / World Cup / screenshot dashboard làm mờ.
  - Overlay màu tối nhẹ để chữ nổi bật.
- Trung tâm slide:
  - Title lớn.
  - Subtitle nhỏ.
- Góc dưới:
  - Tên nhóm.
  - Tên môn học.
  - Công cụ: Dash + Plotly + Pandas.

## Nội dung hiển thị trên slide

```text
FIFA World Cup Dashboard
Tăng trưởng, Thống trị và Bất ngờ

Dash + Plotly + Pandas
Nhóm ...
```

## Speaker notes

Trong bài thuyết trình này, em sẽ giới thiệu dashboard phân tích lịch sử FIFA World Cup. Dashboard không chỉ liệt kê số liệu, mà được thiết kế theo một câu chuyện dữ liệu: World Cup ngày càng mở rộng, nhưng chức vô địch vẫn tập trung vào một nhóm đội tuyển elite, trong khi từng trận đấu vẫn có nhiều bất ngờ.

---

# Slide 2 — Bài toán phân tích

## Tiêu đề

**World Cup có thật sự toàn cầu hơn?**

## Mục tiêu slide

Giới thiệu câu hỏi trung tâm của dashboard và lý do cần trực quan hóa dữ liệu.

## Bố cục HTML đề xuất

- Layout: **2 cột**.
- Cột trái:
  - Một câu hỏi lớn đặt ở giữa.
- Cột phải:
  - 3 question cards:
    1. Quy mô giải đấu có tăng không?
    2. Chức vô địch có phân tán hơn không?
    3. Từng trận đấu có còn khó đoán không?

## Nội dung hiển thị trên slide

```text
Câu hỏi phân tích chính:

World Cup đã thật sự trở thành một giải đấu toàn cầu,
hay chức vô địch vẫn nằm trong tay một nhóm đội tuyển elite?
```

```text
Dashboard cần trả lời:
1. World Cup mở rộng như thế nào qua thời gian?
2. Đội tuyển / khu vực nào đang thống trị?
3. FIFA ranking có dự đoán chính xác kết quả trận đấu không?
```

## Speaker notes

Thay vì chỉ xem đội nào vô địch từng năm, dashboard đặt câu hỏi rộng hơn: sự mở rộng của World Cup có dẫn đến sự cân bằng hơn không? Hay dù số đội tăng, chức vô địch vẫn thuộc về một nhóm nhỏ? Từ đó dashboard được thiết kế để đi từ xu hướng tổng quan đến phân tích đội tuyển, trận đấu và cuối cùng là một case study cụ thể.

---

# Slide 3 — Dataset Overview

## Tiêu đề

**Dữ liệu sử dụng**

## Mục tiêu slide

Cho người nghe hiểu dashboard dựa trên dữ liệu nào và mỗi nguồn dữ liệu dùng để làm gì.

## Bố cục HTML đề xuất

- Hàng trên: **4 KPI cards**.
- Hàng dưới: **bảng 3 nguồn dữ liệu**.

## Nội dung hiển thị trên slide

### KPI cards

```text
22
Kỳ World Cup
1930–2022
```

```text
23,921
Trận quốc tế
1993–2022
```

```text
9
Đội từng vô địch
```

```text
5
Chức vô địch của Brazil
```

### Bảng nguồn dữ liệu

| Nguồn dữ liệu | Nội dung chính | Vai trò trong dashboard |
|---|---|---|
| `FIFA - World Cup Summary.csv` | Year, host, champion, teams, matches, goals | Phân tích xu hướng dài hạn |
| `FIFA - {year}.csv` | Position, team, games, goals, points | Phân tích standings từng kỳ World Cup |
| `international_matches.csv` | Teams, FIFA ranks, scores, tournament, neutral location | Phân tích competitiveness và upset |

## Speaker notes

Dashboard kết hợp dữ liệu ở hai tầng. Tầng thứ nhất là dữ liệu World Cup theo từng kỳ, dùng để phân tích xu hướng dài hạn và nhà vô địch. Tầng thứ hai là dữ liệu trận đấu quốc tế hiện đại, dùng để phân tích mức độ khó đoán của từng trận dựa trên chênh lệch FIFA ranking và kết quả thực tế.

---

# Slide 4 — Storytelling Flow

## Tiêu đề

**Mạch kể chuyện của dashboard**

## Mục tiêu slide

Giải thích dashboard không phải tập hợp biểu đồ rời rạc, mà được tổ chức theo một narrative rõ ràng.

## Bố cục HTML đề xuất

- Layout: **timeline ngang 4 bước**.
- Mỗi bước gồm:
  - Icon.
  - Tên act.
  - Một câu mô tả ngắn.

## Nội dung hiển thị trên slide

```text
1. Expansion
World Cup ngày càng lớn hơn về số đội, số trận và quy mô tổ chức.

2. Dominance
Lớn hơn không đồng nghĩa với cân bằng hơn: chức vô địch vẫn tập trung.

3. Upsets
Ở cấp độ từng trận, bóng đá vẫn khó đoán và có nhiều bất ngờ.

4. 2022 Case Study
World Cup 2022 minh họa rõ sự kết hợp giữa elite teams và outsider.
```

## Speaker notes

Mạch kể chuyện của dashboard gồm 4 phần. Đầu tiên là sự mở rộng của World Cup. Sau đó dashboard chuyển sang câu hỏi liệu sự mở rộng đó có làm quyền lực phân tán hơn không. Tiếp theo là phần upset để cho thấy dù danh hiệu tập trung, từng trận đấu vẫn rất khó đoán. Cuối cùng là Tournament Detail, trong đó World Cup 2022 được dùng như case study.

---

# Slide 5 — Công cụ và cấu trúc dashboard

## Tiêu đề

**Dashboard được xây dựng như thế nào?**

## Mục tiêu slide

Giới thiệu ngắn về công nghệ và cấu trúc dashboard, không đi quá sâu vào code.

## Bố cục HTML đề xuất

- Layout: **2 cột**.
- Cột trái: sơ đồ pipeline.
- Cột phải: danh sách 4 page.

## Nội dung hiển thị trên slide

### Pipeline

```text
CSV Data
   ↓
Pandas
   ↓
Plotly Charts
   ↓
Dash Multi-page App
```

### Các page chính

```text
1. Overview
2. Dominance
3. Upsets & Competitiveness
4. Tournament Detail
```

## Speaker notes

Về mặt kỹ thuật, dashboard được xây dựng bằng Dash, Plotly và Pandas. Pandas dùng để đọc và xử lý dữ liệu, Plotly dùng để tạo biểu đồ tương tác, còn Dash dùng để tổ chức thành ứng dụng nhiều trang với filter, callback và navigation. Trong phần thuyết trình này, em chỉ nói ngắn về công cụ, trọng tâm vẫn là thiết kế trực quan hóa và insight.

---

# Slide 6 — Overview Page

## Tiêu đề

**Overview: World Cup mở rộng theo thời gian**

## Mục tiêu slide

Giới thiệu page đầu tiên và insight tổng quan về sự tăng trưởng quy mô World Cup.

## Bố cục HTML đề xuất

- Layout: **screenshot + insight panel**.
- Bên trái 65%:
  - Screenshot Overview page.
- Bên phải 35%:
  - 3 insight cards.
- Nếu screenshot quá rộng, có thể dùng 1 screenshot chính + 1 crop line chart nhỏ.

## Nội dung hiển thị trên slide

```text
Page Overview trả lời:
World Cup đã thay đổi quy mô như thế nào qua thời gian?
```

### Insight cards

```text
Số đội tăng mạnh
Từ 13 đội ở kỳ đầu lên 32 đội ở giai đoạn hiện đại.
```

```text
Số trận và tổng bàn thắng tăng
Quy mô giải đấu lớn hơn kéo theo nhiều trận và nhiều bàn thắng hơn.
```

```text
Bàn thắng / trận thay đổi theo thời kỳ
Average goals per game không tăng đều, mà dao động theo từng giai đoạn lịch sử.
```

## Chart cần highlight

- KPI cards.
- Line chart: teams, matches, goals theo year.
- Average goals per game.
- Champion timeline.

## Speaker notes

Trang Overview là điểm bắt đầu của câu chuyện. Mục tiêu của page này là cho người xem thấy World Cup đã lớn lên như thế nào qua gần một thế kỷ. Các KPI cards cung cấp bức tranh nhanh, còn line chart cho thấy xu hướng tăng về số đội, số trận và tổng bàn thắng. Đây là nền tảng để sang slide sau đặt câu hỏi: giải đấu lớn hơn thì có cân bằng hơn không?

---

# Slide 7 — Thiết kế visualization ở Overview

## Tiêu đề

**Vì sao dùng line chart và annotation?**

## Mục tiêu slide

Giải thích lựa chọn biểu đồ và kỹ thuật visualization dùng trong Overview.

## Bố cục HTML đề xuất

- Layout: **2 cột**.
- Cột trái:
  - Crop line chart Overview.
- Cột phải:
  - 4 design cards:
    1. Line chart.
    2. Marker.
    3. Annotation.
    4. Reference line.

## Nội dung hiển thị trên slide

```text
Line chart
Phù hợp để biểu diễn xu hướng theo thời gian.
```

```text
Marker
World Cup diễn ra theo từng kỳ, nên marker giúp nhấn mạnh các điểm dữ liệu rời rạc.
```

```text
Annotation / Highlight
Đánh dấu các mốc quan trọng trực tiếp trên biểu đồ.
```

```text
Reference line
Tạo ngữ cảnh so sánh, giúp người xem biết giá trị đang cao hay thấp hơn mức trung bình.
```

## Speaker notes

Ở page Overview, line chart được dùng vì dữ liệu có yếu tố thời gian. Tuy nhiên, World Cup không phải dữ liệu liên tục từng năm, mà là dữ liệu theo từng kỳ, nên marker giúp người xem thấy rõ từng điểm dữ liệu. Ngoài ra, thay vì viết insight dài trong tiêu đề, dashboard dùng annotation, highlight và reference line để insight hiện trực tiếp trên biểu đồ. Cách này giúp người xem hiểu nhanh mà không cần đọc quá nhiều mô tả.

---

# Slide 8 — Dominance Page

## Tiêu đề

**Dominance: Lớn hơn không có nghĩa là cân bằng hơn**

## Mục tiêu slide

Chuyển từ “World Cup mở rộng” sang “quyền lực vô địch vẫn tập trung”.

## Bố cục HTML đề xuất

- Layout: **screenshot + insight cards**.
- Bên trái:
  - Screenshot Dominance page.
- Bên phải:
  - 3 insight cards.
- Có thể crop riêng champion bar chart để nhấn mạnh Brazil / nhóm elite.

## Nội dung hiển thị trên slide

```text
Page Dominance trả lời:
Đội tuyển và khu vực nào kiểm soát lịch sử World Cup?
```

### Insight cards

```text
Chỉ 9 đội từng vô địch
Dù World Cup có 22 kỳ, danh hiệu chỉ thuộc về một nhóm rất nhỏ.
```

```text
Europe và South America thống trị
Hai khu vực này chiếm toàn bộ chức vô địch trong dữ liệu.
```

```text
Brazil nổi bật nhất
Brazil là đội có số lần vô địch nhiều nhất trong dữ liệu summary.
```

## Chart cần highlight

- Horizontal bar chart: số lần vô địch theo đội.
- Stacked bar chart: top 4 theo châu lục.
- Ranked table: appearances, best position, goals, points.

## Speaker notes

Sau khi thấy World Cup mở rộng, câu hỏi tiếp theo là sự mở rộng đó có tạo ra sự cân bằng hơn không. Trang Dominance cho thấy câu trả lời là chưa hẳn. Chỉ có một nhóm nhỏ đội tuyển từng vô địch, và phần lớn thành công vẫn tập trung vào châu Âu và Nam Mỹ. Đây là phần quan trọng nhất để chứng minh thông điệp: World Cup toàn cầu hơn về quy mô, nhưng chưa thật sự phân tán về quyền lực vô địch.

---

# Slide 9 — Thiết kế visualization ở Dominance

## Tiêu đề

**So sánh thành tích bằng bar chart và table**

## Mục tiêu slide

Giải thích vì sao các biểu đồ ở Dominance phù hợp với câu hỏi phân tích.

## Bố cục HTML đề xuất

- Layout: **3 cột**.
- Cột 1: Horizontal bar chart.
- Cột 2: Stacked bar chart.
- Cột 3: Ranked table.
- Mỗi cột có 1 dòng giải thích ngắn.

## Nội dung hiển thị trên slide

```text
Horizontal bar chart
Dùng để so sánh số lần vô địch giữa các đội.
Độ dài thanh giúp người xem nhận ra đội dẫn đầu nhanh hơn.
```

```text
Stacked bar chart
Dùng để nhìn phân bố Top 4 theo châu lục qua các kỳ.
Phù hợp để thể hiện mức độ tập trung theo khu vực.
```

```text
Ranked table
Dùng cho tra cứu chi tiết:
appearances, best position, total goals, total points.
```

## Speaker notes

Ở page Dominance, bar chart được dùng thay vì pie chart vì mục tiêu là so sánh giá trị giữa các đội. Với dữ liệu dạng ranking hoặc count, độ dài thanh giúp người xem so sánh chính xác hơn. Stacked bar được dùng để thấy phân bố top 4 theo châu lục, còn table dùng cho các thông tin chi tiết không thể đưa hết vào biểu đồ.

---

# Slide 10 — Upsets & Competitiveness Page

## Tiêu đề

**Upsets: Ranking không quyết định tất cả**

## Mục tiêu slide

Giới thiệu phần phân tích tính cạnh tranh và các trận bất ngờ.

## Bố cục HTML đề xuất

- Layout: **2 cột + insight footer**.
- Cột trái:
  - Screenshot scatter plot rank gap vs goal difference.
- Cột phải:
  - Screenshot top upset bar hoặc detail panel.
- Dưới cùng:
  - Một câu insight lớn.

## Nội dung hiển thị trên slide

```text
Page Upsets trả lời:
FIFA ranking có dự đoán hoàn toàn kết quả trận đấu không?
```

### Insight footer

```text
Dù chức vô địch tập trung, từng trận đấu vẫn có thể tạo ra bất ngờ.
```

## Chart cần highlight

- Scatter plot: rank gap vs goal difference.
- Top 5 upsets bar chart.
- Result by neutral location.
- Click detail panel.

## Speaker notes

Trang Upsets làm cho câu chuyện cân bằng hơn. Nếu chỉ nhìn vào danh hiệu, World Cup có vẻ bị thống trị bởi nhóm elite. Nhưng khi nhìn ở cấp độ từng trận, kết quả vẫn có nhiều bất ngờ. Scatter plot giúp xem quan hệ giữa chênh lệch ranking và chênh lệch bàn thắng, trong khi các điểm upset được highlight để người xem thấy những trận đội bị đánh giá thấp hơn vẫn thắng.

---

# Slide 11 — Tournament Detail 2022

## Tiêu đề

**World Cup 2022: Case Study**

## Mục tiêu slide

Dùng World Cup 2022 làm ví dụ cụ thể để kết nối toàn bộ câu chuyện.

## Bố cục HTML đề xuất

- Layout: **screenshot + 4 cards**.
- Bên trái 60–65%:
  - Screenshot Tournament Detail page với dropdown chọn 2022.
- Bên phải 35–40%:
  - 4 team cards:
    - Argentina.
    - France.
    - Croatia.
    - Morocco.

## Nội dung hiển thị trên slide

```text
Tournament Detail là template để xem từng kỳ World Cup.
Trong phần trình bày, dashboard tập trung phân tích World Cup 2022.
```

### Team cards

```text
Argentina
Nhà vô địch World Cup 2022.
```

```text
France
Đội có sức tấn công nổi bật trong nhóm dẫn đầu.
```

```text
Croatia
Tiếp tục duy trì vị trí cao trong top 3.
```

```text
Morocco
Outsider nổi bật khi lọt vào top 4.
```

## Chart cần highlight

- Ranking table.
- Goals for.
- Goals against.
- GF vs GA scatter.
- Top 4 cards.

## Speaker notes

Trang Tournament Detail là một template có thể chọn nhiều năm World Cup khác nhau, nhưng phần thuyết trình tập trung vào năm 2022. Năm 2022 minh họa tốt cho toàn bộ câu chuyện: Argentina và France đại diện cho nhóm elite vẫn rất mạnh, Croatia cho thấy sự ổn định ở nhóm đầu, trong khi Morocco là outsider nổi bật khi lọt vào top 4.

---

# Slide 12 — Key Takeaways & Demo Transition

## Tiêu đề

**Key Takeaways**

## Mục tiêu slide

Tóm tắt insight chính và chuyển mượt sang phần dashboard demo.

## Bố cục HTML đề xuất

- Layout: **4 insight cards lớn**.
- Dòng cuối: demo flow.

## Nội dung hiển thị trên slide

### Insight cards

```text
1. World Cup ngày càng mở rộng
Số đội, số trận và quy mô giải đấu tăng mạnh theo thời gian.
```

```text
2. Quyền lực vô địch vẫn tập trung
Chỉ một nhóm nhỏ đội tuyển từng vô địch World Cup.
```

```text
3. Europe và South America vẫn thống trị
Thành công ở vòng cuối chủ yếu đến từ hai khu vực này.
```

```text
4. Từng trận đấu vẫn có bất ngờ
FIFA ranking không quyết định hoàn toàn kết quả trận đấu.
```

### Demo transition

```text
Demo flow:
Overview → Dominance → Upsets & Competitiveness → Tournament Detail 2022
```

## Speaker notes

Tóm lại, dashboard cho thấy World Cup đã mở rộng mạnh về quy mô, nhưng chức vô địch vẫn tập trung vào nhóm elite. Tuy nhiên, ở cấp độ từng trận, bóng đá vẫn có nhiều bất ngờ. Sau phần slide, em sẽ demo dashboard theo đúng mạch kể chuyện này: bắt đầu từ Overview, sau đó sang Dominance, Upsets và cuối cùng là Tournament Detail 2022.

---

# Gợi ý flow demo sau slide

## Demo 1 — Overview

Mục tiêu nói:
- Chỉ vào KPI cards.
- Chỉ vào line chart quy mô.
- Nói: World Cup tăng từ giải nhỏ thành giải quy mô lớn hơn nhiều.

## Demo 2 — Dominance

Mục tiêu nói:
- Chỉ vào champion bar chart.
- Nói: dù giải mở rộng, chức vô địch vẫn tập trung.
- Chỉ vào stacked bar / table để nói thêm về châu lục và đội tuyển.

## Demo 3 — Upsets & Competitiveness

Mục tiêu nói:
- Chỉ vào scatter plot.
- Giải thích rank gap và goal difference.
- Click vào một điểm hoặc một upset để mở detail panel.

## Demo 4 — Tournament Detail 2022

Mục tiêu nói:
- Chọn năm 2022.
- Chỉ vào top 4 cards.
- Chỉ vào goals for / goals against / scatter.
- Kết luận bằng Argentina, France, Croatia, Morocco.

---

# Gợi ý cấu trúc HTML slide

Có thể chia HTML theo các section như sau:

```html
<section class="slide title-slide">
  <!-- Slide 1 -->
</section>

<section class="slide two-column">
  <!-- Slide 2 -->
</section>

<section class="slide kpi-table-layout">
  <!-- Slide 3 -->
</section>

<section class="slide timeline-layout">
  <!-- Slide 4 -->
</section>

<section class="slide two-column">
  <!-- Slide 5 -->
</section>

<section class="slide screenshot-insight-layout">
  <!-- Slide 6 -->
</section>

<section class="slide visual-design-layout">
  <!-- Slide 7 -->
</section>

<section class="slide screenshot-insight-layout">
  <!-- Slide 8 -->
</section>

<section class="slide three-column-layout">
  <!-- Slide 9 -->
</section>

<section class="slide screenshot-two-column">
  <!-- Slide 10 -->
</section>

<section class="slide screenshot-card-layout">
  <!-- Slide 11 -->
</section>

<section class="slide takeaway-layout">
  <!-- Slide 12 -->
</section>
```

---

# Checklist trước khi dựng HTML slide

- [ ] Có screenshot đủ 4 page chính.
- [ ] Screenshot không bị mờ, không dính thanh browser nếu không cần.
- [ ] Mỗi slide không quá 5 bullet.
- [ ] Các slide 6, 8, 10, 11 có screenshot thật.
- [ ] Các slide 7, 9, 11 có giải thích kỹ thuật visualization.
- [ ] Slide 12 có câu chuyển sang demo.
- [ ] Demo flow giống với flow storytelling trong slide.
- [ ] Không đưa quá nhiều code vào slide.
- [ ] Giữ nhất quán màu sắc với dashboard.
