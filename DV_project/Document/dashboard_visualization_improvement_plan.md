# Kế hoạch Cải tiến Trực quan hóa Dashboard

> **Phiên bản:** 1.0 | **Ngày:** 02/06/2026 | **Đối tượng:** Nhóm phát triển Dashboard FIFA World Cup  
> **Dự án:** `c:\Users\Admin\Uni\Data_Visualization_Group2\DV_project\`  
> **Câu chuyện chủ đạo:** "World Cup ngày càng mở rộng toàn cầu, nhưng chức vô địch vẫn tập trung ở nhóm elite; dữ liệu trận đấu hiện đại cho thấy vẫn có nhiều bất ngờ."

---

## 1. Bối cảnh Dự án

Dashboard FIFA World Cup là một ứng dụng phân tích dữ liệu được xây dựng bằng **Dash + Plotly + Pandas**, triển khai theo kiến trúc đa trang (multi-page), phân tích lịch sử 22 kỳ World Cup từ 1930 đến 2022. Dự án được hoàn thành theo kế hoạch phân công nêu trong `dashboard_work_plan.md` với deadline **31/05/2026**.

**Câu hỏi storytelling cốt lõi:** World Cup đã thật sự trở thành một giải đấu toàn cầu, hay chức vô địch vẫn nằm trong tay một nhóm đội tuyển elite?

**Dữ liệu sử dụng:**

| Nguồn dữ liệu | Phạm vi | Vai trò |
|---|---|---|
| `Data/archive/FIFA - World Cup Summary.csv` | 22 kỳ World Cup (1930–2022) | Xu hướng dài hạn, KPI, champion timeline |
| `Data/archive/FIFA - {year}.csv` | Bảng xếp hạng từng năm | Standings, top-4 cards, scatter goals |
| `Data/international_matches.csv` | 23,921 trận quốc tế (1993–2022) | Phân tích upset, rank gap, neutral location |

**Công nghệ:** Dash (Python), Plotly Graph Objects / Express, Pandas, CSS Grid, `lru_cache` cho tối ưu hiệu năng.

---

## 2. Cấu trúc Dự án và Bằng chứng

| File / Module | Chức năng | Trạng thái xác minh |
|---|---|---|
| `app.py` | App shell, sidebar navigation, routing, callback registration | Verified from code |
| `pages/overview.py` | KPI cards, scale line chart (3 subplots), avg goals line chart, champion timeline scatter | Verified from code |
| `pages/dominance.py` | KPI cards, champion bar chart, stacked bar by continent, goals bar chart, ranked DataTable | Verified from code |
| `pages/upsets.py` | KPI cards, scatter rank gap vs goal diff, top-5 upsets bar chart, neutral stacked bar, click detail panel | Verified from code |
| `pages/tournament.py` | Year dropdown, top-4 KPI cards, meta strip, goals for/against bar charts, scatter GF vs GA, standings DataTable, 2022 insight panel | Verified from code |
| `src/theme.py` | `COLORS` dict, Plotly template "worldcup", `apply_chart_layout()`, `empty_figure()` | Verified from code |
| `src/components.py` | `page_header()`, `kpi_card()`, `graph_card()` | Verified from code |
| `src/data.py` | `load_world_cup_summary()`, `load_upsets_data()`, `load_world_cup_standings()`, `lru_cache` | Verified from code |
| `assets/styles.css` | CSS Grid layout, sidebar, KPI cards, filter-panel, responsive breakpoints | Verified from code |
| `dashboard_storytelling.md` | Story arc, wording transformation, annotation strategy | Verified from code |
| `dashboard_work_plan.md` | Phân công thành viên, definition of done | Verified from code |

---

## 3. Kiểm kê Dashboard Hiện tại

| Trang | Chart ID (Dash) | Loại biểu đồ | Nguồn dữ liệu | Mục đích |
|---|---|---|---|---|
| Overview | `overview-scale-chart` | Line chart (3 subplots: Teams, Matches, Goals) | `load_world_cup_summary()` | Tăng trưởng quy mô giải đấu theo năm |
| Overview | `overview-avg-goals-chart` | Line chart + hline trung bình | `load_world_cup_summary()` | Xu hướng bàn thắng/trận theo thời kỳ |
| Overview | `overview-champion-timeline` | Bubble scatter (year × champion_norm) | `load_world_cup_summary()` | Lịch sử nhà vô địch, kích thước = số đội |
| Dominance | `dominance-champion-bar` | Horizontal bar chart | `ALL_STANDINGS` | Số lần vô địch theo đội |
| Dominance | `dominance-top4-by-continent` | Stacked bar (Year × continent) | `ALL_STANDINGS` | Top 4 theo châu lục qua các năm |
| Dominance | `dominance-goals-for-chart` | Horizontal bar chart | `ALL_STANDINGS` | Tổng bàn thắng top 20 đội |
| Dominance | `dominance-summary-table` | `dash_table.DataTable` | `ALL_STANDINGS` | Bảng thống kê tổng hợp đội tuyển |
| Upsets | `upsets-scatter-plot` | Scatter (rank_gap × home_goal_diff) | `load_upsets_data()` | Phân tán kết quả theo chênh lệch rank |
| Upsets | `upsets-bar-chart` | Horizontal bar (top 5 upsets) | `load_upsets_data()` | Top 5 bất ngờ lớn nhất |
| Upsets | `upsets-stacked-bar` | Stacked bar (neutral location × result) | `load_upsets_data()` | So sánh tỷ lệ thắng/thua tại sân trung lập |
| Upsets | `upsets-detail-container` | Detail panel (HTML) | clickData từ scatter/bar | Chi tiết trận được click |
| Tournament | `tournament-goals-for-chart` | Horizontal bar (GF × Team) | `_load_year(year)` | Bàn thắng ghi được theo đội |
| Tournament | `tournament-goals-against-chart` | Horizontal bar (GA × Team) | `_load_year(year)` | Bàn thắng bị thủng lưới theo đội |
| Tournament | `tournament-scatter-chart` | Scatter (GF × GA, size=Points) | `_load_year(year)` | Cân bằng tấn công/phòng ngự |
| Tournament | `tournament-ranking-table` | `dash_table.DataTable` | `_load_year(year)` | Bảng xếp hạng đầy đủ năm được chọn |
| Tournament | `tournament-insight-panel` | HTML cards (chỉ năm 2022) | Hard-coded | Câu chuyện top 4 World Cup 2022 |

**Biểu đồ KHÔNG tìm thấy trong code:**
- Choropleth/Symbol Map (đề xuất trong doc7.md) — **Not found** (không được triển khai)
- Small Multiples / Trellis plots — **Not found** (không được triển khai)
- Annotated line chart có chú thích sự kiện lịch sử — **Not found**
- Slope chart thứ hạng trước/sau giải — **Not found**
- Race chart / animated visualization — **Not found**

---

## 4. Đánh giá Tổng thể

### 4.1 Điểm mạnh

1. **Kiến trúc phân tách rõ ràng:** App shell (`app.py`) tách biệt hoàn toàn với logic trang, tuân thủ nguyên tắc separation of concerns. Hàm `register_callbacks(app)` trong từng module page giúp tránh trùng callback ID, phù hợp với yêu cầu trong `dashboard_work_plan.md`.

2. **Hệ thống màu sắc nhất quán:** `COLORS` dict trong `src/theme.py` định nghĩa tập màu thống nhất (`#007c89` accent teal, `#d98324` amber, `#c44536` red). Toàn bộ dashboard sử dụng `apply_chart_layout()` đảm bảo visual consistency. Nền trắng sạch (`surface: #ffffff`) trên nền tổng thể nhạt (`background: #f6f8fb`) tốt cho tỷ lệ Data-Ink.

3. **Lựa chọn biểu đồ phù hợp theo lý thuyết Mackinlay:** Bar chart cho dữ liệu định lượng (số lần vô địch, bàn thắng), scatter plot cho quan hệ Q-Q (rank_gap × goal_diff, GF × GA), line chart cho xu hướng thời gian — tất cả đều ưu tiên kênh Position và Length, đúng theo xếp hạng Mackinlay (Chương 1, 2, 3).

4. **Xử lý trạng thái rỗng:** Hàm `empty_figure()` trong `src/theme.py` đảm bảo không có biểu đồ trắng không giải thích khi filter trả về dữ liệu rỗng, tránh "Dead-end Dashboard" như cảnh báo trong Chương 8.

5. **Tương tác clickData đa tầng:** Trang Upsets triển khai `display_click_data` callback nhận input từ cả `upsets-scatter-plot` và `upsets-bar-chart`, cho phép người dùng drill-down vào chi tiết trận đấu — thực hành Detail-on-demand đúng theo Chương 8.

