# FIFA World Cup Dashboard Report

**Chủ đề:** FIFA World Cup Dashboard — Tăng trưởng, Thống trị và Bất ngờ  
**Môn học:** Data Visualization  
**Nhóm:** 2  
**Công cụ:** Dash · Plotly · Pandas

---

## 1. Giới thiệu (Introduction)

### 1.1. Bối cảnh

FIFA World Cup là giải đấu bóng đá lớn nhất hành tinh, được tổ chức lần đầu tiên vào năm 1930 tại Uruguay với sự tham gia của 13 đội tuyển. Trải qua gần một thế kỷ phát triển, giải đấu đã mở rộng lên 32 đội (từ năm 1998) với hàng tỷ khán giả theo dõi trên toàn cầu. Sự mở rộng về quy mô tổ chức, số lượng đội tuyển tham dự và mức độ phủ sóng truyền thông đặt ra một câu hỏi thú vị cho phân tích dữ liệu: liệu sự tăng trưởng này có đi kèm với sự phân tán quyền lực và tính cạnh tranh thực sự, hay bóng đá đỉnh cao vẫn là sân chơi của một nhóm nhỏ đội tuyển ưu tú?

Với lượng dữ liệu lịch sử phong phú từ 22 kỳ World Cup (1930–2022) và gần 24.000 trận đấu quốc tế có bảng xếp hạng FIFA, đây là một bài toán phù hợp để áp dụng các kỹ thuật trực quan hóa dữ liệu nhằm khám phá xu hướng, so sánh thành tích và phát hiện các mẫu hình (patterns) ẩn sau những con số.

### 1.2. Mục tiêu dashboard

Dashboard được thiết kế với ba mục tiêu chính:

1. **Khám phá xu hướng tăng trưởng** của World Cup qua thời gian về quy mô tổ chức, số đội tham dự, số trận đấu và hiệu suất ghi bàn.
2. **Phân tích mức độ tập trung quyền lực** trong lịch sử giải đấu — xác định những đội tuyển và khu vực địa lý nào thống trị danh hiệu vô địch và các vị trí cao.
3. **Đánh giá tính cạnh tranh thực tế** ở cấp độ từng trận đấu — kiểm tra mối quan hệ giữa bảng xếp hạng FIFA và kết quả trận đấu, đồng thời phát hiện các trận đấu bất ngờ (upsets).

### 1.3. Câu hỏi phân tích chính

> **World Cup đã thật sự trở thành một giải đấu toàn cầu hơn, hay chức vô địch vẫn nằm trong tay một nhóm đội tuyển elite?**

Câu hỏi trung tâm này được phân tách thành ba câu hỏi phụ:

- **Q1 — Expansion:** Quy mô World Cup đã thay đổi như thế nào qua thời gian về số đội, số trận, tổng bàn thắng và bàn thắng trung bình mỗi trận?
- **Q2 — Dominance:** Đội tuyển và khu vực địa lý nào kiểm soát lịch sử giải đấu? Sự phân bổ danh hiệu có trở nên đa dạng hơn hay vẫn tập trung?
- **Q3 — Competitiveness:** Ở cấp độ từng trận, bảng xếp hạng FIFA có dự đoán chính xác kết quả không? Mức độ bất ngờ (upset) trong các trận đấu quốc tế là bao nhiêu?

### 1.4. Phạm vi phân tích

- **Dữ liệu World Cup:** Toàn bộ 22 kỳ World Cup từ 1930 đến 2022, bao gồm thông tin tổng quan giải đấu và bảng xếp hạng chi tiết từng đội tuyển.
- **Dữ liệu trận đấu quốc tế:** 23.921 trận đấu quốc tế từ 1993 đến 2022, bao gồm bảng xếp hạng FIFA, tỷ số, giải đấu và thông tin sân trung lập.
- **Case study:** World Cup 2022 tại Qatar được sử dụng làm ví dụ phân tích chi tiết.

---

## 2. Mô tả dữ liệu (Dataset Description)

### 2.1. Nguồn dữ liệu

Dashboard sử dụng dữ liệu từ hai bộ dataset trên nền tảng Kaggle:

1. **FIFA Football World Cup Dataset** — tác giả Sourav Banerjee  
   URL: https://www.kaggle.com/datasets/iamsouravbanerjee/fifa-football-world-cup-dataset/data  
   Bao gồm file tổng quan lịch sử các kỳ World Cup và 22 file bảng xếp hạng chi tiết theo từng năm tổ chức.

2. **FIFA World Cup 2022 Dataset** — tác giả Brenda  
   URL: https://www.kaggle.com/datasets/brenda89/fifa-world-cup-2022/data  
   Cung cấp dữ liệu trận đấu quốc tế từ 1993 đến 2022 kèm bảng xếp hạng FIFA.

### 2.2. Tổng quan các file dữ liệu

Bảng 1 trình bày tổng quan các file dữ liệu được sử dụng trong dashboard.

**Bảng 1.** Tổng quan các file dữ liệu

