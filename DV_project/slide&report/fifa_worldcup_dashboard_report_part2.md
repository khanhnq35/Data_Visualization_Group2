## 5. Áp dụng kỹ thuật trực quan hóa (Technique Application)

Phần này trình bày cách nhóm áp dụng các nguyên tắc và kỹ thuật trực quan hóa dữ liệu đã học trong từng chapter vào thiết kế dashboard. Mỗi mục bao gồm: nguyên tắc lý thuyết, cách áp dụng cụ thể trong dashboard, và các ghi chú hoặc đánh đổi (trade-off) nếu có.

---

### 5.1. Chapter 1 — Mục đích trực quan hóa và lựa chọn dữ liệu

#### Nguyên tắc áp dụng

- Phân biệt giữa **exploratory analysis** (khám phá, tìm kiếm mẫu hình) và **explanatory analysis** (giải thích, truyền đạt insight đã biết).
- Lựa chọn dataset phù hợp với câu hỏi phân tích.
- Xác định rõ đối tượng sử dụng (audience) và mục tiêu truyền thông.

#### Cách áp dụng trong Dashboard

Dashboard kết hợp cả hai phương pháp phân tích. Ở khía cạnh **explanatory**, mạch kể chuyện 4 trang (Overview → Dominance → Upsets → Tournament Detail) được thiết kế theo một narrative có sẵn, dẫn dắt người xem đi qua các insight đã được nhóm xác định trước: sự mở rộng quy mô, sự tập trung quyền lực, và tính bất ngờ của bóng đá. Các KPI cards, annotation trên biểu đồ, và insight panel (World Cup 2022) đều phục vụ mục tiêu giải thích.

Ở khía cạnh **exploratory**, dashboard cung cấp hệ thống bộ lọc phong phú (year range, continent, team, tournament, position group) kèm bảng dữ liệu tương tác có thể sắp xếp và lọc, cho phép người dùng tự do khám phá dữ liệu theo hướng riêng. Tính năng click-to-detail trên scatter plot (trang Upsets) và click vào hàng bảng (trang Dominance, Tournament Detail) hỗ trợ quá trình khám phá ở mức chi tiết từng trận đấu hoặc từng đội tuyển.

Việc lựa chọn bộ dữ liệu World Cup (22 kỳ, 454 standings records) kết hợp với trận đấu quốc tế (23.921 trận) cho phép phân tích ở hai tầng: **tầng vĩ mô** (xu hướng lịch sử dài hạn) và **tầng vi mô** (cấp độ từng trận đấu). Đây là sự lựa chọn có chủ đích để trả lời đầy đủ câu hỏi trung tâm của dashboard.

---

### 5.2. Chapter 2 — Loại dữ liệu, visual marks và visual channels

#### Nguyên tắc áp dụng

- Phân loại dữ liệu: **nominal** (tên đội, giải đấu), **ordinal** (vị trí, nhóm thành tích), **quantitative** (bàn thắng, điểm, ranking).
- Chọn **visual marks** (điểm, đường, vùng) phù hợp với loại dữ liệu.
- Sử dụng **visual channels** (vị trí, chiều dài, màu sắc, kích thước, hình dạng) theo thứ tự hiệu quả.

#### Cách áp dụng trong Dashboard

**Visual marks:**

| Mark | Sử dụng tại | Loại dữ liệu |
|---|---|---|
| Điểm (point) | Scatter plot trang Upsets (rank gap vs goal diff), Bubble chart trang Tournament Detail (GF vs GA), Champion Timeline (dot plot) | Quantitative × Quantitative |
| Đường (line) | Line charts trang Overview (xu hướng teams, matches, goals theo năm) | Quantitative × Temporal |
| Thanh (bar) | Horizontal bar charts trang Dominance (champion count, total goals), Tournament Detail (GF, GA), Upsets (top 5 upsets); Stacked bar trang Dominance (Top 4 by continent), Upsets (result distribution) | Categorical × Quantitative |

**Visual channels — áp dụng theo thứ tự hiệu quả:**