6. **Hiệu năng dữ liệu:** `lru_cache(maxsize=1)` trong `src/data.py` cho tất cả hàm load dữ liệu, cần thiết với bộ dữ liệu 23,921 trận (`international_matches.csv`). Responsive layout với CSS Grid và 3 breakpoints (1120px, 720px, 460px).

7. **KPI Cards có ngữ cảnh:** Trang Upsets bổ sung `kpi_helper` hiển thị phần trăm upset trên tổng trận (`{upsets / total_matches:.1%} of matches`), tạo "So What?" layer như đề xuất trong Chương 3.

8. **Tách biệt phân tích lịch sử:** Dashboard phân tầng dữ liệu theo nguồn — World Cup standings (lịch sử, 1930–2022) tách riêng với international matches (hiện đại, 1993–2022). Điều này tránh hiểu lầm phạm vi phân tích như ghi chú trong `dashboard_storytelling.md`.

### 4.2 Hạn chế

1. **Tiêu đề biểu đồ chưa nhất quán với chuẩn mô tả rõ ràng:** Một số tiêu đề như "Rank Gap vs Goal Difference" quá kỹ thuật, khó hiểu với người xem phổ thông. Nguyên tắc: **tiêu đề nên là câu mô tả ngắn gọn, chính xác** — không cần chứa insight. Insight phải tự hiện ra qua **design của biểu đồ**: annotation, highlight màu, reference line, và cấu trúc visual. Người xem nhìn vào phải hiểu insight mà không cần đọc thêm bất kỳ chú thích nào.

2. **Không có Strategic Annotations trên biểu đồ:** Biểu đồ line chart trong `overview.py` (`_scale_figure`, `_avg_goals_figure`) không có chú thích tại các mốc lịch sử quan trọng (1954 kỷ lục bàn thắng, 1990 thấp nhất, 1998 mở rộng lên 32 đội). Chương 9 đề xuất dùng `fig.add_annotation()` để dẫn dắt người xem như bản đồ hành quân Minard.

3. **Champion timeline scatter sử dụng kênh Size để mã hóa "số đội" — vi phạm nguyên tắc:** Trong `_champion_timeline_figure()` (`overview.py` dòng 195), `marker_sizes = (df["teams"].fillna(0).clip(lower=12) * 0.75)`. Biến `teams` là Q-Ratio nhưng được mã hóa bằng Size (Area) — một kênh xếp hạng thấp theo Mackinlay cho Q. Kênh Position đang dùng cho Năm (X) và Champion (Y) là hợp lý, nhưng Size cho số đội gây khó so sánh chính xác (Chương 2, 3).

4. **Scatter tournament thiếu zero-baseline reference lines:** `tournament-scatter-chart` trong `tournament.py` dùng `yaxis_autorange="reversed"` nhưng không có đường tham chiếu nào giúp người xem hiểu "điểm cân bằng" (GF = GA). Thiếu `fig.add_shape()` đường diagonal GF = GA. Chương 6 yêu cầu "Chart Context" rõ ràng.

5. **Mã hóa màu sắc upset chưa CVD-safe:** Trang Upsets dùng `COLOR_UPSET = COLORS["accent_3"]` (`#c44536` — đỏ đậm) và `COLOR_NORMAL = "#94a3b8"` (xám). Trong khi cặp này ổn với người bình thường, Chương 8 và 9 đề xuất bắt buộc dùng bảng màu Blue-Orange cho người mù màu đỏ-xanh (8% nam giới). Cụ thể cặp đỏ `#c44536` và xanh lá `#2f855a` (`COLORS["success"]`) trong `POS_COLORS` của `tournament.py` là vấn đề nghiêm trọng.

6. **Không có Insight Cards kết nối storytelling giữa các trang:** Trang Overview, Dominance, Upsets không có text insight giải thích "So What?" như `dashboard_storytelling.md` đề xuất. Chỉ trang Tournament có insight panel (cố định cho 2022). Người xem không được dẫn dắt từ "Quy mô mở rộng" → "Quyền lực tập trung" → "Nhưng vẫn có bất ngờ".

7. **Không có Map Visualization:** Cả 4 trang không có Choropleth Map hoặc Symbol Map dù Chương 7 đề xuất map là "công cụ mạnh nhất để trực quan hóa luận điểm về Địa lý của thành công". Bản đồ sẽ bổ sung chiều không gian thiết yếu cho câu chuyện về sự mở rộng toàn cầu.

8. **Filter Dominance không có "Reset All" rõ ràng:** `dominance-continent-filter` default value là toàn bộ continents (`value=CONTINENT_OPTIONS`), nhưng không có nút "Reset All Filters" rõ ràng. Chương 8 yêu cầu "Reset All Filters là bắt buộc để giải cứu người dùng khỏi mê cung dữ liệu".

### 4.3 Khu vực cần cải thiện khẩn cấp

| Ưu tiên | Vấn đề | File ảnh hưởng | Chương liên quan | Mức độ tác động |
|---|---|---|---|---|
| P0 — Bắt buộc | Tiêu đề biểu đồ chưa chuẩn — một số quá kỹ thuật, một số quá dài. Cần tiêu đề **ngắn, mô tả rõ** — insight phải tự hiện ra qua design (annotation, highlight, reference line) | Tất cả 4 trang | Chương 3, 6, 9 | Người xem không hiểu được insight nếu chỉ nhìn vào biểu đồ |
| P0 — Bắt buộc | Cặp màu đỏ-xanh trong `POS_COLORS` không CVD-safe | `tournament.py`, `theme.py` | Chương 6, 8, 9 | Accessibility nghiêm trọng |
| P1 — Quan trọng | Thiếu Strategic Annotations trên line charts | `overview.py` | Chương 9 | Thiếu ngữ cảnh lịch sử |
| P1 — Quan trọng | Thiếu đường reference GF=GA trên scatter tournament | `tournament.py` | Chương 6 | Khó đọc tương quan |
| P1 — Quan trọng | Thiếu Insight Cards storytelling giữa các trang | `overview.py`, `dominance.py`, `upsets.py` | Chương 9 | Mạch truyện bị đứt |
| P2 — Nên làm | Mã hóa Size cho số đội trong champion timeline không tối ưu | `overview.py` | Chương 1, 3 | Giảm độ chính xác nhận thức |
| P2 — Nên làm | Chưa có Map Visualization | Tất cả trang | Chương 7 | Thiếu chiều không gian |
| P2 — Nên làm | Tooltip chưa có ngữ cảnh so sánh ("So What?") | `overview.py` | Chương 2, 8 | Giảm giá trị insight |
| P3 — Tùy chọn | Thiếu Small Multiples cho so sánh châu lục | `dominance.py` | Chương 4 | Cải thiện so sánh song song |
| P3 — Tùy chọn | Chưa có Annotated Line Chart | `overview.py` | Chương 4, 9 | Cải thiện storytelling xu hướng |

---

## 5. Phân tích và Đề xuất từng Chart

### 5.1 Scale Line Chart — `overview-scale-chart` (`pages/overview.py`)

**Vai trò hiện tại:** Minh họa sự tăng trưởng quy mô giải đấu (số đội, số trận, tổng bàn thắng) theo năm — tương ứng với "Act 1: World Cup ngày càng lớn hơn" trong storytelling.

**Bằng chứng trong code:** Hàm `_scale_figure()` (dòng 120–154 trong `overview.py`) dùng `make_subplots(rows=3, cols=1, shared_xaxes=True)`, 3 trace `go.Scatter` với `mode="lines+markers"`, màu sắc lấy từ `COLORS["accent"]`, `COLORS["accent_2"]`, `COLORS["success"]`.