| File dữ liệu | Số dòng | Số cột | Mô tả |
|---|:---:|:---:|---|
| `FIFA - World Cup Summary.csv` | 22 | 10 | Thông tin tổng quan từng kỳ World Cup: năm, nước chủ nhà, nhà vô địch, á quân, hạng ba, hạng tư, số đội, số trận, tổng bàn thắng, bàn thắng trung bình/trận. |
| `FIFA - {YYYY}.csv` (22 files) | Tổng 454 | 7 | Bảng xếp hạng chi tiết từng đội tuyển trong từng kỳ: vị trí, tên đội, số trận, bàn ghi, bàn thủng, hiệu số, điểm. |
| `international_matches.csv` | 23.921 | 17 | Kết quả trận đấu quốc tế 1993–2022: ngày, đội nhà/khách, tỷ số, giải đấu, thành phố, nước, sân trung lập, bảng xếp hạng FIFA, điểm FIFA, tỷ số luân lưu, kết quả. |

### 2.3. Các biến chính theo nhóm

Bảng 2 phân loại các biến quan trọng theo loại dữ liệu.

**Bảng 2.** Phân loại biến dữ liệu

| Loại biến | Biến | Nguồn |
|---|---|---|
| **Nominal** | `host`, `champion`, `runner_up`, `third_place`, `fourth_place`, `home_team`, `away_team`, `tournament`, `city`, `country` | Summary, Matches |
| **Ordinal** | `position` (1–32), `position_group` (Champion / Top 4 / Top 8 / Other), `home_team_result` (Win / Draw / Lose) | Standings, Derived |
| **Quantitative (ratio)** | `teams`, `matches_played`, `goals_scored`, `avg_goals_per_game`, `goals_for`, `goals_against`, `goal_difference`, `points`, `home_team_score`, `away_team_score`, `home_team_fifa_rank`, `away_team_fifa_rank` | Summary, Standings, Matches |
| **Quantitative (derived)** | `rank_gap`, `home_goal_diff`, `upset_rank_gap`, `goals_per_appearance` | Derived |
| **Boolean** | `neutral_location`, `host_won`, `is_upset` | Matches, Derived |
| **Temporal** | `year`, `date` | Summary, Matches |

### 2.4. Tiền xử lý dữ liệu

Quá trình tiền xử lý dữ liệu được thực hiện trong module `src/data.py` và bên trong từng page module. Các bước chính bao gồm:

#### 2.4.1. Chuẩn hóa tên cột

Tất cả các cột được chuyển về dạng snake_case (viết thường, thay dấu cách và gạch ngang bằng gạch dưới) thông qua hàm `_snake_case_columns()`. Ví dụ: `"Matches Played"` → `"matches_played"`, `"Goals For"` → `"goals_for"`.

#### 2.4.2. Chuẩn hóa tên đội tuyển

Một số tên đội tuyển lịch sử được chuẩn hóa về tên hiện đại để đảm bảo tính nhất quán khi phân tích liên kỳ. Cụ thể, `"West Germany"` được ánh xạ thành `"Germany"` thông qua hàm `normalize_team_name()` và từ điển `TEAM_NORMALIZATION`.

#### 2.4.3. Ghép nối dữ liệu standings

22 file standings riêng biệt (mỗi file tương ứng một kỳ World Cup) được đọc và ghép nối (concatenate) thành một DataFrame duy nhất gồm 454 dòng. Mỗi dòng được gắn thêm cột `year` tương ứng, trích xuất từ tên file (ví dụ: `"FIFA - 2022.csv"` → `year = 2022`).

#### 2.4.4. Ánh xạ khu vực địa lý (continent)

Trong module `pages/dominance.py`, một hàm ánh xạ tự động (`_load_team_continent_mapping()`) được xây dựng bằng cách đọc file `international_matches.csv` và xác định châu lục phổ biến nhất (mode) cho mỗi đội tuyển. Đối với các đội tuyển lịch sử không có trong dữ liệu trận đấu hiện đại, một từ điển dự phòng (`FALLBACK_TEAM_CONTINENT`) được sử dụng.

#### 2.4.5. Các biến phái sinh (derived fields)

Bảng 3 liệt kê tất cả các biến được tạo thêm trong quá trình xử lý dữ liệu, kèm công thức hoặc logic tính toán.

**Bảng 3.** Các biến phái sinh