- **Vị trí (position):** Là channel hiệu quả nhất, được sử dụng làm kênh chính ở tất cả biểu đồ. Trục X thường biểu diễn thời gian (year) hoặc biến so sánh (rank gap, goals for); trục Y biểu diễn giá trị đo lường (goals, goal difference, position).
- **Chiều dài (length):** Sử dụng trong tất cả bar charts để encode giá trị quantitative (số lần vô địch, tổng bàn thắng, upset rank gap). Đây là kênh phù hợp nhất cho so sánh giữa các đối tượng nominal.
- **Màu sắc — hue (color):** Dùng để phân biệt các nhóm categorical: châu lục trong stacked bar (mỗi châu lục một màu cố định qua `CONTINENT_COLORS`), `position_group` trong biểu đồ Tournament Detail (Champion/Top 4/Top 8/Other), và trạng thái upset vs normal trong scatter plot.
- **Kích thước (size):** Sử dụng trong bubble chart GF vs GA trên trang Tournament Detail, với `size="Points"` — kích thước bong bóng tỷ lệ với điểm số, thêm một chiều thông tin quantitative mà không cần trục phụ.
- **Hình dạng (shape):** Sử dụng trong Champion Timeline trên trang Overview — marker ngôi sao (★) cho kỳ nước chủ nhà vô địch, hình tròn (●) cho các kỳ khác. Đây là cách hiệu quả để encode biến boolean (`host_won`) mà không cần thêm màu sắc.

#### Ghi chú

Nhóm ưu tiên sử dụng position và length làm kênh chính vì chúng cho phép đánh giá chính xác nhất về mặt tri giác (perceptual accuracy). Color hue chỉ dùng cho biến categorical (phân nhóm), không dùng để encode giá trị quantitative — tránh vấn đề color magnitude estimation kém chính xác.

---

### 5.3. Chapter 3 — Pre-attentive processing, nguyên tắc Gestalt, và magnitude estimation

#### Nguyên tắc áp dụng

- **Pre-attentive processing:** Sử dụng các thuộc tính thị giác được bộ não xử lý tức thì (màu sắc, kích thước, hướng) để thu hút sự chú ý vào thông tin quan trọng.
- **Gestalt principles:** Proximity (gần nhau), Similarity (tương đồng), Enclosure (bao quanh), Connection (kết nối), Continuity (liên tục).
- **Magnitude estimation:** Con người đánh giá chính xác nhất qua vị trí và chiều dài; kém chính xác hơn qua diện tích và màu sắc.

#### Cách áp dụng trong Dashboard

**Pre-attentive processing:**

- Trang Dominance: Biểu đồ champion count sử dụng kỹ thuật **highlight bằng màu** — đội có nhiều danh hiệu nhất được tô màu amber nổi bật (`accent_2 = #d98324`), trong khi tất cả các đội khác dùng màu xám nhạt. Sự tương phản màu sắc này cho phép người xem lập tức nhận diện được đội dẫn đầu mà không cần đọc nhãn hoặc số liệu.
- Trang Upsets: Scatter plot sử dụng màu cam (accent) cho các điểm upset và màu xám mờ cho các trận bình thường. Sự khác biệt về **hue** kết hợp với khác biệt về **opacity** (upset points đậm hơn) tạo hiệu ứng pop-out tức thì cho các trận bất ngờ giữa hàng nghìn điểm dữ liệu.
- KPI cards trên tất cả các trang sử dụng **kích thước font lớn** (30px, font-weight 820) cho giá trị số, kết hợp viền màu trên cạnh card, tạo hiệu ứng pre-attentive giúp người xem nắm bắt các số liệu tổng quan ngay lập tức.

**Gestalt principles:**

- **Proximity (gần nhau):** KPI cards được xếp thành hàng ngang liền kề, tạo nhóm thị giác thống nhất. Biểu đồ cùng chủ đề được đặt trong cùng một `chart-grid` với khoảng cách đều nhau. Filter bar là một hàng ngang liền khối phía trên nội dung.
- **Similarity (tương đồng):** Tất cả KPI cards chia sẻ cùng kiểu dáng (white card, shadow, colored top border) tạo cảm giác chúng thuộc cùng một nhóm thông tin. Cùng bảng màu `position_group` (amber cho Champion, xám cho Runner-Up, nâu cho 3rd, xám nhạt cho 4th) được dùng nhất quán giữa trang Dominance và Tournament Detail.
- **Enclosure (bao quanh):** Mỗi biểu đồ được đặt trong một `.chart-card` với viền, border-radius và shadow, phân tách rõ ràng từng đơn vị thông tin. Detail panel trên trang Upsets dùng nền vàng nhạt kèm viền vàng (`#fff8e1`, `#f0d28a`) để tách biệt khỏi phần nội dung chính.
- **Connection (kết nối):** Line charts trên trang Overview kết nối các điểm dữ liệu (marker) bằng đường, cho phép tri giác xu hướng liên tục theo thời gian dù World Cup chỉ diễn ra 4 năm một lần.

