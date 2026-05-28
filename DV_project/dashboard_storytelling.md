# Kế hoạch Storytelling Dashboard: FIFA World Cup và bóng đá quốc tế

## 1. Tổng quan dữ liệu

Dữ liệu trong `DV_project/Data/` có 2 tầng chính:

| Nhóm dữ liệu | Phạm vi | Trường dữ liệu chính | Vai trò trong dashboard |
|---|---:|---|---|
| `archive/FIFA - World Cup Summary.csv` | 22 kỳ World Cup, 1930-2022 | Year, host, champion, runner-up, third place, teams, matches, goals, average goals per game | Phân tích xu hướng dài hạn của World Cup |
| `archive/FIFA - {year}.csv` | Bảng xếp hạng đội tuyển theo từng kỳ World Cup | Position, team, games played, win/draw/loss, goals for/against, goal difference, points | Phân tích thành tích đội tuyển, nhà vô địch, top 4, drilldown năm 2022 |
| `international_matches.csv` | 23,921 trận quốc tế, 1993-08-08 đến 2022-06-14 | Teams, continents, FIFA ranks, scores, tournament, neutral location, shoot-out, result | Phân tích mức độ cạnh tranh, chênh lệch ranking, upset, bộ lọc theo giải đấu |

Một số số liệu nhanh từ dữ liệu local:

- World Cup có 22 kỳ từ 1930 đến 2022.
- File trận quốc tế có 23,921 trận từ 1993 đến 2022.
- Có 88 đội xuất hiện trong các file bảng xếp hạng World Cup.
- Chỉ có 9 đội từng vô địch World Cup.
- Châu Âu có 12 chức vô địch, Nam Mỹ có 10 chức vô địch.
- Brazil là đội vô địch nhiều nhất trong dữ liệu summary: 5 lần.
- Brazil xuất hiện ở toàn bộ 22 kỳ World Cup trong dữ liệu standings.
- Kỳ World Cup có trung bình bàn thắng cao nhất là 1954: 5.4 bàn/trận.
- Kỳ World Cup có trung bình bàn thắng thấp nhất là 1990: 2.2 bàn/trận.
- Đội chủ nhà vô địch 6 lần và vào top 4 trong 13 lượt chủ nhà.
- `international_matches.csv` có 432 trận World Cup hiện đại trong giai đoạn 1994-2022.

## 2. Câu chuyện chính

**Câu hỏi storytelling:** World Cup đã thật sự trở thành một giải đấu toàn cầu, hay chức vô địch vẫn nằm trong tay một nhóm đội tuyển elite?

**Thông điệp chính:** World Cup ngày càng mở rộng về quy mô và phạm vi đại diện, nhưng quyền lực vô địch vẫn tập trung rất mạnh. Giải đấu có nhiều đội hơn, nhiều nước chủ nhà hơn và nhiều trận bất ngờ hơn, nhưng vòng cuối vẫn chủ yếu bị thống trị bởi châu Âu và Nam Mỹ.

## 3. Mạch kể chuyện

### Act 1: World Cup ngày càng lớn hơn

Bắt đầu từ xu hướng cấp giải đấu:

- Số đội tăng từ 13 đội năm 1930 lên 32 đội từ năm 1998 trở đi.
- Số trận tăng khi thể thức giải đấu mở rộng.
- Tổng số bàn thắng tăng theo số trận, nhưng trung bình bàn thắng/trận thay đổi theo từng thời kỳ.

Mục tiêu trực quan: cho người xem thấy quy mô giải đấu trước khi đi vào so sánh đội tuyển.

### Act 2: Lớn hơn không có nghĩa là cân bằng hơn

Chuyển từ quy mô giải đấu sang sự thống trị:

- Chỉ 9 đội từng vô địch trong 22 kỳ World Cup.
- Châu Âu và Nam Mỹ chiếm toàn bộ chức vô địch trong dữ liệu.
- Nhóm quyền lực chính gồm Brazil, Italy, Germany/West Germany, Argentina, France, Uruguay, England và Spain.

Mục tiêu trực quan: làm rõ mức độ tập trung bằng số lần vô địch, số lần vào top 4 và bảng xếp hạng thành tích đội tuyển.

### Act 3: Một trận đấu đơn lẻ vẫn có thể rất khó đoán

Dùng `international_matches.csv` để phân tích tính cạnh tranh ở cấp trận đấu:

- Có thể so sánh chênh lệch FIFA ranking với kết quả thực tế.
- Vẫn có nhiều upset dù chênh lệch ranking lớn.
- Một số ví dụ trong dữ liệu World Cup hiện đại: South Korea thắng Germany năm 2018, Senegal thắng France năm 2002.