| Biến | Công thức / Logic | Module |
|---|---|---|
| `champion_norm` | `normalize_team_name(champion)` — ánh xạ "West Germany" → "Germany" | `data.py` |
| `runner_up_norm` | `normalize_team_name(runner_up)` | `data.py` |
| `third_place_norm` | `normalize_team_name(third_place)` | `data.py` |
| `host_norm` | `normalize_team_name(host)` | `data.py` |
| `host_won` | `host_norm == champion_norm` (boolean) | `data.py` |
| `team_norm` | `normalize_team_name(team)` | `data.py` |
| `position_group` | `pd.cut(position, bins=[0,1,4,8,∞], labels=["Champion","Top 4","Top 8","Other"])` | `data.py` |
| `year` (matches) | `date.dt.year` | `data.py` |
| `home_team_norm` | `normalize_team_name(home_team)` | `data.py` |
| `away_team_norm` | `normalize_team_name(away_team)` | `data.py` |
| `home_goal_diff` | `home_team_score - away_team_score` | `data.py` |
| `rank_gap` | `home_team_fifa_rank - away_team_fifa_rank` | `data.py` |
| `winner` | `"Draw"` nếu hòa; tên đội thắng nếu có kết quả | `data.py` |
| `winner_rank` | Thứ hạng FIFA của đội thắng | `data.py` |
| `loser_rank` | Thứ hạng FIFA của đội thua | `data.py` |
| `is_upset` | `(winner ≠ "Draw") AND (winner_rank > loser_rank)` — đội thắng có thứ hạng kém hơn | `data.py` |
| `upset_rank_gap` | `winner_rank - loser_rank` (chỉ khi `is_upset = True`) | `data.py` |
| `date_str` | `date.strftime("%Y-%m-%d")` | `data.py` |
| `match_short_label` | `"HomeTeam X - Y AwayTeam"` (chuỗi mô tả ngắn trận đấu) | `data.py` |
| `continent` | Ánh xạ tên đội → châu lục qua mode analysis hoặc fallback dict | `dominance.py` |
| `goals_per_appearance` | `total_goals_for / appearances` (tính cho mỗi đội qua tổng hợp) | `dominance.py` |

### 2.5. Kiểm tra giá trị thiếu (missing values)

Bảng 4 trình bày kết quả kiểm tra giá trị thiếu cho từng dataset.

**Bảng 4.** Giá trị thiếu trong dữ liệu

| Dataset | Biến có missing | Số dòng thiếu | Ghi chú |
|---|---|:---:|---|
| World Cup Summary | (không có) | 0 | Dữ liệu đầy đủ cho cả 22 kỳ. |
| Standings (22 files) | (không có) | 0 | Dữ liệu đầy đủ cho tất cả 454 dòng. |
| International Matches | `city` | 3 | Có thể bỏ qua, không ảnh hưởng phân tích. |
| | `home_team_fifa_rank` | 276 | Một số trận đấu đầu giai đoạn 1993 chưa có bảng xếp hạng FIFA. Các trận này bị loại khi phân tích upset. |
| | `away_team_fifa_rank` | 276 | Tương tự `home_team_fifa_rank`. |
| | `home_team_total_fifa_points` | 276 | Tương tự. |
| | `away_team_total_fifa_points` | 276 | Tương tự. |
| | `home_team_score_penalty` | 22.932 | Chỉ có giá trị khi trận đấu diễn ra đá luân lưu (96% trận không có). Đây là đặc điểm tự nhiên của dữ liệu, không phải lỗi. |
| | `away_team_score_penalty` | 22.932 | Tương tự. |

### 2.6. Hạn chế dữ liệu

- **Phạm vi thời gian không đồng nhất:** Dữ liệu World Cup bao phủ 1930–2022 (gần 100 năm), trong khi dữ liệu trận đấu quốc tế chỉ từ 1993–2022 (30 năm). Do đó, phân tích upset và ranking chỉ áp dụng được cho giai đoạn hiện đại.
- **Thiếu bảng xếp hạng FIFA trước 1993:** Bảng xếp hạng FIFA chính thức bắt đầu từ 1993, nên không thể đánh giá tính bất ngờ (upset) cho các trận đấu trước giai đoạn này.
- **Chuẩn hóa tên đội hạn chế:** Hiện tại chỉ ánh xạ `"West Germany"` → `"Germany"`. Một số trường hợp khác như `"Soviet Union"` → `"Russia"`, `"Czechoslovakia"` → `"Czech Republic"` chưa được xử lý, có thể ảnh hưởng nhẹ đến phân tích liên kỳ.
- **Không có dữ liệu bản đồ địa lý:** Dataset không bao gồm tọa độ (latitude/longitude) hoặc mã quốc gia chuẩn ISO, nên không hỗ trợ trực tiếp cho việc tạo bản đồ (map visualization).

---

## 3. Thiết kế Dashboard (Dashboard Design)

### 3.1. Công nghệ sử dụng

Dashboard được xây dựng trên nền tảng web application sử dụng bộ công cụ Python sau:

- **Dash** (Plotly Dash): Framework ứng dụng web tương tác, cho phép xây dựng giao diện bằng Python với mô hình callback reactive.
- **Plotly**: Thư viện trực quan hóa tương tác, hỗ trợ nhiều loại biểu đồ (line, bar, scatter) với khả năng hover, zoom, và click.
- **Pandas**: Thư viện xử lý và phân tích dữ liệu dạng bảng, sử dụng cho đọc CSV, lọc, nhóm và tính toán thống kê.
- **CSS tùy chỉnh**: File `assets/styles.css` với hệ thống CSS variables và responsive design hỗ trợ nhiều kích thước màn hình.