**Magnitude estimation:**

Nhóm ưu tiên sử dụng bar charts (chiều dài thanh) thay vì pie charts (diện tích/góc) cho các so sánh quantitative (champion count, total goals, GF, GA). Lý do: nghiên cứu về magnitude estimation cho thấy con người ước lượng chiều dài chính xác hơn so với diện tích hoặc góc. Pie chart không được sử dụng ở bất kỳ đâu trong dashboard.

---

### 5.4. Chapter 4 — Các loại biểu đồ cho xu hướng, so sánh, quan hệ, thành phần và tra cứu chi tiết

#### Nguyên tắc áp dụng

Lựa chọn chart type phù hợp với bài toán phân tích:

- **Trend (xu hướng):** Line chart.
- **Amount (so sánh lượng):** Bar chart.
- **Relationship (quan hệ):** Scatter plot.
- **Composition (thành phần):** Stacked bar chart.
- **Detail lookup (tra cứu chi tiết):** Table.

#### Cách áp dụng trong Dashboard

**Bảng 5.** Ánh xạ loại biểu đồ ↔ bài toán phân tích

| Bài toán | Chart type | Trang | Biểu đồ cụ thể |
|---|---|---|---|
| **Trend** | Line chart (lines+markers) | Overview | Tournament Scale (3 subplots: teams, matches, goals theo year); Avg Goals per Game theo year |
| **Trend** | Dot plot (scatter markers only) | Overview | Champion Timeline (year × champion, 2 traces theo host_won) |
| **Amount** | Horizontal bar chart | Dominance | Championship count (top 20 teams); Total goals (top 20 teams) |
| **Amount** | Horizontal bar chart | Tournament Detail | Goals For (all teams), Goals Against (all teams) |
| **Amount** | Horizontal bar chart | Upsets | Top 5 upsets by rank gap |
| **Composition** | Stacked bar chart | Dominance | Top 4 finishes by continent (year × count, color=continent) |
| **Composition** | Stacked bar chart | Upsets | Result distribution by neutral location (Home Win / Away Win / Draw, percentage) |
| **Relationship** | Scatter plot | Upsets | Rank gap vs Goal difference (color=is_upset) |
| **Relationship** | Bubble chart | Tournament Detail | Goals For vs Goals Against (size=Points, color=position_group) |
| **Detail lookup** | DataTable | Dominance | Team Dominance Summary (sortable, paginated, 15 rows/page) |
| **Detail lookup** | DataTable | Tournament Detail | Full standings table (sortable, paginated, 20 rows/page) |

Tổng cộng dashboard sử dụng **12 biểu đồ** và **2 bảng dữ liệu tương tác**, mỗi loại biểu đồ được chọn có chủ đích phù hợp với bài toán phân tích cụ thể.

#### Ghi chú — Lựa chọn subplots cho Overview

Biểu đồ Tournament Scale trên trang Overview sử dụng **3 subplots chia sẻ trục X** (shared x-axis) thay vì 3 đường trên cùng một biểu đồ. Quyết định này là có chủ đích: ba chỉ số teams, matches, goals_scored có đơn vị và scale rất khác nhau (teams: 13–32; matches: 17–64; goals: 70–172), nên việc đặt chung trục Y sẽ khiến đường có giá trị nhỏ bị dẹt. Subplots giúp mỗi chỉ số có trục Y riêng, đảm bảo biến thiên được thể hiện rõ ràng, đồng thời vẫn giữ được trục X chung để so sánh xu hướng theo thời gian.

---

### 5.5. Chapter 5 — Graph Data (Dữ liệu đồ thị / mạng lưới)

#### Đánh giá

Chapter này đề cập đến trực quan hóa dữ liệu dạng đồ thị (graph/network), ví dụ mạng lưới quan hệ giữa các nút và cạnh (node-link diagrams, adjacency matrices).

Bộ dữ liệu World Cup không có cấu trúc graph/network tự nhiên. Mặc dù có thể xây dựng mạng lưới "đội nào đã gặp đội nào" từ dữ liệu trận đấu, nhóm đánh giá rằng biểu diễn này không trả lời trực tiếp cho câu hỏi phân tích trung tâm của dashboard (expansion, dominance, upsets) và sẽ thêm độ phức tạp thị giác không cần thiết.