Mục tiêu trực quan: cho thấy bóng đá có nhiều bất ngờ ở từng trận, dù chức vô địch cả giải vẫn tập trung.

### Act 4: World Cup 2022 là case study

Dùng bảng xếp hạng World Cup 2022 để kết thúc câu chuyện:

- Argentina vô địch.
- France ghi 16 bàn, cao nhất trong nhóm hai đội đứng đầu năm 2022.
- Morocco xếp hạng 4, thể hiện một lần hiếm hoi đội châu Phi lọt vào top 4 trong dữ liệu standings.

Mục tiêu trực quan: chốt câu chuyện bằng một kỳ World Cup cụ thể, kết nối giữa nhóm elite, hiệu quả tấn công/phòng ngự và sự bứt phá của đội ngoài nhóm truyền thống.

## 4. Bố cục dashboard đề xuất

### Page 1: Executive Overview

Mục đích: cho người xem nắm toàn bộ câu chuyện trong một màn hình.

| Khu vực | Loại biểu đồ | Trường dữ liệu | Insight chính |
|---|---|---|---|
| Hàng KPI trên cùng | KPI cards | Số kỳ World Cup, số đội, số trận, số bàn thắng, số đội từng vô địch | Thiết lập quy mô dữ liệu |
| Khu chính bên trái | Line chart | Year vs teams, matches played, goals scored | Cho thấy World Cup mở rộng theo thời gian |
| Khu chính bên phải | Line chart | Year vs average goals per game | Cho thấy phong cách ghi bàn thay đổi theo thời kỳ |
| Khu dưới | Champion timeline | Year, host, champion | Kết nối lịch sử, chủ nhà và nhà vô địch |
| Cột insight | Text insight cards | Tập trung chức vô địch, tỷ lệ châu Âu/Nam Mỹ | Dẫn dắt câu chuyện |

Bộ lọc nên có:

- Year range.
- Host country.
- Champion.

### Page 2: Dominance and Geography of Success

Mục đích: trả lời câu hỏi đội nào/khu vực nào kiểm soát World Cup.

| Khu vực | Loại biểu đồ | Trường dữ liệu | Insight chính |
|---|---|---|---|
| Bên trái | Horizontal bar chart | Champion, count of titles | Thấy rõ chức vô địch tập trung vào vài đội |
| Ở giữa | Matrix / heatmap | Year, continent của top 4 | Thấy sự thống trị của châu Âu/Nam Mỹ và các ngoại lệ |
| Bên phải | Ranked table | Team, appearances, best position, total goals, total points | Thấy các đội ổn định qua nhiều kỳ, không chỉ đội vô địch |
| Phía dưới | Stacked bar chart | Continent, top 4 count | So sánh sức mạnh khu vực ở giai đoạn cuối |

Bộ lọc nên có:

- Year range.
- Team.
- Continent.
- Position group: champion, top 4, all teams.

### Page 3: Competitiveness and Upsets

Mục đích: cho thấy ranking không dự đoán hoàn toàn kết quả bóng đá.

| Khu vực | Loại biểu đồ | Trường dữ liệu | Insight chính |
|---|---|---|---|
| Hàng KPI trên cùng | KPI cards | Total matches, home win rate, draw rate, neutral match count, shoot-out count | Tóm tắt bối cảnh trận đấu |
| Khu chính | Scatter plot | FIFA rank gap vs goal difference | Quan hệ giữa lợi thế ranking và kết quả |
| Bên phải | Bar chart | Biggest upsets by rank gap | Nêu các trận bất ngờ lớn |
| Dưới trái | Stacked bar | Home result by neutral location | So sánh hiệu ứng sân nhà/sân trung lập |
| Dưới phải | Line chart | Year vs average goals per international match | Xu hướng ghi bàn trong giai đoạn hiện đại |

Bộ lọc nên có:

- Tournament type.
- Team.
- Continent.
- Neutral location.
- Shoot-out.
- Year range.

### Page 4: World Cup 2022 Drilldown

Mục đích: biến câu chuyện thành một ví dụ cụ thể từ kỳ World Cup mới nhất có trong dataset.

| Khu vực | Loại biểu đồ | Trường dữ liệu | Insight chính |
|---|---|---|---|
| Phía trên | Ranking table | Position, team, points, goal difference | Thứ hạng cuối cùng |
| Bên trái | Bar chart | Team vs goals for | So sánh sức tấn công |
| Ở giữa | Bar chart | Team vs goals against | So sánh phòng ngự |
| Bên phải | Scatter plot | Goals for vs goals against, tô màu theo position group | Cân bằng tấn công/phòng ngự |
| Phía dưới | Highlight cards | Argentina, France, Croatia, Morocco | Giải thích vì sao top 4 đáng chú ý |

Bộ lọc nên có:

- Team.
- Position range.
- Minimum games played.

## 5. Chuẩn bị dữ liệu đề xuất

Nên tạo thêm các trường sau trước khi dựng dashboard:

| Field | Nguồn | Mục đích |
|---|---|---|
| `goals_per_game` | `World Cup Summary` | `GOALS SCORED / MATCHES PLAYED`; dùng cho trend chart |
| `team_normalized` | Tất cả file team-level | Gộp khác biệt tên lịch sử như Germany/West Germany nếu báo cáo quyết định xem là cùng một lịch sử bóng đá |
| `continent` | Lookup từ `international_matches.csv` và bảng sửa tay | Phân tích khu vực cho standings World Cup |
| `position_group` | Các file standings World Cup | Champion, top 4, top 8, group/other |
| `goal_difference` | International matches | `home_team_score - away_team_score`; đo mức chênh kết quả trận |
| `rank_gap` | International matches | `home_team_fifa_rank - away_team_fifa_rank`; đo lợi thế ranking |
| `favorite_team` | International matches | Đội có FIFA rank nhỏ hơn trước trận |
| `is_upset` | International matches | Đội thắng có FIFA rank kém hơn đối thủ |
| `upset_rank_gap` | International matches | Độ lớn chênh lệch ranking khi `is_upset = true` |

Lưu ý cleanup:

- Tên đội chưa chuẩn hoàn toàn qua các thời kỳ. Ví dụ Germany và West Germany cần có quyết định xử lý rõ ràng.
- Một số quốc gia lịch sử không còn tồn tại hoặc dùng tên cũ. Nên tạo bảng mapping nhỏ thay vì sửa trực tiếp dữ liệu gốc.
- `international_matches.csv` bắt đầu từ năm 1993, nên phân tích ranking ở cấp trận chỉ nên ghi là phân tích giai đoạn hiện đại, không phải toàn bộ lịch sử World Cup.

## 6. Kỹ thuật trực quan hóa nên áp dụng

| Nội dung trong môn học | Cách áp dụng vào dashboard |
|---|---|
| Data types và encoding | Dùng vị trí trên cùng một thang đo cho goals, points, match counts, rank gaps; dùng màu chủ yếu cho continent, position group hoặc result. |
| Pre-attentive processing | Dùng màu nhấn có kiểm soát cho champion, host team và upset. |
| Chart choice | Line chart cho xu hướng, bar chart cho xếp hạng, scatter plot cho quan hệ ranking/kết quả, table cho tra cứu chi tiết. |
| Layout và Gestalt | Đặt filter nhất quán; nhóm biểu đồ theo câu hỏi; để các chỉ số liên quan gần nhau. |
| Color accessibility | Tránh chỉ dùng đỏ/xanh cho thắng/thua; nên kết hợp màu với label hoặc icon. |
| Interaction | Cho phép filter theo year, team, continent, tournament, neutral location; click vào champion bar/timeline để lọc các chart khác. |
| Storytelling | Đi từ bức tranh lớn, thu hẹp vào sự thống trị, sau đó chỉ ra ngoại lệ/upset, rồi kết thúc bằng case 2022. |

## 7. Tên dashboard đề xuất

Tên khuyến nghị:

**"World Cup Globalization: Bigger Tournament, Same Elite Winners?"**

Tên thay thế:

- **"From Expansion to Dominance: The Data Story of the FIFA World Cup"**
- **"How Global Is the World Cup?"**
- **"World Cup Power Map: Growth, Dominance, and Upsets"**

## 8. Storyline dùng cho phần thuyết trình

1. World Cup phát triển từ một giải đấu nhỏ thành sự kiện toàn cầu với 32 đội.
2. Sự mở rộng làm tăng số đội, số trận và tổng số bàn thắng.
3. Tuy vậy, chức vô địch vẫn chỉ tập trung ở 9 đội.
4. Châu Âu và Nam Mỹ vẫn thống trị chức vô địch và top 4.
5. Dữ liệu cấp trận cho thấy vẫn có nhiều upset và bất ngờ trong giai đoạn hiện đại.
6. World Cup 2022 minh họa cả hai mặt: Argentina và France đại diện cho nhóm elite, còn Morocco cho thấy cơ hội bứt phá của đội ngoài nhóm truyền thống.

## 9. Phạm vi build đầu tiên

Để làm dashboard khả thi trong giai đoạn đầu, nên dựng trước 4 visual:

1. Line chart mở rộng World Cup: teams, matches, goals theo year.
2. Bar chart số lần vô địch theo champion.
3. Heatmap hoặc stacked bar top 4 theo continent.
4. Scatter plot World Cup 2022: goals for vs goals against.

Sau đó mới bổ sung phân tích ranking/upset từ `international_matches.csv`.