Toàn bộ hệ thống visual được thống nhất qua một Plotly template tùy chỉnh có tên `"worldcup"` (đăng ký trong `src/theme.py`), đảm bảo tính nhất quán về font (Inter), bảng màu, grid styling, và legend positioning trên tất cả các biểu đồ.

### 3.2. Cấu trúc multi-page dashboard

Ứng dụng được tổ chức dưới dạng **multi-page dashboard** với một sidebar navigation cố định bên trái (có thể thu gọn) và vùng nội dung chính bên phải. Điều hướng giữa các trang sử dụng `dcc.Location` và callback routing. Dashboard gồm 4 trang chính:

| Trang | Đường dẫn | Biểu tượng | Mục đích |
|---|---|:---:|---|
| Executive Overview | `/` | 📊 | Xu hướng tăng trưởng quy mô World Cup |
| Dominance | `/dominance` | 🏆 | Phân tích sự thống trị và di sản |
| Upsets & Competitiveness | `/upsets` | ⚡ | Tính cạnh tranh và các trận bất ngờ |
| Tournament Detail | `/tournament` | 📅 | Chi tiết từng kỳ World Cup cụ thể |

### 3.3. Mạch kể chuyện (Storytelling Flow)

Dashboard không chỉ là tập hợp các biểu đồ rời rạc, mà được tổ chức theo một **narrative structure** (mạch kể chuyện) dẫn dắt người xem đi từ bức tranh tổng quan đến phân tích chi tiết:

```
Overview (Expansion)  →  Dominance (Concentration)  →  Upsets (Surprises)  →  Tournament Detail (Case Study)
```

- **Act 1 — Expansion:** World Cup ngày càng lớn hơn về quy mô.
- **Act 2 — Dominance:** Lớn hơn không đồng nghĩa với cân bằng — danh hiệu vẫn tập trung.
- **Act 3 — Upsets:** Tuy nhiên, ở cấp độ từng trận, bóng đá vẫn đầy bất ngờ.
- **Act 4 — Case Study 2022:** Minh họa tất cả qua World Cup 2022.

Mạch truyện này kết hợp phương pháp **guided storytelling** (dẫn dắt qua sidebar navigation và thứ tự các trang) với **free exploration** (người dùng có thể tự lọc, nhấp vào biểu đồ và khám phá theo ý muốn).

### 3.4. Executive Overview

**Mục tiêu:** Trả lời Q1 — World Cup đã thay đổi quy mô như thế nào qua gần một thế kỷ?

![Hình 1. Trang Executive Overview — KPI cards và biểu đồ xu hướng quy mô](dashboard_image/overview_1.png)

*Hình 1. Trang Executive Overview — KPI cards và biểu đồ xu hướng quy mô.*

#### Thành phần giao diện

**5 KPI Cards** (hàng trên cùng):
- Tournaments: tổng số kỳ World Cup trong phạm vi lọc.
- Team entries: tổng lượt tham dự của tất cả đội tuyển.
- Matches: tổng số trận đấu.
- Goals: tổng số bàn thắng.
- Champion nations: số đội tuyển khác nhau từng vô địch.

**Bộ lọc (filter bar):**
- Year range slider (RangeSlider): cho phép chọn khoảng thời gian phân tích.
- Host dropdown (multi-select): lọc theo nước chủ nhà.
- Champion dropdown (multi-select): lọc theo đội vô địch.
- Nút Apply: áp dụng bộ lọc.

**Biểu đồ chính:**

1. **Tournament Scale** — 3 biểu đồ đường xếp chồng theo trục dọc (subplots chia sẻ trục X) hiển thị xu hướng theo năm của ba chỉ số: số đội tham dự (`teams`), số trận đấu (`matches_played`), và tổng bàn thắng (`goals_scored`). Sử dụng `go.Scatter` với `mode="lines+markers"`. Mỗi biểu đồ có đường tham chiếu (hline) tại giá trị trung bình tổng thể. Ba annotation mũi tên đánh dấu các mốc lịch sử quan trọng: 1950 ("Trở lại sau WWII"), 1982 ("Mở rộng 24 đội"), 1998 ("Mở rộng 32 đội").

2. **Average Goals per Game** — Biểu đồ đường đơn hiển thị bàn thắng trung bình mỗi trận theo năm. Có đường tham chiếu ngang (dashed, màu đỏ) tại giá trị trung bình toàn kỳ, kèm annotation ghi chú điểm cực đại.

![Hình 2. Trang Executive Overview — Champion Timeline](dashboard_image/overview_2.png)

*Hình 2. Trang Executive Overview — Champion Timeline.*

3. **Champion Timeline** — Biểu đồ chấm (dot plot) với trục X là năm, trục Y là tên đội vô địch. Sử dụng 2 trace phân biệt bằng marker: ngôi sao (★) cho kỳ mà nước chủ nhà vô địch (`host_won = True`), hình tròn (●) cho các kỳ còn lại. Cho phép nhận diện nhanh mẫu hình lặp lại của nhóm đội tuyển chiến thắng.