Do đó, kỹ thuật graph visualization **không được áp dụng** trong dashboard hiện tại. Đây là một hướng mở rộng tiềm năng cho phiên bản tương lai (xem mục 6.4 Future Work).

---

### 5.6. Chapter 6 — Proportional ink, bảng màu, CVD-safe colors, xử lý overlap, tiêu đề và tránh 3D

#### Nguyên tắc áp dụng

- **Proportional ink:** Diện tích mực in phải tỷ lệ thuận với giá trị dữ liệu.
- **Color palette:** Sử dụng bảng màu có chủ đích, nhất quán.
- **CVD-safe:** Cân nhắc người dùng bị rối loạn sắc giác (color vision deficiency).
- **Handling overlap:** Xử lý khi nhiều điểm dữ liệu chồng chất.
- **Titles & captions:** Mỗi biểu đồ cần có tiêu đề rõ ràng.
- **Avoid 3D:** Không sử dụng biểu đồ 3D vì gây biến dạng tri giác.

#### Cách áp dụng trong Dashboard

**Proportional ink:**

Tất cả bar charts trong dashboard đều bắt đầu từ gốc 0 (baseline = 0), đảm bảo chiều dài thanh tỷ lệ thuận hoàn toàn với giá trị dữ liệu. Không có trường hợp nào trục Y bị cắt ngắn (truncated axis) khiến biến thiên bị phóng đại. Bubble chart trên trang Tournament Detail sử dụng `size="Points"` với ánh xạ diện tích (area mapping), đảm bảo tỷ lệ diện tích bong bóng phản ánh đúng tỷ lệ giá trị.

**Color palette — hệ thống màu thống nhất:**

Dashboard sử dụng một bảng màu trung tâm được định nghĩa trong `src/theme.py` và `assets/styles.css`:

| Vai trò | Mã màu | Tên | Sử dụng |
|---|---|---|---|
| Primary accent | `#007c89` | Teal | Màu chủ đạo, sidebar, accent mặc định |
| Secondary accent | `#d98324` | Amber | Highlight champion, slider, top upsets |
| Tertiary accent | `#c44536` | Red | Cảnh báo, giá trị âm |
| Success | `#2f855a` | Green | Giá trị tích cực |
| Background | `#f6f8fb` | Light gray | Nền trang |
| Surface | `#ffffff` | White | Nền card/biểu đồ |
| Text | `#172026` | Dark | Văn bản chính |
| Muted | `#64727d` | Gray | Văn bản phụ, nhãn |

Bảng màu được đăng ký thành Plotly template `"worldcup"` và áp dụng tự động cho tất cả biểu đồ, đảm bảo tính nhất quán (consistency) trên toàn dashboard. Chuỗi `CHART_COLORS` gồm 7 màu được thiết kế có độ tương phản đủ lớn giữa các sắc liền kề.

**CVD-safe colors:**

Bảng màu chính (teal `#007c89`, amber `#d98324`, red `#c44536`) được chọn có sự khác biệt đáng kể về **luminance** (độ sáng) ngoài hue (sắc). Teal có luminance trung bình, amber có luminance cao, red có luminance thấp hơn. Điều này giúp người bị rối loạn sắc giác (đặc biệt deuteranopia — mù đỏ-xanh) vẫn phân biệt được các nhóm dữ liệu thông qua kênh luminance. Tuy nhiên, nhóm chưa thực hiện kiểm tra CVD simulation chính thức (như sử dụng Color Oracle hoặc Coblis). Đây là một điểm cần cải thiện trong tương lai.

**Xử lý overlap:**

- Scatter plot trang Upsets với ~24.000 điểm dữ liệu tiềm ẩn rủi ro overplotting nghiêm trọng. Nhóm xử lý bằng hai cách: (1) thiết lập `opacity=0.5` cho tất cả các điểm, cho phép nhìn thấy mật độ dữ liệu qua vùng đậm/nhạt; (2) bộ lọc mặc định giới hạn phạm vi năm (2000–max) giúp giảm số lượng điểm ban đầu.
- Bubble chart trang Tournament Detail: Các nhãn text chỉ hiển thị cho đội Top 8, tránh tình trạng chồng lấn text khi có 32 đội.
- Bar charts Goals For / Goals Against trên trang Tournament Detail sử dụng chiều cao 700px và kỹ thuật hiển thị xen kẽ nhãn tick cho nhóm "Other" (chỉ hiển thị cách một) để tránh chồng lấn nhãn khi có 32 đội.

**Titles & captions:**