**Điểm mạnh:**
- Ba subplots chia sẻ trục X (Year) — đúng kỹ thuật Small Multiples cho biến temporal (Chương 4).
- `mode="lines+markers"` với markers tại từng năm World Cup (dữ liệu rời rạc) là đúng theo Chương 6: "nếu các điểm dữ liệu là rời rạc, hãy dùng markers".
- Sử dụng Position (kênh #1 Mackinlay) cho cả X (Year) và Y (giá trị Q-Ratio) — tối ưu.

**Hạn chế:**
- Tiêu đề "Tournament Scale by Year" mô tả chứ không kể chuyện.
- Không có annotation tại các mốc lịch sử quan trọng: 1954 (bàn thắng cao nhất), 1990 (thấp nhất), 1998 (mở rộng 32 đội).
- Subplot titles ("Teams", "Matches", "Goals") là label kỹ thuật, thiếu con số tham chiếu cho người xem.
- Không có index chart (bắt đầu từ 0%) để so sánh tốc độ tăng trưởng tương đối như đề xuất trong Chương 1.

| Thay đổi đề xuất | Cách thực hiện | Chương cơ sở | Ưu tiên |
|---|---|---|---|
| Tiêu đề ngắn gọn: **"Quy mô World Cup theo năm"** — không cần insight trong title | `fig.update_layout(title=...)` | Chương 6 | P0 |
| **Annotation tại 1998** trên subplot Teams: "32 đội" với mũi tên → người xem tự thấy bước nhảy | `fig.add_annotation(x=1998, text="32 đội", arrowhead=2)` trên subplot row=1 | Chương 3, 9 | P1 |
| **Highlight điểm bước ngoặt** bằng marker lớn hơn/màu khác tại 1998 — preattentive pop-out | `marker={"size": [12 if y==1998 else 7 for y in df["year"]]}` | Chương 3 | P1 |
| Annotation tại năm có bàn thắng cao nhất và thấp nhất trên subplot Goals — tự hiện insight | `fig.add_annotation()` tại max/min của `goals_scored` | Chương 3, 9 | P1 |
| Chuyển sang Index Chart (series bắt đầu từ 100%) — tùy chọn bonus | Normalize series | Chương 1 | P3 |

---

### 5.2 Average Goals Line Chart — `overview-avg-goals-chart` (`pages/overview.py`)

**Vai trò hiện tại:** Hiển thị xu hướng trung bình bàn thắng/trận qua các kỳ World Cup, thể hiện sự thay đổi phong cách thi đấu.

**Bằng chứng trong code:** Hàm `_avg_goals_figure()` (dòng 157–184) dùng `go.Scatter` với `mode="lines+markers"`, có `add_hline` đường trung bình dạng dotted, annotation "Selected mean: {value:.2f}".

**Điểm mạnh:**
- Đường `hline` tham chiếu trung bình — đúng kỹ thuật "Reference line" của Chương 6.
- Annotation trung bình đặt "bottom right" hợp lý.

**Hạn chế:**
- Tiêu đề "Average Goals per Game" đúng về mô tả nhưng chưa chuẩn về ngôn ngữ — nên Việt hóa cho nhất quán.
- Không có annotation tại 1954 (5.4 bàn/trận — cao nhất lịch sử) và 1990 (2.2 bàn/trận — thấp nhất): **đây là nơi insight phải nằm trong biểu đồ, không phải trong title**.
- Màu `COLORS["accent_3"]` (đỏ `#c44536`) cho đường duy nhất — màu cảnh báo không phù hợp cho xu hướng trung tính.

| Thay đổi đề xuất | Cách thực hiện | Chương cơ sở | Ưu tiên |
|---|---|---|---|
| Tiêu đề ngắn chuẩn: **"Trung bình bàn thắng / trận"** | `fig.update_layout(title=...)` | Chương 6 | P0 |
| **Annotation trực tiếp** tại điểm max (1954: "5.4 — Kỷ lục") và min (1990: "2.2 — Thấp nhất") — người xem thấy insight không cần đọc title | `fig.add_annotation()` tại max/min, `font_size=11`, màu muted | Chương 3, 9 | P1 |
| **Highlight 2 điểm outlier** bằng marker khác (symbol="diamond", size=12) để tạo pop-out preattentive | `marker={"symbol": [...], "size": [...]}` theo điều kiện | Chương 3 | P1 |
| Đổi màu đường sang `COLORS["accent"]` (teal) — màu trung tính, không gây liên tưởng cảnh báo | `line={"color": COLORS["accent"]}` | Chương 6 | P1 |

---

### 5.3 Champion Timeline — `overview-champion-timeline` (`pages/overview.py`)

**Vai trò hiện tại:** Biểu đồ scatter Year × Champion, thể hiện ai vô địch năm nào, kích thước bubble = số đội, màu = host_won.

**Bằng chứng trong code:** Hàm `_champion_timeline_figure()` (dòng 187–227). `marker_colors` = `COLORS["success"]` nếu host thắng, `COLORS["accent"]` nếu không. `marker_sizes` tính từ `df["teams"] * 0.75`.

**Điểm mạnh:**
- Dùng kênh Position (X=Year, Y=Champion) cho hai biến Q và N — đúng nguyên tắc.
- Mã hóa Host Won bằng màu sắc (Green = host thắng) là preattentive attribute hợp lý.
- Tooltip đầy đủ: Champion, Host, Runner-up, Teams, Matches, Goals.

**Hạn chế:**
- `marker_sizes` mã hóa số đội (Q-Ratio) bằng Size (Area/Diện tích) — theo Mackinlay, Area xếp hạng thứ 5 cho Q, thấp hơn nhiều so với Position và Length. Người xem khó ước tính chính xác rằng 32 đội = 2.46 lần 13 đội từ kích thước bubble (Chương 2, 3).
- Hai màu (host thắng vs không thắng) cần legend nhưng `showlegend=False`. Người xem không hiểu ý nghĩa màu xanh vs teal mà không đọc tooltip.
- Không có annotation cho các đội thống trị (Brazil 5 lần, Germany 4 lần) — thiếu Pop-out Effect (Chương 3).
- Tiêu đề "Champion Timeline" đủ ngắn gọn nhưng chưa rõ phạm vi thời gian.

| Thay đổi đề xuất | Cách thực hiện | Chương cơ sở | Ưu tiên |
|---|---|---|---|
| Tiêu đề ngắn chuẩn: **"Lịch sử nhà vô địch World Cup (1930–2022)"** | `fig.update_layout(title=...)` | Chương 6 | P0 |
| Bỏ mã hóa Size, thay bằng uniform size (12px) — insight về số đội đưa vào tooltip | `marker={"size": 12}` thay vì `marker_sizes` | Chương 2, 3 | P1 |
| Bật legend rõ ràng: "Chủ nhà vô địch ★" / "Đội khách vô địch ●" — người xem tự thấy pattern | `showlegend=True`, tên trace mô tả | Chương 3 | P1 |
| **Annotation trực tiếp** tại hàng Brazil: "5 lần vô địch" — người xem thấy ngay đội nào thống trị nhiều nhất | `fig.add_annotation(x=..., y="Brazil", text="5 lần")` | Chương 3, 9 | P2 |
| Dùng symbol="star" cho host thắng — shape khác biệt dễ nhận hơn chỉ dùng màu | `marker={"symbol": "star"}` cho host_won | Chương 3 | P2 |

---

### 5.4 Champion Bar Chart — `dominance-champion-bar` (`pages/dominance.py`)

**Vai trò hiện tại:** Biểu đồ horizontal bar chart số lần vô địch theo đội (top 20), sắp xếp tăng dần (ascending=True) để bar lớn nhất ở trên cùng khi horizontal.

**Bằng chứng trong code:** Hàm `update_dominance()` (dòng 277–407), `champion_counts = champion_counts.sort_values("titles", ascending=True)` trước khi `.tail(20)`, dùng `px.bar(..., orientation="h", color_discrete_sequence=[COLORS["accent"]])`.

**Điểm mạnh:**
- Horizontal bar chart với Length (Độ dài) mã hóa số lần vô địch (Q-Ratio) — đúng Mackinlay ranking #1 sau Position (Chương 1, 3).
- Sắp xếp thứ tự (`sort_values`) giúp người xem so sánh mà không phải tìm kiếm — đúng nguyên tắc "Sorted" của Chương 1.
- Zero-baseline (trục X bắt đầu từ 0) cho bar chart — tuân thủ Proportional Ink (Chương 6).

**Hạn chế:**
- Tất cả bars cùng màu (`COLORS["accent"]` — teal) — mất cơ hội làm nổi bật (highlight) Brazil/Germany bằng màu khác biệt (Chương 1, 3).
- Tiêu đề "Championship Count by Team" đúng nhưng là tiếng Anh, chưa nhất quán với phần còn lại.
- Tất cả bars cùng màu teal — mất cơ hội **highlight Brazil/Germany bằng màu nổi bật** để người xem thấy ngay ai thống trị mà không cần đọc số.

| Thay đổi đề xuất | Cách thực hiện | Chương cơ sở | Ưu tiên |
|---|---|---|---|
| Tiêu đề ngắn chuẩn: **"Số lần vô địch theo đội"** | `title=...` | Chương 6 | P0 |
| **Highlight Brazil** bằng màu amber đậm, các đội khác muted gray — người xem thấy ngay đội nhiều nhất mà không đọc trục | `color_discrete_map={"Brazil": COLORS["accent_2"], default: "#cbd5e1"}` | Chương 3 | P1 |
| **Annotation trực tiếp** bên phải bar Brazil: "5 lần" — insight tự hiện ra | `fig.add_annotation(x=5, y="Brazil", text="5 lần", showarrow=False)` | Chương 3, 9 | P1 |
| Tô màu bars theo châu lục — người xem thấy pattern EU/SA chiếm ưu thế qua màu sắc | `color="continent"` với bảng màu cố định | Chương 2 | P2 |

---

### 5.5 Stacked Bar Top 4 by Continent — `dominance-top4-by-continent` (`pages/dominance.py`)

**Vai trò hiện tại:** Stacked bar chart theo năm (X) và số lượt top 4 theo châu lục (Y), màu theo continent.

**Bằng chứng trong code:** `top4_fig = px.bar(top4_by_continent, x="Year", y="top4_count", color="continent", ...)` (dòng 357–369).

**Điểm mạnh:**
- Dùng Color Hue (màu sắc theo châu lục) để phân biệt Nominal data (N) — đúng nguyên tắc Mackinlay (Chương 2).
- Stacked bar với Y là Q-Ratio (số lần) phù hợp cho dữ liệu proportions (Chương 4).
- Mỗi cột = 1 kỳ World Cup → thấy rõ châu lục nào chiếm ưu thế từng giai đoạn.

**Hạn chế:**
- Không rõ tổng số màu sắc (số châu lục) — nếu có >7 màu sẽ vi phạm ngưỡng 5-7 màu (Chương 3).
- Thiếu phần tử "Gestalt Enclosure" để phân nhóm giai đoạn lịch sử (13 đội / 16 đội / 24 đội / 32 đội).
- Tiêu đề "Top 4 Finishes by Continent" chỉ mô tả.
- Khi có nhiều năm, các nhãn X bị chồng chéo — cần `tickangle`.

| Thay đổi đề xuất | Cách thực hiện | Chương cơ sở | Ưu tiên |
|---|---|---|---|
| Tiêu đề ngắn chuẩn: **"Số suất Top 4 theo châu lục qua các kỳ"** | `title=...` | Chương 6 | P0 |
| **Gộp châu lục ít xuất hiện** thành "Phần còn lại" — giảm màu, EU và SA nổi bật hơn → người xem thấy ngay 2 châu lục thống trị | `continent_grouped` column | Chương 3 | P1 |
| **Vrect phân tách giai đoạn** thể thức (13/16/24/32 đội) → người xem thấy pattern thay đổi theo thời kỳ | `fig.add_vrect(x0=1930, x1=1950, fillcolor=..., opacity=0.05)` | Chương 3, 9 | P2 |
| Xoay nhãn X 45° tránh chồng chéo | `update_xaxes(tickangle=-45)` | Chương 6 | P1 |

---

### 5.6 Goals For Bar Chart — `dominance-goals-for-chart` (`pages/dominance.py`)

**Vai trò hiện tại:** Horizontal bar chart tổng bàn thắng ghi được của top 20 đội trong lịch sử.

**Bằng chứng trong code:** `goals_fig = px.bar(goals_by_team.tail(20), x="total_goals_for", y="Team", orientation="h", color_discrete_sequence=[COLORS["accent_2"]])` (dòng 381–394).

**Điểm mạnh:**
- Sắp xếp tăng dần (ascending=True) cho bar lớn nhất ở trên — hợp lý cho horizontal bar.
- Zero-baseline tuân thủ.

**Hạn chế:**
- Không chuẩn hóa theo số lần tham dự — Brazil có 5 lần vô địch và 22 lần tham gia sẽ luôn đứng đầu về tổng bàn thắng, không có nghĩa tương đối.
- Không kết nối với câu chuyện "Sức mạnh tấn công của Elite" — cần thêm cột `goals_per_appearance`.
- Đây là biểu đồ bổ trợ nhưng chiếm `chart-wide` (toàn chiều rộng), nhiều không gian hơn cần thiết.

| Thay đổi đề xuất | Cách thực hiện | Chương cơ sở | Ưu tiên |
|---|---|---|---|
| Thêm cột bàn thắng/lần tham dự làm tooltip bổ sung | `hovertemplate="... Avg: {gf/app:.1f}/tournament"` | Chương 2, 8 | P1 |
| Tiêu đề ngắn chuẩn: **"Tổng bàn thắng — Top 20 đội (lịch sử)"** | `title=...` | Chương 6 | P1 |
| Thu gọn về `chart-card` thay vì `chart-wide` nếu không phải Hero Chart | CSS layout | Chương 4 | P2 |

---

### 5.7 Ranked DataTable — `dominance-summary-table` (`pages/dominance.py`)

**Vai trò hiện tại:** Bảng tổng hợp thống kê đội tuyển (appearances, championships, top4, best_position, goals, points), có sort và conditional formatting.

**Bằng chứng trong code:** `dash_table.DataTable(id="dominance-summary-table", ...)` với `style_data_conditional=[{"if": {"filter_query": "{best_position} = 1"}, "color": COLORS["accent_2"], "fontWeight": "700"}]` (dòng 231–267 trong `dominance.py`).

**Điểm mạnh:**
- Conditional formatting highlight Champion (best_position = 1) bằng màu amber — đúng kỹ thuật Highlight Table (Chương 4).
- Zebra striping (alternating row colors) giảm tải thị giác cho bảng dữ liệu nhiều hàng.
- `sort_action="native"` cho phép người dùng sort theo bất kỳ cột nào — tương tác tốt (Chương 8).

**Hạn chế:**
- Bảng thuần text — chưa được chuyển sang Highlight Table với Color Saturation cho cột championship_count như Chương 4 đề xuất.
- Không có Sparkline hay Micro-chart trong bảng như gợi ý trong Chương 3.
- `page_size=15` — tốt, nhưng cần "No Data Handling" rõ ràng khi filter trả về rỗng.

| Thay đổi đề xuất | Cách thực hiện | Chương cơ sở | Ưu tiên |
|---|---|---|---|
| Thêm `style_data_conditional` dùng gradient màu cho `championship_count` (0 = trắng, 5 = vàng đậm) | Dùng `filter_query` với ranges | Chương 4 | P2 |
| Thêm cột tỷ lệ `title_rate = championships/appearances` làm cột mới | Tính trong `team_summary` aggregation | Chương 2 | P2 |

---

### 5.8 Scatter Plot Rank Gap vs Goal Diff — `upsets-scatter-plot` (`pages/upsets.py`)

**Vai trò hiện tại:** Scatter plot với X = rank_gap (Q-Interval), Y = home_goal_diff (Q-Interval), màu = is_upset (Nominal). Là "Hero Chart" của trang Upsets.

**Bằng chứng trong code:** Hàm `_scatter_figure()` (dòng 257–286). Upset points: `opacity=0.9`, non-upset: `opacity=0.45`. Có `add_hline(y=0)` và `add_vline(x=0)`.

**Điểm mạnh:**
- Position X-Y cho hai biến Q-Q — kênh tốt nhất theo Mackinlay (Chương 2, 3, 4).
- Reference lines y=0 và x=0 giúp người xem phân chia quadrant — đúng "Chart Context" (Chương 6).
- Opacity thấp (0.45) cho non-upset và cao (0.9) cho upset — kỹ thuật "Muted Gray" chính xác (Chương 1, 3).
- clickData callback cho Detail Panel — Detail-on-demand tốt (Chương 8).
- customdata đầy đủ: date, tournament, teams, ranks, scores.

**Hạn chế:**
- Khi bộ dữ liệu đầy đủ (23,921 trận), các điểm chồng lấp nghiêm trọng — thiếu `opacity` tổng thể hoặc Jittering (Chương 6).
- Màu is_upset=True = `COLORS["accent_3"]` (đỏ `#c44536`) — cần kiểm tra CVD-safe với màu is_upset=False = `"#94a3b8"` (xám). Cặp đỏ-xám ổn hơn đỏ-xanh nhưng vẫn nên dùng Orange-Blue (Chương 8, 9).
- Legend chỉ hiển thị "True"/"False" — không rõ nghĩa mà không đọc tiêu đề.
- Tiêu đề "Rank Gap vs Goal Difference" là kỹ thuật hoàn toàn.

| Thay đổi đề xuất | Cách thực hiện | Chương cơ sở | Ưu tiên |
|---|---|---|---|
| Tiêu đề ngắn chuẩn: **"Chênh lệch hạng FIFA vs chênh lệch bàn thắng"** — insight tự hiện qua màu cam (upset) nổi bật | `title=...` | Chương 6 | P0 |
| Đổi màu upset sang Orange (`#f97316`) thay vì đỏ — CVD-safe hơn | `COLOR_UPSET = "#f97316"` trong `upsets.py` | Chương 6, 8, 9 | P0 |
| Đổi tên trace legend: "Upset (Đội yếu thắng)" / "Normal" | `fig.for_each_trace(lambda t: t.update(name=...))` | Chương 3 | P1 |
| Giảm `marker.size` xuống 5 và thêm `opacity=0.3` global cho toàn scatter khi dataset lớn | `fig.update_traces(marker={"size":5, "opacity":0.3})` rồi override upset | Chương 6 | P1 |
| Thêm annotation vùng quadrant: "Đội thấp rank thắng lớn" tại góc phải-dưới | `fig.add_annotation(x=max_rank_gap*0.8, y=min_diff*0.5, ...)` | Chương 9 | P2 |

---

### 5.9 Top 5 Upsets Bar Chart — `upsets-bar-chart` (`pages/upsets.py`)

**Vai trò hiện tại:** Horizontal bar chart top 5 upset có upset_rank_gap lớn nhất, text label bên trong bar.

**Bằng chứng trong code:** Hàm `_top_upsets_figure()` (dòng 289–318). `insidetextanchor="start"`, white text, `showticklabels=False` cho Y axis.

**Điểm mạnh:**
- Ẩn Y axis label vì text đã được nhúng trong bar — tránh cognitive switching (Chương 3).
- `categoryorder="total ascending"` đảm bảo bar lớn nhất ở trên.

**Hạn chế:**
- Chỉ hiển thị top 5 — hạn chế discovery. Không có tùy chọn xem top 10.
- Text "match_short_label" dài, có thể bị cắt khi bar ngắn.
- Không có so sánh giữa rank gap của upset với rank gap trung bình của toàn bộ dataset.

| Thay đổi đề xuất | Cách thực hiện | Chương cơ sở | Ưu tiên |
|---|---|---|---|
| Thêm dropdown chọn N (Top 5/10/20) | Thêm `dcc.Dropdown` cho số lượng hiển thị | Chương 8 | P2 |
| Thêm đường tham chiếu "median rank gap" làm vline | `fig.add_vline(x=median_gap, ...)` | Chương 4 | P2 |
| Tiêu đề ngắn chuẩn: **"Top 5 upset lớn nhất theo chênh lệch hạng"** | `title=...` | Chương 6 | P0 |

---

### 5.10 Neutral Location Stacked Bar — `upsets-stacked-bar` (`pages/upsets.py`)

**Vai trò hiện tại:** Stacked bar theo location type (Home/Away vs Neutral), màu = match_result (Home Win/Away Win/Draw), text = percentage.

**Bằng chứng trong code:** Hàm `_neutral_result_figure()` (dòng 321–366). `COLOR_HOME = COLORS["accent"]` (teal), `COLOR_AWAY = COLORS["accent_3"]` (đỏ), `COLOR_DRAW = "#cbd5e1"` (xám nhạt).

**Điểm mạnh:**
- Percent stacking (100%) tốt cho so sánh tỷ lệ (Chương 4).
- Text label trong bar với percentage rõ ràng — tránh đọc legend.
- Annotation tổng số trận phía trên mỗi cột.

**Hạn chế:**
- `COLOR_HOME = teal` và `COLOR_AWAY = red` — cặp màu này không phân biệt rõ cho người mù màu đỏ-xanh nếu context thay đổi (Chương 6, 8, 9).
- Chỉ có 2 cột (Home/Away và Neutral) — đơn giản nhưng thiếu insight chiều sâu.
- Tiêu đề "Result by Neutral Location" không kể chuyện.

| Thay đổi đề xuất | Cách thực hiện | Chương cơ sở | Ưu tiên |
|---|---|---|---|
| Đổi `COLOR_HOME` sang Blue (`#1d4ed8`), `COLOR_AWAY` sang Orange (`#f97316`) — CVD-safe | `COLOR_HOME = "#1d4ed8"`, `COLOR_AWAY = "#f97316"` | Chương 6 | P0 |
| Tiêu đề ngắn chuẩn: **"Kết quả trận theo loại địa điểm thi đấu"** — insight tự hiện khi người xem so sánh 2 cột | `title=...` | Chương 6 | P1 |
| **Annotation** chênh lệch % thắng của home giữa 2 cột → người xem thấy ngay lợi thế giảm bao nhiêu | `fig.add_annotation()` với text "Thắng sân nhà giảm X%" | Chương 3, 9 | P1 |

---

### 5.11 Goals For/Against Bar Charts — `tournament-goals-for-chart`, `tournament-goals-against-chart` (`pages/tournament.py`)

**Vai trò hiện tại:** Hai horizontal bar chart song song: bàn thắng ghi được (Goals For) và bàn thắng bị thủng lưới (Goals Against), màu theo position_group.

**Bằng chứng trong code:** `fig_gf = px.bar(gf_df, x="Goals For", y="Label", orientation="h", color="position_group", color_discrete_map=POS_COLORS, ...)` (dòng 322–335). `POS_COLORS = {"Champion": COLORS["accent_2"], "Top 4": COLORS["accent"], "Top 8": COLORS["success"], "Other": COLORS["muted"]}`.

**Điểm mạnh:**
- Màu theo `position_group` giúp nhận diện ngay Champion và top 4 — preattentive attribute tốt.
- Dùng short label (3 ký tự: ARG, FRA, MAR) từ `TEAM_LABEL` dict — tiết kiệm không gian, dễ đọc.
- Dynamic height: `height=max(360, len(gf_df) * 22)` — tự điều chỉnh theo số đội, tránh overlap.

**Hạn chế:**
- `COLORS["success"]` = `#2f855a` (xanh lá) và `COLORS["accent_3"]` = `#c44536` (đỏ) xuất hiện cùng nhau trong `POS_COLORS` — **vi phạm CVD nghiêm trọng** (Chương 6, 8, 9). Cặp xanh lá-đỏ là cặp màu tệ nhất cho người mù màu Protanopia/Deuteranopia.
- Goals Against chart sắp xếp `ascending=False` (nhiều thủng lưới nhất ở trên) — không nhất quán với Goals For (`ascending=True`, ít GF ở trên). Người xem bị mất phương hướng khi đọc song song.
- Tiêu đề chỉ là "Goals Scored — {year}" và "Goals Conceded — {year}".

| Thay đổi đề xuất | Cách thực hiện | Chương cơ sở | Ưu tiên |
|---|---|---|---|
| **Sửa CVD ngay**: Đổi `POS_COLORS["Top 8"]` từ `success (#2f855a)` sang Purple (`#7c3aed`) | `POS_COLORS = {"Champion": "#d98324", "Top 4": "#007c89", "Top 8": "#7c3aed", "Other": "#94a3b8"}` | Chương 6 | **P0 Khẩn cấp** |
| Đồng nhất thứ tự sắp xếp Goals Against thành `ascending=True` — ít GA ở trên cùng → người xem thấy ngay đội phòng ngự tốt nhất | `ga_df.sort_values("Goals Against", ascending=True)` | Chương 3 | P1 |
| Tiêu đề ngắn chuẩn: **"Bàn ghi được — {year}"** và **"Bàn thủng lưới — {year}"** | `title=f"Bàn ghi được — {year}"` | Chương 6 | P0 |
| **Màu sắc position_group tự nói insight**: Champion (amber) nổi bật nhất → người xem thấy ngay ARG ở đầu bảng mà không cần đọc text | Đảm bảo POS_COLORS contrast đủ mạnh | Chương 3 | P1 |

---

### 5.12 Scatter Goals For vs Goals Against — `tournament-scatter-chart` (`pages/tournament.py`)

**Vai trò hiện tại:** Scatter với X=Goals For, Y=Goals Against, color=position_group, size=Points, text labels cho top 8.

**Bằng chứng trong code:** `fig_sc = px.scatter(sc_df, x="Goals For", y="Goals Against", color="position_group", color_discrete_map=POS_COLORS, text="DisplayLabel", size="Points", size_max=28, ...)` (dòng 372–391). `yaxis_autorange="reversed"` để đảo ngược trục Y (ít GA ở trên = phòng ngự tốt).

**Điểm mạnh:**
- `yaxis_autorange="reversed"` là thiết kế thông minh — Champion nằm ở góc phải-trên (nhiều GF, ít GA).
- `size=Points` tạo Bubble chart — Points là Q-Ratio bổ sung thêm chiều thứ 3.
- `DisplayLabel` chỉ hiển thị nhãn cho Top 8 — tránh over-clutter.

**Hạn chế:**
- **CVD issue** như đã nêu ở 5.11: màu xanh lá (Top 8) và đỏ (sẽ không có nhưng nếu thêm) cùng tồn tại.
- Size=Points mã hóa Q bằng Area (kênh thứ 5 Mackinlay) — khó ước lượng chính xác. Nên dùng hover tooltip thay vì mã hóa thị giác.
- Thiếu đường tham chiếu diagonal (GF = GA) để phân biệt "tấn công > phòng ngự" và ngược lại. Đây là **đường tham chiếu quan trọng nhất** trong biểu đồ này (Chương 6).
- Tiêu đề "Goals Scored vs Goals Conceded — {year}" là kỹ thuật.

| Thay đổi đề xuất | Cách thực hiện | Chương cơ sở | Ưu tiên |
|---|---|---|---|
| **Đường diagonal GF=GA** (nét đứt, màu muted) → người xem tự thấy đội nào thiên tấn công / thiên phòng ngự mà không cần đọc label | `fig.add_shape(type="line", x0=0, y0=0, x1=max_val, y1=max_val, line_dash="dot")` | Chương 6 | **P1 Quan trọng** |
| **Annotation vùng** góc phải-trên (nhỏ, màu muted): "Nhiều GF, ít GA" → định hướng đọc chart, không cần title dài | `fig.add_annotation(text="Nhiều GF, ít GA", showarrow=False, font_size=10)` | Chương 3 | P1 |
| Tiêu đề ngắn chuẩn: **"Bàn ghi vs bàn thủng — {year}"** | `title=...` | Chương 6 | P0 |
| **Sửa CVD**: Đổi POS_COLORS như đã đề xuất ở 5.11 | Xem 5.11 | Chương 6 | P0 |

---

### 5.13 Biểu đồ KHÔNG tìm thấy — Choropleth/Symbol Map

**Trạng thái:** Not found — không được triển khai trong bất kỳ trang nào.

**Đánh giá theo Chương 7:** Doc7.md đề xuất mạnh mẽ "bản đồ là thành phần thiết yếu để khẳng định luận điểm về Địa lý của thành công" và "Sự tương phản Gay gắt giữa các vùng trắng danh hiệu mênh mông vs đậm đặc màu sắc tại Europe và South America". Tuy nhiên, đây không phải yêu cầu bắt buộc vì Chương 5 cũng cảnh báo về over-complexity.

**Khuyến nghị:** Thêm Choropleth Map đơn giản vào trang Dominance (panel bổ sung) thể hiện số lần vô địch theo màu sắc trên bản đồ thế giới. Dùng bảng màu Sequential (YlOrRd) — Blue cuối cùng nếu cần CVD. Đây là **P3 — Bonus nếu còn thời gian**.

---

### 5.14 Biểu đồ KHÔNG tìm thấy — Small Multiples / Trellis Plots

**Trạng thái:** Not found — Chương 3, 4, 9 đề xuất nhưng chưa triển khai.

**Khuyến nghị:** Xem xét thêm Small Multiples cho Dominance page: mỗi ô là một châu lục, X=Year, Y=số lần top 4. Hiện tại stacked bar đang cố gắng thể hiện thông tin này nhưng khó đọc khi có nhiều châu lục. Đây là **P3 — Bonus**.

---

## 6. Kế hoạch Áp dụng theo Chương

| Chương | Kỹ thuật được áp dụng (Verified) | Cách áp dụng hiện tại | Khoảng trống (Gap) | Đề xuất bổ sung |
|---|---|---|---|---|
| **Chương 1**: Overview — Why Visualization | Ưu tiên Position và Length cho Q; tránh Pie chart; sắp xếp bar chart; màu xám cho background | Bar charts sắp xếp đúng; không có Pie chart; màu accent chỉ dùng cho điểm nhấn | Tiêu đề thiếu insight; thiếu Zero-baseline check cho mọi bar chart | Kiểm tra tất cả bar charts bắt đầu Y=0; thêm "Action Titles" |
| **Chương 2**: Visual Models & Encoding | N→Hue, Q→Position/Length; tránh Shape cho Q; Text Label cho Tooltip | Continent→Hue trong stacked bars; Q→Length trong bar charts; Text Labels trong tooltips | Size cho số đội trong champion timeline vi phạm ranking; Bubble size cho Points không cần thiết | Bỏ Size encoding không quan trọng; dùng hover tooltip thay thế |
| **Chương 3**: Graphical Perception | Preattentive attributes; Data-Ink Ratio; Direct Labeling; Pop-out effect; 5-7 màu max | Opacity thấp cho non-upset (preattentive ok); Direct Label trong upset bar chart; zebra striping | Thiếu Pop-out cho Brazil/Morocco; Legend "True/False" không direct label | Thêm annotation trực tiếp; đổi legend sang tên mô tả |
| **Chương 4**: Multi-dimensional Data | Small Multiples; Scatter cho Q-Q; Stacked Bar cho Proportions; Annotated Line Chart | Scatter plot tốt; Stacked bar cho continent; subplots chia sẻ trục X | Không có Small Multiples độc lập cho châu lục; Annotated Line Chart chưa có | Thêm trellis view cho Dominance (P3); thêm annotation sự kiện lịch sử |
| **Chương 5**: Graph Visualization | Không áp dụng Network Graph (quyết định đúng) | Không có network graph trong dashboard | Không có gap — quyết định đúng theo lý thuyết "Position > Connection" | Không cần thay đổi; ghi chú trong báo cáo là quyết định có cơ sở |
| **Chương 6**: Figure Design Principles | Proportional Ink; Zero-baseline; Opacity/Jittering; CVD-safe colors; Narrative Titles | Zero-baseline trong bar charts; Opacity trong scatter; nền trắng sạch | **CVD: màu xanh lá + đỏ trong POS_COLORS là lỗi nghiêm trọng**; thiếu diagonal line trong scatter tournament | Sửa POS_COLORS ngay; thêm reference line |
| **Chương 7**: Map Visualization | Không triển khai (Not found) | Không có bản đồ | Thiếu hoàn toàn chiều không gian địa lý cho storyline | Thêm Choropleth Map đơn giản (P3 Bonus) |
| **Chương 8**: Interactive Visualization | Filtering; clickData; Detail Panel; Empty state handling; Dropdown; RangeSlider | click detail panel trong Upsets; dynamic dropdown options; empty_figure(); suppress_callback_exceptions | Thiếu "Reset All Filters" button; tooltip chưa đủ "So What?" context; thiếu cross-chart highlighting | Thêm reset button; nâng cấp tooltip với comparison context |
| **Chương 9**: Storytelling | Narrative arc; Action Titles; Insight Cards; Strategic Annotations; CVD bắt buộc | Câu chuyện 4 act trong work plan đã được triển khai thành 4 trang; 2022 insight panel tốt | **Tất cả tiêu đề biểu đồ thiếu storytelling**; không có insight cards nối act 1→2→3→4; thiếu annotations | Sửa 100% tiêu đề biểu đồ; thêm insight text block đầu mỗi trang |

---

## 7. Cấu trúc Dashboard Cải tiến Đề xuất

| Trang | Hero Chart (đề xuất) | Supporting Charts | Insight Text Block | Bộ lọc |
|---|---|---|---|---|
| **Overview** "Kỷ nguyên Bành trướng" | Annotated Line Chart (Teams/Matches/Goals) với annotations 1930, 1954, 1990, 1998 | Avg Goals line chart có min/max markers; Champion Timeline với legend host-wins | Block: "Sau 92 năm, World Cup tăng từ 13 lên 32 đội — nhưng ai nắm cúp vàng?" | Year range, Host, Champion |
| **Dominance** "Bức tường Pha lê" | Horizontal Bar Chart số lần vô địch, màu theo châu lục, highlight Brazil | Stacked Bar top 4 theo continent có vrect giai đoạn; Ranked Table với gradient | Block: "Chỉ 9 đội chia nhau 22 chức vô địch. Châu Âu + Nam Mỹ = 100% danh hiệu." | Year range, Team, Continent, Position group |
| **Upsets** "Những Cú Sốc Định Mệnh" | Scatter Rank Gap vs Goal Diff (màu CVD-safe Orange/Gray) với quadrant annotations | Top 5 Upsets bar chart; Neutral Location stacked bar (CVD-safe Blue/Orange) | Block: "Bóng đá có 1 luật bất thành văn: Số liệu không thể đoán được mọi thứ." | Year range, Tournament, Team, Continent, Match type |
| **Tournament Detail** "Bằng chứng từ 2022" | Scatter GF vs GA với diagonal reference line và position_group colors (CVD-safe) | Goals For / Goals Against bar charts đồng nhất thứ tự sắp xếp; Full standings table | 2022 insight panel (đã có) — mở rộng cho năm khác | Year dropdown |

---

## 8. Hướng dẫn Phong cách Trực quan

### 8.1 Bảng màu CVD-Safe (Cần cập nhật ngay)

Màu hiện tại trong `src/theme.py` cần thay thế `POS_COLORS` trong `tournament.py` và `dominance.py`:

| Vai trò | Màu hiện tại | Màu đề xuất | Lý do |
|---|---|---|---|
| Champion | `#d98324` (amber) | Giữ nguyên | Hợp lý, phân biệt tốt |
| Top 4 | `#007c89` (teal) | Giữ nguyên | Tốt |
| **Top 8** | **`#2f855a` (xanh lá)** | **`#7c3aed` (purple)** | **Xanh lá + đỏ = CVD fail** |
| Other | `#64727d` (xám) | Giữ nguyên | Tốt — background color |
| Upset color | `#c44536` (đỏ) | `#f97316` (orange) | Blue-Orange safer than Red |
| Home Win | `#007c89` (teal/blue) | `#1d4ed8` (blue rõ hơn) | Phân biệt rõ hơn với Away |
| Away Win | `#c44536` (đỏ) | `#f97316` (orange) | CVD-safe |

### 8.2 Typography

Hệ thống font Inter (đã có trong `styles.css` và theme Plotly) là hợp lý. Thêm phân cấp:

- **KPI Numbers:** `font-size: 30px`, `font-weight: 820` — đã có trong `.kpi-value`
- **Chart Titles:** `font-size: 18px`, `font-weight: 700` — đã có trong theme
- **Insight Cards:** `font-size: 14px`, `line-height: 1.6` — cần thêm component mới
- **Axis Labels:** `font-size: 12px`, `color: #64727d` — đã có trong theme

### 8.3 Nguyên tắc Annotation

Mọi annotation phải:
1. Dùng `arrowhead=2` hoặc `arrowhead=0` (không arrow) tùy ngữ cảnh
2. Font 11-12px để không cạnh tranh với data
3. Màu `COLORS["muted"]` (`#64727d`) cho annotation ngữ cảnh
4. Màu `COLORS["accent_3"]` hoặc `COLORS["warning"]` cho annotation cảnh báo/highlight
5. Đặt `xanchor="left"` để tránh bị cắt ở cạnh biểu đồ

### 8.4 Insight Card Component

Cần thêm component mới vào `src/components.py`:

```python
def insight_card(text: str, accent_color: str = None) -> html.Div:
    """Insight text block cho đầu mỗi trang, giải thích 'So What?'"""
    ...
```

Style: nền `surface_alt` (`#eef4f5`), border-left 3px solid accent, padding 16px, font-size 14px.

---

## 9. Kế hoạch Thiết kế Tương tác

| Tương tác | Trang | Trạng thái hiện tại | Đề xuất cải tiến | Chương cơ sở |
|---|---|---|---|---|
| Year Range Slider | Overview, Dominance, Upsets | Implemented, hoạt động tốt | Thêm tooltip "Kỳ đầu tiên" / "Kỳ gần nhất" | Chương 8 |
| Dropdown lọc Host/Champion | Overview | Implemented | Thêm placeholder text có insight: "Tất cả 8 nhà vô địch" | Chương 8 |
| Click-to-detail trận đấu | Upsets | Implemented — scatter + bar | Nâng cấp detail panel: thêm tên giải đấu, vòng đấu, ý nghĩa upset | Chương 8 |
| Cross-chart highlighting | Tất cả | Chưa có | Khi click một đội trong bar chart → highlight đội đó trong scatter plot cùng trang | Chương 8 |
| Year Dropdown Tournament | Tournament | Implemented | Thêm quick-link "Xem 2022 (Mặc định)" | Chương 8 |
| Reset All Filters | Tất cả | Chưa có | Thêm nút "Đặt lại bộ lọc" dùng `PreventUpdate` khi đã mặc định | Chương 8 |
| Hover Tooltip nâng cấp | Overview | Chỉ hiển thị số liệu đơn | Thêm ngữ cảnh: "Cao hơn X% so với trung bình lịch sử" | Chương 2, 8 |
| Animated Race Chart | Dominance | Không có | Bonus: animated bar chart đua số lần vô địch theo năm | Chương 8 |
| No-data Warning | Tất cả | `empty_figure()` đã có | Thêm text hướng dẫn reset filter | Chương 8 |

---

## 10. Kế hoạch Cải thiện Storytelling

| Act | Trang | Thông điệp cần truyền tải | Tiêu đề biểu đồ hiện tại | Tiêu đề đề xuất | Insight Card đề xuất |
|---|---|---|---|---|---|
| Act 1: Mở rộng | Overview | World Cup tăng từ 13→32 đội, nhiều trận hơn, nhiều bàn hơn | "Quy mô World Cup theo năm" | **Annotation tại 1998** trên chart: "32 đội" với mũi tên; **highlight điểm bước nhảy** → người xem thấy ngay mà không đọc title | Insight card trang: "Sau 92 năm, World Cup tăng từ 13 lên 32 đội." |
| Act 2: Thống trị | Dominance | Chỉ EU + SA thống trị Top 4, chỉ 9 đội từng vô địch | "Số lần vô địch theo đội" | **Highlight Brazil** màu amber đậm + annotation "5 lần" trên bar → người xem thấy ngay ai nhiều nhất; màu stacked bar tự nói EU/SA chiếm ưu thế | Insight card trang: "Chỉ 9 đội chia nhau 22 chức vô địch." |
| Act 3: Bất ngờ | Upsets | Rank cao không đảm bảo thắng — nhiều upset ở cấp trận | "Chênh lệch hạng FIFA vs chênh lệch bàn thắng" | **Màu cam (upset)** nổi bật trên nền xám → người xem thấy ngay có rất nhiều điểm cam phân tán ở mọi vùng rank gap | Insight card trang: "23,921 trận — đội yếu hơn vẫn thắng thường xuyên hơn bạn nghĩ." |
| Act 4: Case study | Tournament | Argentina + France = Elite; Morocco = ngoại lệ lịch sử | "Bàn ghi được — 2022" | **Màu amber (Champion)** của ARG nổi bật nhất; **đường GF=GA** tự phân vùng tấn công/phòng ngự; **top 4 cards** tự kể câu chuyện top 4 | 2022 insight panel đã có |
| Kết | Tất cả | World Cup 48 đội (tương lai) | Không có | Không cần — mạch truyện đã đủ qua 4 trang | Closing note tùy chọn |

---

## 11. Kế hoạch Hành động Ưu tiên

### 11.1 Phải sửa trước khi nộp

Các mục này ảnh hưởng đến tính đúng đắn kỹ thuật, accessibility, hoặc storytelling cốt lõi:

1. **[KHẨN CẤP — CVD] Sửa POS_COLORS trong `tournament.py`** — Đổi `"Top 8": COLORS["success"]` (`#2f855a` xanh lá) sang `"Top 8": "#7c3aed"` (purple). Ảnh hưởng: `tournament-goals-for-chart`, `tournament-goals-against-chart`, `tournament-scatter-chart`. File: `pages/tournament.py` dòng 61-66.

2. **[KHẨN CẤP — CVD] Sửa màu Upset trong `upsets.py`** — Đổi `COLOR_UPSET = COLORS["accent_3"]` (`#c44536`) sang `COLOR_UPSET = "#f97316"` (orange). File: `pages/upsets.py` dòng 12.

3. **[KHẨN CẤP — CVD] Sửa màu trong neutral_result chart** — Đổi `COLOR_HOME = COLORS["accent"]` và `COLOR_AWAY = COLORS["accent_3"]` sang Blue/Orange. File: `pages/upsets.py` dòng 14-16.

4. **[P0] Chuẩn hóa tiêu đề biểu đồ** — Ngắn gọn, mô tả đúng nội dung, không cần chứa insight. **Insight phải tự hiện ra qua design**: annotation, highlight màu, reference line, thứ tự sắp xếp. Ảnh hưởng: tất cả hàm `_scale_figure`, `_avg_goals_figure`, `_champion_timeline_figure`, `update_dominance`, `_scatter_figure`, `_top_upsets_figure`, `_neutral_result_figure`, `update_all` trong 4 page files.

5. **[P0] Thêm Insight Card text block đầu mỗi trang** — Thêm `html.Div(className="insight-card", ...)` vào layout của Overview, Dominance, Upsets. CSS style mới trong `assets/styles.css`.

6. **[P1] Thêm đường diagonal tham chiếu GF=GA vào `tournament-scatter-chart`** — Thêm `fig.add_shape(type="line", ...)` trong hàm scatter của `tournament.py`.

7. **[P1] Đồng nhất thứ tự sắp xếp** Goals Against chart — Đổi `ascending=False` thành `ascending=True` (ít GA ở trên = phòng ngự tốt hơn) trong `tournament.py` dòng khoảng 340.

### 11.2 Nên cải thiện nếu còn thời gian

8. **[P1] Thêm Strategic Annotations trên Overview line charts** — Annotation tại 1954 (bàn thắng peak), 1990 (thấp nhất), 1998 (32 đội). File: `pages/overview.py`, hàm `_scale_figure()` và `_avg_goals_figure()`.

9. **[P1] Nâng cấp legend scatter upsets** — Đổi tên trace từ "True"/"False" thành "Upset (Đội yếu thắng)"/"Kết quả thông thường". File: `pages/upsets.py`, hàm `_scatter_figure()`.

10. **[P1] Bỏ mã hóa Size trong champion timeline** — Dùng fixed size thay vì `marker_sizes` từ số đội. File: `pages/overview.py`, hàm `_champion_timeline_figure()`.

11. **[P1] Thêm vrect giai đoạn lịch sử vào stacked bar continent** — Phân tách 4 giai đoạn thể thức (1930-54, 1958-82, 1986-94, 1998-nay). File: `pages/dominance.py`.

12. **[P2] Thêm tô màu châu lục cho champion bar chart** — Thêm continent info vào champion_counts và dùng `color="continent"`. File: `pages/dominance.py`.

13. **[P2] Nâng cấp Tooltip Overview** — Thêm context "% thay đổi so với kỳ trước" trong hovertemplate. File: `pages/overview.py`.

14. **[P2] Thêm nút "Đặt lại bộ lọc"** — Thêm `html.Button("Đặt lại", id="overview-reset")` và callback tương ứng. Tất cả 4 trang.

### 11.3 Tùy chọn / Bonus

15. **[P3] Choropleth Map trang Dominance** — Thêm tab "Bản đồ" vào Dominance page dùng `px.choropleth` với `color=championship_count`, bảng màu YlOrBr.

16. **[P3] Small Multiples trang Dominance** — Thêm faceted view bằng `px.bar(..., facet_col="continent")` để so sánh 6 châu lục song song.

17. **[P3] Animated Race Chart** — `px.bar(..., animation_frame="Year", ...)` cho champion count accumulation qua các năm.

18. **[P3] Index Chart trong Overview** — Thêm toggle "Xem tương đối" để normalize tất cả series về base=100 tại năm 1930.

19. **[P3] Closing Note block** — Thêm text block về World Cup 2026 (48 đội) ở cuối trang Overview: "Với 48 đội từ 2026, bức tường pha lê có vỡ không?"

---

## 12. Hỗ trợ Viết Báo cáo

### Outline theo từng Chương

**Chương 1 — Tổng quan trực quan hóa dữ liệu:**
- Giải thích tại sao dự án chọn Bar Chart (Length/Position) thay vì Pie Chart (Angle) cho số lần vô địch
- Nêu nguyên tắc sắp xếp có ý nghĩa (sorted bar charts) trong `dominance-champion-bar`
- Đề cập Zero-baseline của tất cả bar charts trong codebase
- Nêu màu xám (muted) cho background data, màu accent cho highlight

**Chương 2 — Visual Models & Encoding:**
- Bảng ánh xạ N-O-Q: Champion (N)→Hue, Goals (Q)→Length, Year (Interval)→Position
- Giải thích tại sao `is_upset (N)` được mã hóa bằng Color Hue (Orange vs Gray)
- Phê bình việc dùng Size (Area) cho số đội trong champion timeline
- Nêu lý do không dùng Angle (Pie chart) cho bất kỳ biến Q nào

**Chương 3 — Graphical Perception:**
- Preattentive: Morocco highlight màu xanh lá trong 2022 insight panel
- Data-Ink: nền trắng sạch, grid color nhẹ (`#e8eef2`), không có chart junk
- Pop-out effect: đề xuất annotation Brazil 5 lần vô địch
- Giới hạn màu: `CHART_COLORS` trong theme có 7 màu (đúng ngưỡng 5-7)

**Chương 4 — Multi-dimensional Data:**
- Scatter plot (Q × Q): rank_gap × home_goal_diff trong upsets page
- Scatter plot (Q × Q với 3 dimension): GF × GA × position_group trong tournament
- Stacked bar (Continent × Year × Count): dominance-top4-by-continent
- 3 subplots chia sẻ trục X trong scale chart: ví dụ Small Multiples đơn giản

**Chương 5 — Graph Visualization:**
- Giải thích quyết định KHÔNG dùng Network Graph: "Với hàng trăm trận đấu, hiện tượng hairball không thể tránh" (trích doc5.md)
- Nêu rằng Position > Connection trong ranking Mackinlay cho mục tiêu phân tích Ranking và Trend
- Dashboard chọn Bar Chart và Line Chart vì "người dùng so sánh nhanh hơn 10-20 lần qua độ dài thanh"

**Chương 6 — Figure Design Principles:**
- Proportional Ink: tất cả bar charts có Y-axis bắt đầu từ 0 (xác minh trong code)
- CVD: vấn đề POS_COLORS màu xanh lá + đỏ cần sửa; đề xuất Blue-Orange
- Narrative Titles: biểu đồ tournament-scatter-chart nên đổi thành "Champion nằm ở góc phải-trên"
- Overlapping: opacity 0.45 cho non-upset scatter points (Jittering gián tiếp)

**Chương 7 — Map Visualization:**
- Thừa nhận không triển khai map vì phạm vi thời gian
- Giải thích vị trí lý tưởng: Choropleth trong trang Dominance, Sequential color cho wins
- Nêu rủi ro: Uruguay (2 titles, diện tích nhỏ) bị che mờ bởi Russia/Brazil (diện tích lớn, ít/nhiều titles hơn)
- Kết luận: Map là "Biểu đồ bối cảnh" hỗ trợ Bar Chart, không thay thế

**Chương 8 — Interactive Visualization:**
- Filtering: 4 trang có Year Range Slider, Team/Continent/Tournament dropdowns
- Detail-on-demand: clickData callback trong upsets page (scatter + bar → detail panel)
- Empty state: `empty_figure()` xử lý khi filter trả về rỗng
- Cross-page navigation: `dcc.Location` + routing trong `app.py`
- Thiếu: Reset All button, Cross-chart highlighting, Latency check

**Chương 9 — Storytelling:**
- Nêu 4 Act narrative: Mở rộng → Thống trị → Bất ngờ → Case Study 2022
- Wording transformation: "Tournament Scale" → "Kỷ nguyên Bành trướng" (từ doc9.md)
- Strategic Annotations đề xuất: 1954, 1990, 1998 trên line chart
- 2022 Insight Panel trong tournament.py là ví dụ tốt về Release của narrative arc
- Đề xuất "Closing Note" về World Cup 48 đội 2026

---

## 13. Checklist Cuối cùng

### Checklist Kỹ thuật (Trước khi nộp)

- [ ] **CVD-FIX**: `POS_COLORS["Top 8"]` đã đổi từ xanh lá sang purple
- [ ] **CVD-FIX**: `COLOR_UPSET` đã đổi từ đỏ sang orange
- [ ] **CVD-FIX**: `COLOR_HOME`/`COLOR_AWAY` trong neutral chart đã là Blue/Orange
- [ ] **TITLES**: Tất cả biểu đồ có Action Title (không phải "Chart Title")
- [ ] **ZERO-BASELINE**: Tất cả bar charts xác nhận Y-axis bắt đầu từ 0
- [ ] **DIAGONAL LINE**: Scatter tournament-scatter-chart có đường tham chiếu GF=GA
- [ ] **SORTING**: Goals Against chart sắp xếp ascending (ít GA ở trên)
- [ ] **LEGEND**: Scatter upsets legend hiển thị "Upset (Đội yếu thắng)" không phải "True"
- [ ] **EMPTY STATE**: Tất cả charts có empty_figure() khi filter trả về rỗng
- [ ] **NO CRASH**: Chạy `python app.py` không lỗi, chuyển 4 trang không callback error

### Checklist Storytelling (Trước khi nộp)

- [ ] **TITLE CHUẨN**: Tất cả tiêu đề ngắn gọn, mô tả đúng nội dung — không có title dài quá 8 từ
- [ ] **INSIGHT QUA DESIGN**: Người xem nhìn vào biểu đồ phải thấy insight mà **không cần đọc title hay insight card**
- [ ] **ANNOTATION**: Ít nhất 1 annotation lịch sử trên line charts (1998 hoặc 1954) — thay title dài
- [ ] **HIGHLIGHT**: Ít nhất 1 chart có element nổi bật hơn phần còn lại (màu, size, annotation)
- [ ] **INSIGHT CARDS**: Mỗi trang có 1 câu ngắn tóm tắt context — **không phải giải thích chart**
- [ ] **2022 PANEL**: Insight panel hiển thị đúng khi chọn năm 2022
- [ ] **NARRATIVE ARC**: Người xem đọc 4 trang theo thứ tự và tự hiểu câu chuyện từ visual

### Checklist Accessibility

- [ ] **CVD**: Không có cặp màu đỏ-xanh trong bất kỳ biểu đồ nào
- [ ] **CONTRAST**: Màu text trên nền có đủ contrast ratio (>4.5:1)
- [ ] **SKIP LINK**: `html.A("Skip to content", href="#page-content")` đã có trong `app.py`
- [ ] **RESPONSIVE**: Dashboard hiển thị đúng ở breakpoint 1120px và 720px

### Checklist Báo cáo

- [ ] Mỗi chương có 1 đoạn áp dụng vào dashboard (theo outline Mục 12)
- [ ] Số liệu thực tế khớp với data: 22 kỳ WC, 9 đội vô địch, Brazil 5 lần, EU 12 titles
- [ ] Phê bình self-critical: Nêu được 2-3 hạn chế của dashboard và lý do chưa sửa
- [ ] Screenshot được chụp: Overview, Dominance, Upsets, Tournament 2022

---

*Tài liệu này được soạn thảo dựa trên phân tích chi tiết 9 chương tài liệu khóa học (doc1.md–doc9.md) và toàn bộ source code của dự án tại `c:\Users\Admin\Uni\Data_Visualization_Group2\DV_project\`. Mọi đề xuất đều tham chiếu đến function name, component ID, và file path cụ thể trong codebase để đảm bảo tính thực thi.*