#### Insight chính

Từ các biểu đồ trên trang Overview, người xem có thể nhận ra:
- Quy mô World Cup tăng trưởng rõ rệt qua thời gian: từ 13 đội và 18 trận năm 1930 lên 32 đội và 64 trận từ năm 1998.
- Tổng bàn thắng tăng theo quy mô giải đấu, nhưng bàn thắng trung bình mỗi trận không tăng tương ứng — thậm chí giảm từ đỉnh cao >5 bàn/trận ở thập niên 1950 xuống khoảng 2.5–2.7 bàn/trận ở thời kỳ hiện đại.
- Champion Timeline cho thấy một số đội tuyển xuất hiện nhiều lần (Brazil 5 lần, Germany 4 lần, Italy 4 lần), gợi ý sự tập trung quyền lực — chủ đề sẽ được phân tích sâu hơn ở trang Dominance.

### 3.5. Dominance

**Mục tiêu:** Trả lời Q2 — Đội tuyển và khu vực nào thống trị lịch sử World Cup?

![Hình 3. Trang Dominance — Biểu đồ vô địch, Top 4 theo châu lục, và bảng tổng hợp](dashboard_image/dominance_1.png)

*Hình 3. Trang Dominance — Biểu đồ vô địch, phân bổ Top 4 theo châu lục, và biểu đồ tổng bàn thắng.*

#### Thành phần giao diện

**4 KPI Cards:**
- Tournaments: số kỳ World Cup trong phạm vi lọc.
- Teams: số đội tuyển khác nhau.
- Titles: tổng số lần vô địch (có thể bằng số kỳ nếu không lọc).
- Top 4 Finishes: tổng số lượt lọt vào Top 4.

**Bộ lọc (filter bar):**
- Year range slider (step=4, tương ứng chu kỳ World Cup).
- Team dropdown (multi-select): lọc theo đội tuyển cụ thể.
- Continent dropdown (multi-select): lọc theo châu lục.
- Position group dropdown (multi-select): lọc theo nhóm thành tích (Champion, Top 4, Top 8, Other).
- Nút Apply và Reset.

**Biểu đồ chính:**

1. **Championship Count** — Biểu đồ thanh ngang (`px.bar`, horizontal) hiển thị top 20 đội tuyển theo số lần vô địch. Đội có nhiều danh hiệu nhất được tô màu amber (`accent_2`), các đội khác dùng màu xám nhẹ, tạo hiệu ứng pre-attentive attention hướng ánh nhìn vào nhà vô địch nhiều nhất.

2. **Top 4 by Continent** — Biểu đồ thanh xếp chồng theo chiều dọc (`px.bar`, stacked). Trục X là năm tổ chức, trục Y là số lượt Top 4, màu sắc phân chia theo châu lục. Các dải `vrect` phủ nhẹ đánh dấu từng giai đoạn thay đổi thể thức giải đấu. Biểu đồ cho thấy trực quan sự áp đảo gần như tuyệt đối của Europe và South America trong nhóm dẫn đầu.

3. **Total Goals — Top 20** — Biểu đồ thanh ngang hiển thị tổng bàn thắng tích lũy của top 20 đội tuyển, kèm thông tin số lần tham dự và hiệu suất bàn thắng/lần tham dự qua `custom_data` và hover.

**Bảng tổng hợp (DataTable):**

Bảng dữ liệu tương tác cho phép sắp xếp và phân trang (15 dòng/trang), hiển thị: Team, Continent, Appearances, Championships, Top 4, Best Position, Goals For, Points. Các dòng có vị trí Champion (Position=1) được tô nổi bật bằng màu accent.

#### Insight chính

- Chỉ có 9 đội tuyển từng vô địch World Cup trong 22 kỳ tổ chức, cho thấy quyền lực vô địch cực kỳ tập trung.
- Brazil dẫn đầu với 5 lần vô địch, tiếp theo là Germany và Italy (4 lần mỗi đội).
- Biểu đồ Top 4 by Continent chứng minh rằng Europe và South America chiếm gần như toàn bộ các vị trí Top 4 trong lịch sử, với rất ít ngoại lệ (Hàn Quốc 2002, Morocco 2022).

### 3.6. Upsets & Competitiveness

**Mục tiêu:** Trả lời Q3 — Bảng xếp hạng FIFA có phản ánh chính xác kết quả trận đấu?

![Hình 4. Trang Upsets & Competitiveness — Scatter plot, Top Upsets, và phân bố kết quả](dashboard_image/upsets_1.png)

*Hình 4. Trang Upsets & Competitiveness — Scatter plot rank gap vs goal difference, top 5 upsets, phân bố kết quả theo sân trung lập.*

#### Thành phần giao diện