Mỗi section biểu đồ có tiêu đề HTML (`<h3>`) bên ngoài biểu đồ thông qua component `section_block()`. Trục X và Y của tất cả biểu đồ đều có label tiếng Việt phù hợp. Các reference lines (đường tham chiếu) trên Overview đều có annotation text giải thích giá trị.

**Tránh 3D:**

Dashboard **không sử dụng bất kỳ biểu đồ 3D nào**. Tất cả các biểu đồ đều ở dạng 2D. Ngay cả khi cần thể hiện 3 chiều thông tin (ví dụ GF × GA × Points trên trang Tournament Detail), nhóm sử dụng bubble chart 2D với size channel cho chiều thứ ba, thay vì 3D scatter plot — tránh vấn đề perspective distortion và occlusion.

---

### 5.7. Chapter 7 — Map Visualization (Bản đồ)

#### Đánh giá

Map visualization là kỹ thuật mạnh mẽ khi dữ liệu có thành phần địa lý rõ ràng. Dữ liệu World Cup có yếu tố địa lý (nước chủ nhà, quốc gia đội tuyển, châu lục), tuy nhiên nhóm quyết định **không triển khai map visualization** trong phiên bản hiện tại vì các lý do sau:

1. **Dataset thiếu tọa độ:** Dữ liệu không bao gồm latitude/longitude hoặc mã quốc gia chuẩn ISO 3166, cần thêm bước ánh xạ thủ công.
2. **Câu hỏi phân tích không yêu cầu:** Ba câu hỏi trung tâm (expansion, dominance, upsets) tập trung vào xu hướng thời gian, so sánh thành tích và phân tích quan hệ — không đòi hỏi biểu diễn không gian địa lý.
3. **Choropleth map hạn chế:** Một choropleth map thể hiện số lần vô địch theo quốc gia sẽ chỉ tô màu 9 quốc gia, trong khi phần lớn bản đồ bị để trống — hiệu quả truyền đạt thông tin thấp hơn so với horizontal bar chart đang được sử dụng.

Tuy nhiên, nhóm nhận thấy map visualization có thể bổ sung giá trị cho phiên bản tương lai, cụ thể:
- Choropleth map hiển thị số lần tham dự hoặc thành tích tốt nhất theo quốc gia.
- Flow map thể hiện quá trình mở rộng địa lý của nước chủ nhà qua các kỳ.

Xem thêm mục 6.4 (Future Work).

---

### 5.8. Chapter 8 — Kỹ thuật tương tác (Interaction Techniques)

#### Nguyên tắc áp dụng

- **Filter:** Cho phép người dùng thu hẹp phạm vi dữ liệu.
- **Hover / Tooltip:** Hiển thị thông tin chi tiết khi di chuột.
- **Click detail (details-on-demand):** Hiển thị thông tin sâu khi nhấp chuột.
- **Select / Highlight:** Nhấn mạnh phần dữ liệu được chọn.
- **Navigation:** Di chuyển giữa các view khác nhau.

#### Cách áp dụng trong Dashboard

**Bảng 6.** Tổng hợp kỹ thuật tương tác trong dashboard

| Kỹ thuật | Thành phần | Trang | Mô tả |
|---|---|---|---|
| **Filter — Range slider** | `dcc.RangeSlider` | Overview, Dominance, Upsets | Cho phép chọn khoảng thời gian phân tích. Trang Dominance sử dụng step=4 (chu kỳ World Cup). |
| **Filter — Dropdown** | `dcc.Dropdown` | Overview (Host, Champion), Dominance (Team, Continent, Position), Upsets (Tournament, Team, Continent, Match type), Tournament Detail (Year) | Lọc theo biến categorical. Hỗ trợ cả single-select và multi-select tùy ngữ cảnh. |
| **Filter — Cascading** | Callback chain | Upsets | Khi thay đổi một bộ lọc, các dropdown khác tự động cập nhật danh sách tùy chọn phù hợp. Ví dụ: chọn "FIFA World Cup" ở Tournament → dropdown Team chỉ hiển thị các đội từng thi đấu World Cup. |
| **Filter — Apply/Reset** | `html.Button` | Tất cả 4 trang | Nút Apply kích hoạt callback cập nhật toàn bộ nội dung. Trang Dominance có thêm nút Reset đưa bộ lọc về mặc định. |
| **Hover / Tooltip** | Plotly built-in | Tất cả biểu đồ | Tất cả biểu đồ Plotly đều hỗ trợ hover mặc định, hiển thị giá trị chính xác, tên đội, năm, tỷ số. Một số biểu đồ có `custom_data` bổ sung (ví dụ: goals_per_appearance trên Dominance). |
| **Click detail** | `clickData` callback | Upsets | Nhấp vào điểm trên scatter plot hoặc thanh trên Top Upsets bar → hiển thị panel chi tiết trận đấu (ngày, giải đấu, đội, tỷ số, ranking, trạng thái upset). Sử dụng `ctx.triggered_id` để xác định nguồn click. |
| **Table sort & filter** | `dash_table.DataTable` | Dominance, Tournament Detail | Bảng hỗ trợ sắp xếp theo cột (click header), phân trang, và conditional formatting (highlight Champion rows bằng accent color). |
| **Multi-page navigation** | `dcc.Location` + sidebar | Toàn bộ app | Sidebar navigation với 4 link page, hỗ trợ thu gọn (collapse). Active page được highlight bằng CSS class. URL routing qua callback `render_page()`. |
| **Sidebar collapse** | `dcc.Store` + callback | Toàn bộ app | Nút toggle thu gọn sidebar từ 260px xuống 80px (chỉ hiển thị icon), trạng thái lưu vào `localStorage` qua `dcc.Store`. |