**6 KPI Cards** (được xây dựng động):
- Matches: tổng số trận đấu sau lọc.
- Upsets: số trận bất ngờ kèm tỷ lệ phần trăm.
- Home win rate: tỷ lệ thắng sân nhà.
- Draw rate: tỷ lệ hòa.
- Away win rate: tỷ lệ thắng sân khách.
- Neutral matches: số trận trên sân trung lập kèm số trận đá luân lưu.

**Bộ lọc (filter bar):**
- Year range slider (bước 1 năm, mặc định 2000–max).
- Tournament dropdown (single-select): lọc theo giải đấu (FIFA World Cup, Qualifier, Friendly, v.v.).
- Team dropdown (single-select): lọc theo đội tuyển tham gia.
- Continent dropdown (single-select): lọc theo châu lục.
- Match type dropdown (All / Shootout / Neutral).
- Nút Apply.
- Các dropdown hỗ trợ **cascading filter**: khi thay đổi một bộ lọc, các bộ lọc khác tự động cập nhật danh sách tùy chọn phù hợp.

**Biểu đồ chính:**

1. **Rank Gap vs Goal Difference** — Scatter plot (`px.scatter`) là biểu đồ trung tâm của trang. Trục X biểu thị `rank_gap` (chênh lệch thứ hạng FIFA giữa hai đội), trục Y biểu thị `home_goal_diff` (chênh lệch bàn thắng thực tế). Màu sắc phân biệt trận bình thường (xám) và trận upset (cam/accent). Các đường tham chiếu ngang và dọc tại vị trí 0 chia biểu đồ thành 4 phần tư. Biểu đồ chiếm diện tích lớn (spanning 2 rows) để dễ quan sát phân phối.

2. **Top 5 Upsets** — Biểu đồ thanh ngang hiển thị 5 trận có `upset_rank_gap` lớn nhất (đội cửa dưới thắng với chênh lệch ranking cao nhất). Nhãn text được đặt bên trong thanh.

3. **Result Distribution by Neutral Location** — Biểu đồ thanh xếp chồng theo chiều dọc, so sánh tỷ lệ phần trăm kết quả (Home Win / Away Win / Draw) giữa trận đấu trên sân nhà/sân khách và trận trên sân trung lập. Annotation hiển thị tổng số trận cho mỗi nhóm.

**Bảng chi tiết trận đấu (click-driven):**

Khi người dùng nhấp vào một điểm trên scatter plot hoặc một thanh trên biểu đồ top upsets, một panel chi tiết hiển thị thông tin đầy đủ của trận đấu: ngày, giải đấu, hai đội, tỷ số, thứ hạng FIFA, chênh lệch ranking, và trạng thái upset. Panel sử dụng nền vàng nhạt (`#fff8e1`) với viền vàng để thu hút sự chú ý.

#### Insight chính

- Scatter plot cho thấy mối tương quan yếu giữa chênh lệch ranking và chênh lệch bàn thắng — nhiều trận đấu có khoảng cách ranking lớn nhưng kết quả sát nút hoặc ngược lại.
- Tỷ lệ upset (đội có ranking kém hơn thắng) chiếm một tỷ lệ đáng kể trong tổng số trận đấu, chứng minh rằng bảng xếp hạng FIFA không phải yếu tố quyết định tuyệt đối.
- Lợi thế sân nhà thể hiện rõ: tỷ lệ thắng sân nhà cao hơn đáng kể so với sân trung lập.

### 3.7. Tournament Detail

**Mục tiêu:** Cung cấp giao diện tra cứu chi tiết từng kỳ World Cup, đồng thời dùng World Cup 2022 làm case study minh họa.

![Hình 5. Trang Tournament Detail 2022 — Top 4 cards, biểu đồ bàn ghi và bàn thủng](dashboard_image/detail_1.png)

*Hình 5. Trang Tournament Detail 2022 — Top 4 highlight cards, biểu đồ Goals For và Goals Against.*

#### Thành phần giao diện

**Bộ lọc:**
- Year dropdown (single-select, không xóa được, mặc định 2022): cho phép chọn bất kỳ kỳ World Cup nào từ 1930 đến 2022.
- Nút Apply.

**Top 4 Rank Cards** (4 cards nổi bật):
- 🏆 Champion: tô màu amber.
- Runner-Up: màu xám.
- 3rd Place: màu nâu.
- 4th Place: màu xám nhạt.
- Mỗi card hiển thị: tên đội, số trận, bàn ghi, bàn thủng.

**5 Meta KPI Cards:**
- Host Country: nước chủ nhà.
- Teams: số đội tham dự.
- Matches Played: tổng số trận.
- Total Goals: tổng bàn thắng.
- Avg Goals/Match: bàn thắng trung bình mỗi trận.

**Biểu đồ chính:**

1. **Goals For** — Biểu đồ thanh ngang (`px.bar`, horizontal) hiển thị bàn ghi của từng đội, sắp xếp theo thứ hạng (vị trí 1 ở trên). Màu sắc phân nhóm theo `position_group` (Champion, Top 4, Top 8, Other). Chiều cao 700px để hiển thị rõ ràng 32 đội.

2. **Goals Against** — Tương tự Goals For, nhưng hiển thị bàn thủng.

![Hình 6. Trang Tournament Detail 2022 — Scatter plot GF vs GA](dashboard_image/detail_2.png)

*Hình 6. Trang Tournament Detail 2022 — Scatter plot Goals Scored vs Goals Conceded (Bàn ghi vs Bàn thủng).*

3. **Goals Scored vs Goals Conceded** — Bubble chart (`px.scatter` với `size="Points"`): trục X là bàn ghi (Goals For), trục Y là bàn thủng (Goals Against, trục đảo ngược để hướng tốt lên trên). Kích thước bong bóng tỷ lệ với điểm số. Màu sắc phân theo `position_group`. Đường chéo tham chiếu GF=GA giúp phân biệt đội có hiệu số dương/âm. Nhãn text hiển thị cho các đội Top 8.

**Bảng xếp hạng đầy đủ (DataTable):**

Bảng dữ liệu có thể sắp xếp và phân trang (20 dòng/trang), hiển thị: Position, Team, Games Played, Win, Draw, Loss, Goals For, Goals Against, Goal Difference, Points.

**Insight Panel (chỉ hiển thị khi chọn năm 2022):**

Khi chọn World Cup 2022, một panel narrative bổ sung xuất hiện với 4 insight cards phân tích thành tích của Argentina, France, Croatia và Morocco — 4 đội lọt vào Top 4. Mỗi card bao gồm biểu tượng emoji cờ quốc gia và đoạn văn phân tích ngắn.

#### World Cup 2022 — Case Study

World Cup 2022 là kỳ giải minh họa hoàn hảo cho toàn bộ mạch truyện của dashboard:

- **Argentina** vô địch, đại diện cho nhóm elite truyền thống (CONMEBOL) tiếp tục thống trị ngôi cao nhất.
- **France** (á quân) sở hữu chỉ số tấn công nổi bật nhất giải với 16 bàn thắng trong 7 trận, thể hiện rõ trên biểu đồ Goals For.
- **Croatia** (hạng 3) tiếp tục duy trì phong độ ổn định ở vòng cuối, lần thứ hai liên tiếp lọt vào Top 4.
- **Morocco** (hạng 4) là hiện tượng lịch sử — đội bóng châu Phi đầu tiên lọt vào bán kết World Cup, minh chứng cho tính bất ngờ và sự trỗi dậy của các đội tuyển bên ngoài nhóm elite truyền thống.

#### Insight chính

- Bubble chart GF vs GA giúp phân loại rõ ràng phong cách của từng đội: đội thiên về tấn công (nhiều bàn ghi), đội thiên về phòng ngự (ít bàn thủng), và đội cân bằng.
- Thanh bar so sánh song song Goals For và Goals Against cho phép nhận diện nhanh đội có hiệu suất công/thủ tốt nhất.
- Bảng xếp hạng đầy đủ hỗ trợ tra cứu chi tiết từng chỉ số cho tất cả 32 đội.

---

## 4. Phân tích Insight (Insight Analysis)

### 4.1. Sự mở rộng không ngừng của World Cup

Dữ liệu gần một thế kỷ cho thấy World Cup đã trải qua quá trình tăng trưởng vượt bậc về mọi chỉ số quy mô. Giải đấu năm 1930 tại Uruguay chỉ có 13 đội và 18 trận, nhưng tới năm 2022, con số này đã tăng lên 32 đội và 64 trận. Ba mốc mở rộng quan trọng nhất được ghi nhận qua các annotation trên biểu đồ Timeline Scale: sự trở lại sau Thế chiến thứ hai năm 1950 (sau 12 năm gián đoạn), mở rộng lên 24 đội năm 1982, và mở rộng lên 32 đội năm 1998.

Tuy nhiên, sự mở rộng về quy mô không kéo theo sự tăng trưởng tương ứng về hiệu suất ghi bàn. Biểu đồ Average Goals per Game cho thấy chỉ số này đạt đỉnh ở thập niên 1950 (trên 5 bàn/trận tại World Cup 1954 ở Thụy Sĩ) rồi giảm dần và ổn định quanh mốc 2.5–2.7 bàn/trận từ thập niên 1990 trở đi. Điều này phản ánh sự tiến bộ của chiến thuật phòng ngự và mức độ cạnh tranh đồng đều hơn giữa các đội tuyển ở bóng đá hiện đại.

### 4.2. Quyền lực vô địch vẫn cực kỳ tập trung

Dù World Cup mở rộng về quy mô tham dự, câu hỏi liệu quyền lực có phân tán hơn không nhận được một câu trả lời rõ ràng từ trang Dominance: **chưa hẳn**. Trong suốt 22 kỳ World Cup, chỉ có đúng 9 đội tuyển quốc gia từng giành cúp vàng. Brazil dẫn đầu với 5 danh hiệu, tiếp theo là Germany và Italy với 4 danh hiệu mỗi đội. Điều này có nghĩa là chỉ 3 đội tuyển đã chiếm 13/22 (59%) tổng số chức vô địch.