**Tổng cộng:** Dashboard triển khai **13 bộ lọc**, **10 callbacks**, và hỗ trợ hover trên tất cả 12 biểu đồ.

#### Ghi chú — Mô hình tương tác Apply-on-click

Dashboard sử dụng mô hình **Apply-on-click** thay vì reactive tức thì (filter thay đổi → biểu đồ cập nhật ngay). Quyết định này là có chủ đích: khi người dùng muốn thay đổi nhiều bộ lọc cùng lúc (ví dụ: chọn continent + year range + position group), việc cập nhật biểu đồ sau mỗi thay đổi đơn lẻ sẽ gây hiệu ứng nhấp nháy (flickering) và tốn tài nguyên tính toán không cần thiết. Nút Apply cho phép người dùng cấu hình xong tất cả bộ lọc rồi áp dụng một lần.

Ngoại lệ: Callback cascading filter trên trang Upsets vẫn hoạt động reactive để cập nhật danh sách tùy chọn dropdown, vì đây là thao tác nhẹ và cải thiện trải nghiệm người dùng.

---

### 5.9. Chapter 9 — Storytelling (Kể chuyện bằng dữ liệu)

#### Nguyên tắc áp dụng

- **Narrative structure:** Tổ chức thông tin theo mạch truyện có mở đầu, phát triển và kết luận.
- **Guided story vs. Free exploration:** Kết hợp giữa dẫn dắt người xem và cho phép tự khám phá.
- **Insight cards & annotations:** Đưa insight trực tiếp vào biểu đồ thay vì để riêng.

#### Cách áp dụng trong Dashboard

**Narrative structure — mạch truyện 4 act:**

Dashboard được thiết kế theo cấu trúc narrative 4 act rõ ràng, thể hiện qua thứ tự 4 trang trong sidebar navigation:

1. **Act 1 — Setup (Overview):** Thiết lập bối cảnh — World Cup đã tăng trưởng mạnh mẽ. Người xem nhìn thấy các biểu đồ xu hướng đi lên, KPI cards cho thấy quy mô lớn. Đây là phần "kể chuyện" nhẹ nhàng, tạo nền tảng cho câu hỏi tiếp theo.

2. **Act 2 — Complication (Dominance):** Đưa ra xung đột — sự mở rộng không dẫn đến sự cân bằng. Bar charts cho thấy chỉ 9 đội từng vô địch, stacked bar cho thấy 2 châu lục thống trị. Phần này tạo sự bất ngờ và thách thức giả định ban đầu của người xem.

3. **Act 3 — Nuance (Upsets):** Bổ sung chiều sâu — dù danh hiệu tập trung, từng trận đấu vẫn có bất ngờ. Scatter plot cho thấy mối tương quan yếu giữa ranking và kết quả. Phần này cân bằng lại narrative bằng cách cho thấy bức tranh phức tạp hơn mức "nhóm elite thống trị tuyệt đối".

4. **Act 4 — Resolution (Tournament Detail 2022):** Minh họa bằng case study cụ thể — World Cup 2022 kết hợp cả elite (Argentina, France, Croatia) và outsider (Morocco), mang lại một kết luận trọn vẹn cho toàn bộ câu chuyện.

**Kết hợp Guided Story và Free Exploration:**