Sự tập trung này còn thể hiện rõ hơn khi phân tích theo khu vực địa lý. Biểu đồ Top 4 by Continent cho thấy Europe và South America chiếm gần như toàn bộ các vị trí Top 4 trong lịch sử giải đấu. Các châu lục khác — Africa, Asia, North America, Oceania — chỉ có những lần xuất hiện rất hiếm hoi trong nhóm dẫn đầu. Biểu đồ thanh xếp chồng qua các năm cho thấy xu hướng này gần như không thay đổi theo thời gian, dù số đội tham dự đã tăng gấp đôi.

### 4.3. Bóng đá vẫn đầy bất ngờ ở cấp độ trận đấu

Nếu chỉ nhìn vào danh hiệu, World Cup có vẻ như bị chi phối hoàn toàn bởi nhóm elite. Tuy nhiên, phân tích ở cấp độ từng trận đấu qua trang Upsets & Competitiveness cho thấy bức tranh phức tạp hơn nhiều. Scatter plot mối quan hệ giữa chênh lệch ranking FIFA và chênh lệch bàn thắng thực tế cho thấy **mối tương quan yếu** — nhiều trận đấu giữa các đội có khoảng cách ranking rất lớn lại kết thúc với tỷ số sít sao, và ngược lại, một số trận giữa các đội xếp hạng gần nhau lại có kết quả chênh lệch lớn.

Tỷ lệ upset (trận mà đội có ranking kém hơn giành chiến thắng) chiếm một phần đáng kể trong tổng số trận đấu quốc tế, khẳng định rằng bảng xếp hạng FIFA chỉ phản ánh xác suất thắng chứ không phải kết quả chắc chắn. Top 5 upsets với chênh lệch ranking cực lớn cho thấy những đội bị đánh giá thấp hoàn toàn có thể tạo nên cú sốc trước những đội hạng cao.

Ngoài ra, phân tích phân bổ kết quả theo tính chất sân cho thấy lợi thế sân nhà là yếu tố có ý nghĩa thống kê: tỷ lệ thắng sân nhà cao hơn rõ rệt so với tỷ lệ thắng trên sân trung lập. Điều này cung cấp thêm một góc nhìn về tính bất ngờ trong bóng đá — kết quả phụ thuộc vào nhiều yếu tố ngoài năng lực thuần túy được phản ánh qua ranking.

### 4.4. World Cup 2022 — Bức tranh thu nhỏ hoàn hảo

World Cup 2022 tại Qatar minh họa trọn vẹn cả ba chủ đề phân tích. Nhóm đội tuyển elite vẫn chiếm vị trí áp đảo: Argentina đăng quang, France giành á quân với lối chơi tấn công hủy diệt (16 bàn thắng, cao nhất giải), và Croatia lần thứ hai liên tiếp lọt vào Top 4 — tất cả đều đến từ Europe hoặc South America.

Tuy nhiên, câu chuyện đáng chú ý nhất lại đến từ Morocco, đội tuyển châu Phi đầu tiên trong lịch sử lọt vào bán kết World Cup. Trên biểu đồ GF vs GA (Hình 6), Morocco nằm trong góc phần tư "thủ tốt" với chỉ 1 bàn thua (không tính luân lưu) sau 5 trận vòng bảng và vòng knockout. Sự xuất hiện của Morocco trong Top 4 không chỉ là một anomaly (ngoại lệ) đáng ghi nhận, mà còn minh chứng cho insight từ trang Upsets: bóng đá luôn có chỗ cho bất ngờ, ngay cả ở đấu trường cao nhất.

Biểu đồ bubble chart GF vs GA ở kỳ giải 2022 cũng phân tách rõ ràng phong cách chiến thuật của từng đội: France thiên về tấn công (nhiều bàn ghi nhất nhưng cũng thủng lưới nhiều), Morocco thiên về phòng ngự (ít bàn thủng nhất trong Top 8), trong khi Argentina duy trì sự cân bằng hợp lý giữa công và thủ — phong cách phù hợp với một nhà vô địch.

### 4.5. Tổng hợp

Bốn insight trên kết nối với nhau tạo thành một câu chuyện dữ liệu nhất quán: **World Cup đã mở rộng mạnh mẽ về quy mô tổ chức, nhưng sự phân bổ quyền lực vô địch gần như không thay đổi** — vẫn tập trung vào một nhóm nhỏ đội tuyển từ Europe và South America. Tuy nhiên, **ở cấp độ từng trận đấu, bóng đá luôn ẩn chứa tính bất ngờ**, và World Cup 2022 là minh chứng rõ ràng nhất cho sự đan xen giữa truyền thống elite và những outsider quả cảm.

---

<!-- Phase 2: Phần 5–6 sẽ được bổ sung trong giai đoạn tiếp theo -->