| Guided Story | Free Exploration |
|---|---|
| Thứ tự trang trong sidebar dẫn dắt theo narrative flow | Bộ lọc trên mỗi trang cho phép tùy chỉnh phân tích |
| KPI cards cung cấp insight tổng quan tức thì | DataTable cho phép sắp xếp và tra cứu chi tiết |
| Annotation trên biểu đồ đánh dấu mốc lịch sử | Click-to-detail hiển thị thông tin từng trận đấu |
| Insight panel 2022 kể câu chuyện 4 đội top | Dropdown year cho phép xem bất kỳ kỳ nào |
| Champion highlight (màu accent) hướng sự chú ý | Cascading filter cho phép khám phá tổ hợp |

**Annotations trực tiếp trên biểu đồ:**

Thay vì viết insight dài dưới biểu đồ, dashboard đưa thông tin trực tiếp vào biểu đồ qua:

- **Annotation mũi tên** trên Tournament Scale (Overview): đánh dấu các mốc 1950, 1982, 1998 với text giải thích ngắn gọn (ví dụ: "Trở lại sau WWII", "Mở rộng 24 đội", "Mở rộng 32 đội").
- **Reference lines** (đường tham chiếu): đường trung bình trên Avg Goals chart, đường GF=GA trên bubble chart, đường x=0 và y=0 trên scatter plot — giúp người xem có ngữ cảnh so sánh ngay trên biểu đồ.
- **Quadrant labels** trên bubble chart: phân chia vùng "Tấn công mạnh, Thủ tốt" vs "Tấn công yếu, Thủ kém" giúp phân loại phong cách đội tuyển tức thì.
- **Highlight bands** (`vrect`) trên stacked bar (Dominance): dải màu nhẹ phân chia các giai đoạn thay đổi thể thức giải đấu, cung cấp bối cảnh lịch sử mà không cần chú thích riêng.

---

## 6. Kết luận (Conclusion)

### 6.1. Tóm tắt kết quả

Dashboard FIFA World Cup đã được thiết kế và triển khai thành công dưới dạng ứng dụng web tương tác multi-page sử dụng Dash, Plotly và Pandas. Dashboard bao gồm 4 trang phân tích, 12 biểu đồ tương tác, 2 bảng dữ liệu, 24 KPI cards, và 13 bộ lọc, kết hợp cả phương pháp explanatory (kể chuyện có dẫn dắt) và exploratory (khám phá tự do).

Thông qua mạch kể chuyện dữ liệu 4 act, dashboard đã trả lời được câu hỏi phân tích trung tâm: **World Cup đã mở rộng mạnh mẽ về quy mô tổ chức trong gần một thế kỷ, nhưng sự phân bổ quyền lực vô địch gần như không thay đổi — chức vô địch vẫn tập trung vào một nhóm nhỏ đội tuyển từ Europe và South America.** Tuy nhiên, ở cấp độ từng trận đấu, bóng đá vẫn luôn ẩn chứa tính bất ngờ, và World Cup 2022 là minh chứng hoàn hảo cho sự đan xen giữa truyền thống elite và những outsider quả cảm.

### 6.2. Tóm tắt các insight chính

| # | Insight | Minh chứng |
|:---:|---|---|
| 1 | Quy mô World Cup tăng trưởng liên tục | 13 → 32 đội, 18 → 64 trận (Overview line charts) |
| 2 | Hiệu suất ghi bàn không tăng theo quy mô | Avg goals/game đạt đỉnh ở 1954, ổn định ~2.5 từ 1990s (Overview avg goals chart) |
| 3 | Chỉ 9 đội từng vô địch trong 22 kỳ | Brazil 5, Germany 4, Italy 4 lần (Dominance champion bar) |
| 4 | Europe & South America thống trị Top 4 | Gần 100% vị trí Top 4 trong lịch sử (Dominance stacked bar) |
| 5 | Ranking FIFA tương quan yếu với kết quả | Scatter plot cho thấy phân bố rộng (Upsets scatter) |
| 6 | Morocco 2022 — outsider lịch sử | Đội châu Phi đầu tiên vào Top 4 (Tournament Detail 2022) |

### 6.3. Tóm tắt kỹ thuật visualization đã áp dụng

Dashboard áp dụng đa dạng các kỹ thuật trực quan hóa đã học trong chương trình:

- **Lựa chọn chart type có chủ đích**: Line chart cho trend, bar chart cho amount, scatter/bubble cho relationship, stacked bar cho composition, DataTable cho detail lookup.
- **Visual encoding hiệu quả**: Ưu tiên position và length (channel chính xác nhất); color hue chỉ cho biến categorical; size cho quantitative bổ sung; shape cho boolean.
- **Pre-attentive processing**: Highlight champion bằng accent color, tách biệt upset vs normal bằng hue + opacity.
- **Gestalt principles**: Proximity (nhóm KPI), Similarity (style nhất quán), Enclosure (chart cards), Connection (line charts).
- **Proportional ink**: Tất cả bar charts bắt đầu từ 0, không truncated axis.
- **Bảng màu nhất quán**: Plotly template `"worldcup"` đảm bảo tính consistency.
- **Interaction phong phú**: Filter, hover, click detail, cascading filter, table sort, multi-page navigation, sidebar collapse.
- **Storytelling**: Narrative 4-act, kết hợp guided story và free exploration, annotation trực tiếp trên biểu đồ.

### 6.4. Hạn chế

1. **Thiếu map visualization**: Dashboard chưa triển khai biểu đồ bản đồ dù dữ liệu có yếu tố địa lý, do dataset thiếu tọa độ và mã quốc gia chuẩn.
2. **Hiệu năng scatter plot**: Scatter plot trên trang Upsets với tối đa ~24.000 điểm có thể gây lag khi không áp dụng bộ lọc. Cần cân nhắc kỹ thuật sampling hoặc aggregation cho dữ liệu lớn hơn.
3. **CVD testing chưa đầy đủ**: Bảng màu đã cân nhắc luminance contrast nhưng chưa được kiểm tra chính thức bằng công cụ CVD simulation.
4. **Chuẩn hóa tên đội hạn chế**: Chỉ ánh xạ "West Germany" → "Germany", chưa xử lý hết các trường hợp lịch sử khác (Soviet Union, Czechoslovakia, Yugoslavia).
5. **Thiếu small multiples**: Một số biểu đồ có thể hưởng lợi từ kỹ thuật small multiples (ví dụ: so sánh phân bố bàn thắng theo châu lục) nhưng chưa được triển khai.

### 6.5. Hướng phát triển (Future Work)

- **Map visualization**: Bổ sung choropleth map hiển thị số lần tham dự hoặc thành tích tốt nhất theo quốc gia, sử dụng thư viện Plotly Express `choropleth` kết hợp mã ISO 3166.
- **Small multiples**: Triển khai small multiples cho biểu đồ xu hướng bàn thắng theo châu lục hoặc theo nhóm thành tích, cho phép so sánh đồng thời nhiều nhóm.
- **Tối ưu hiệu năng scatter**: Áp dụng kỹ thuật WebGL rendering (`px.scatter` với `render_mode="webgl"`) hoặc server-side aggregation cho tập dữ liệu lớn.
- **Cập nhật dữ liệu**: Bổ sung dữ liệu World Cup 2026 (dự kiến 48 đội) khi có sẵn — đây sẽ là mốc mở rộng lịch sử mới và là case study thú vị cho phân tích tiếp theo.
- **Graph visualization**: Xây dựng network diagram thể hiện lịch sử đối đầu giữa các đội tuyển, với kích thước node tỷ lệ số lần tham dự và độ đậm cạnh tỷ lệ số lần gặp nhau.
- **CVD verification**: Kiểm tra toàn bộ bảng màu bằng công cụ Color Oracle hoặc tương đương, điều chỉnh nếu cần thiết.

---

## Tài liệu tham khảo (References)

1. Sourav Banerjee, "FIFA Football World Cup Dataset," Kaggle, 2023. [Online]. Available: https://www.kaggle.com/datasets/iamsouravbanerjee/fifa-football-world-cup-dataset/data

2. Brenda, "FIFA World Cup 2022," Kaggle, 2022. [Online]. Available: https://www.kaggle.com/datasets/brenda89/fifa-world-cup-2022/data

3. Plotly Technologies Inc., "Dash — Python Framework for Building ML & Data Science Web Apps," 2024. [Online]. Available: https://dash.plotly.com/

4. Plotly Technologies Inc., "Plotly Python Open Source Graphing Library," 2024. [Online]. Available: https://plotly.com/python/

5. The pandas development team, "pandas — Python Data Analysis Library," 2024. [Online]. Available: https://pandas.pydata.org/

6. Tài liệu bài giảng môn Data Visualization — Các chapter 1–9, Giảng viên phụ trách môn học.
