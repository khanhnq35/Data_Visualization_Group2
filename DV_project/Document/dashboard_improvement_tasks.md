# Kế hoạch Thực thi Cải tiến Dashboard

> **Phiên bản:** 1.0 | **Ngày:** 02/06/2026  
> **Dự án:** FIFA World Cup Dashboard — `DV_project/`  
> **Dựa trên:** `dashboard_visualization_improvement_plan.md`  
> **Nguyên tắc cốt lõi:** Tiêu đề ngắn gọn, mô tả đúng nội dung. Insight phải tự hiện ra qua **design của biểu đồ** (annotation, highlight màu, reference line, thứ tự sắp xếp) — không phải qua tiêu đề dài hay text giải thích.

---

## 1. Tóm tắt Kế hoạch

Dashboard FIFA World Cup hiện tại đã có kiến trúc tốt, hệ thống màu nhất quán, và logic tương tác cơ bản hoạt động đúng. Tuy nhiên, phân tích chi tiết code phát hiện một số vấn đề cần giải quyết trước khi nộp:

**Vấn đề CVD (Color Vision Deficiency) — đã được sửa một phần trong code hiện tại:**
- `upsets.py` dòng 12–15: `COLOR_UPSET = "#f97316"` (orange), `COLOR_HOME = "#1d4ed8"` (blue) — đã CVD-safe.
- `tournament.py` dòng 64: `POS_COLORS["Top 8"] = "#7c3aed"` (purple) — đã CVD-safe.
- Tuy nhiên cần **kiểm tra lại baseline** để xác nhận những thay đổi này hoạt động đúng trên giao diện thực tế.

**Vấn đề tiêu đề và storytelling — đã được cải thiện một phần:**
- Nhiều tiêu đề đã được Việt hóa và mang tính mô tả (ví dụ: `_scale_figure()` dùng title "Từ 13 lên 32 Đội: Cuộc Bành Trướng 92 Năm của World Cup").
- Tuy nhiên, một số tiêu đề vẫn còn dài, và quan trọng hơn, **insight phải tự hiện ra qua thiết kế biểu đồ** (annotation trực tiếp, highlight màu, reference line) thay vì nằm trong title.

**Vấn đề annotation và reference line:**
- `_scale_figure()`: Đã có annotation tại 1998, cần bổ sung annotation tại điểm đỉnh/đáy goals.
- `_avg_goals_figure()`: Đã có annotation tại max/min, nhưng màu đường (`COLORS["accent_3"]` = đỏ) không phù hợp cho xu hướng trung tính.
- `tournament-scatter-chart`: Đã có đường diagonal GF=GA — kiểm tra lại xem đã hiển thị đúng chưa.

**Vấn đề highlight và pop-out:**
- `dominance-champion-bar`: Tất cả bars vẫn cùng màu teal — thiếu highlight Brazil với màu amber đậm.
- `overview-champion-timeline`: Đã tách legend, nhưng cần annotation "5 lần" cho Brazil.

**Insight Cards:**
- `overview.py` và `dominance.py` đã có `.insight-card` trong layout.
- `upsets.py` cũng đã có `.insight-card`.
- Cần kiểm tra nội dung có đủ ngắn gọn và đúng storytelling không.

---

## 2. Tổng quan Các Giai đoạn

| Giai đoạn | Tên | Ưu tiên | Ước lượng | Phụ thuộc |
|---|---|---|---|---|
| Phase 0 | Kiểm tra baseline — chạy app, chụp màn hình hiện trạng | P0 | 30 phút | Không có |
| Phase 1 | Sửa màu CVD-safe và shared style | P0 | 45 phút | Phase 0 |
| Phase 2 | Chuẩn hóa tiêu đề và insight cards | P0 | 60 phút | Phase 1 |
| Phase 3 | Cải thiện trang Overview | P1 | 90 phút | Phase 1, 2 |
| Phase 4 | Cải thiện trang Dominance | P1 | 90 phút | Phase 1, 2 |
| Phase 5 | Cải thiện trang Upsets | P1 | 60 phút | Phase 1, 2 |
| Phase 6 | Cải thiện trang Tournament Detail | P1 | 60 phút | Phase 1, 2 |
| Phase 7 | Polish tương tác và usability | P2 | 90 phút | Phase 3–6 |
| Phase 8 | QA cuối, chụp màn hình, căn chỉnh báo cáo | P0 | 60 phút | Phase 3–7 |
| Phase 9 | Tùy chọn / Bonus (P3) | P3 | Tùy chọn | Phase 8 |

---

## 3. Chi tiết Task theo Giai đoạn

---

### Phase 0 — Kiểm tra Baseline

#### Task 0.1 — Chạy app và xác nhận trạng thái hiện tại

**Ưu tiên:** P0  
**Loại:** QA  
**Liên quan plan:** "Checklist Kỹ thuật — NO CRASH: Chạy `python app.py` không lỗi, chuyển 4 trang không callback error"  
**File/component ảnh hưởng:** `app.py`, tất cả 4 trang  
**Mục tiêu:** Xác nhận app chạy được trước khi bắt đầu sửa, ghi nhận baseline để so sánh sau khi cải tiến.

**Các bước thực hiện:**
1. Chạy `python app.py` từ thư mục `DV_project/`.
2. Mở trình duyệt tại `http://127.0.0.1:8050`.
3. Điều hướng qua 4 trang: Overview, Dominance, Upsets, Tournament Detail.
4. Ghi lại bất kỳ lỗi console hoặc callback exception nào.
5. Chụp màn hình 4 trang ở trạng thái mặc định.
6. Kiểm tra màu sắc hiện tại: xác nhận `COLOR_UPSET` trong `upsets.py` là `"#f97316"` (orange), `POS_COLORS["Top 8"]` trong `tournament.py` là `"#7c3aed"` (purple).

**Tiêu chí chấp nhận:**
- [x] App khởi động không có exception.
- [x] Cả 4 trang render không có lỗi callback.
- [x] Trang Tournament mặc định hiển thị năm 2022.
- [x] Màu CVD-safe đã được áp dụng (orange cho upset, purple cho Top 8).

**Bước kiểm tra:** Mở browser console (F12), kiểm tra không có lỗi đỏ. Kiểm tra Network tab không có failed requests.

**Ghi chú / rủi ro:** Nếu `POS_COLORS["Top 8"]` hoặc `COLOR_UPSET` chưa là giá trị CVD-safe, ghi nhận và thực hiện ngay Task 1.1.

---

#### Task 0.2 — Kiểm tra `.insight-card` hiển thị đúng trên 4 trang

**Ưu tiên:** P0  
**Loại:** QA  
**Liên quan plan:** "Thêm Insight Card text block đầu mỗi trang — Thêm `html.Div(className='insight-card', ...)` vào layout của Overview, Dominance, Upsets"  
**File/component ảnh hưởng:** `pages/overview.py` dòng 74–83, `pages/dominance.py` dòng 143–148, `pages/upsets.py` dòng 113–124, `assets/styles.css` dòng 304–316  
**Mục tiêu:** Xác nhận `.insight-card` component hiển thị đúng style trên cả 3 trang (Overview, Dominance, Upsets). Tournament không cần insight card vì đã có 2022 insight panel.

**Các bước thực hiện:**
1. Mở từng trang và tìm insight card ngay dưới filter panel.
2. Kiểm tra visual: nền `#eef4f5`, border-left 4px solid teal (`#007c89`), font-size 14px.
3. Đọc nội dung text: xác nhận 3 trang có nội dung đúng theo storytelling arc.
4. Kiểm tra trang Tournament: KHÔNG có insight card — thay vào đó có 2022 panel ở cuối trang.

**Tiêu chí chấp nhận:**
- [x] Overview: "Sau 92 năm, World Cup đã mở rộng từ **13 lên 32 đội**..."
- [x] Dominance: "**Chỉ 9 đội chia nhau 22 chức vô địch.**..."
- [x] Upsets: "Dữ liệu **23,921 trận quốc tế**..."
- [x] CSS `.insight-card` hiển thị đúng màu và border.

**Bước kiểm tra:** Chụp màn hình insight card từng trang, so sánh với thiết kế mong muốn.

**Ghi chú / rủi ro:** Nếu CSS `insight-card` không hiển thị đúng (ví dụ: border không thấy), kiểm tra xem `assets/styles.css` có được load đúng không.

---

### Phase 1 — Sửa màu CVD-safe và Shared Style

#### Task 1.1 — Xác nhận và sửa POS_COLORS trong tournament.py

**Ưu tiên:** P0 — Khẩn cấp  
**Loại:** Bugfix / Accessibility  
**Liên quan plan:** "[KHẨN CẤP — CVD] Sửa POS_COLORS trong `tournament.py` — Đổi `'Top 8': COLORS['success']` (`#2f855a` xanh lá) sang `'Top 8': '#7c3aed'` (purple). Ảnh hưởng: `tournament-goals-for-chart`, `tournament-goals-against-chart`, `tournament-scatter-chart`."  
**File/component ảnh hưởng:** `pages/tournament.py` dòng 61–66 (`POS_COLORS` dict)  
**Mục tiêu:** Đảm bảo cặp màu xanh lá (`#2f855a`) và đỏ (`#c44536`) không xuất hiện cùng nhau, vi phạm CVD (Color Vision Deficiency) cho người mù màu Protanopia/Deuteranopia (8% nam giới).

**Các bước thực hiện:**
1. Mở `pages/tournament.py`, tìm `POS_COLORS` dict (dòng 61–66).
2. Xác nhận giá trị hiện tại:
   ```python
   POS_COLORS = {
       "Champion": COLORS["accent_2"],   # amber #d98324
       "Top 4":    COLORS["accent"],     # teal #007c89
       "Top 8":    "#7c3aed",            # purple — CVD-safe
       "Other":    COLORS["muted"],      # grey #64727d
   }
   ```
3. Nếu `"Top 8"` vẫn là `COLORS["success"]` (`#2f855a`), đổi sang `"#7c3aed"`.
4. Lưu file, reload app, kiểm tra Tournament 2022 — xác nhận không còn màu xanh lá trong bar charts và scatter.

**Tiêu chí chấp nhận:**
- [x] `POS_COLORS["Top 8"]` = `"#7c3aed"` (không phải `COLORS["success"]`).
- [x] Trang Tournament 2022: bar chart GF và GA không có màu xanh lá.
- [x] Scatter chart: 4 nhóm (Champion/amber, Top4/teal, Top8/purple, Other/grey) phân biệt rõ.

**Bước kiểm tra:** Mở Tournament 2022. Kiểm tra legend của scatter chart — xác nhận "Top 8" hiện màu tím (`#7c3aed`).

**Ghi chú / rủi ro:** `POS_COLORS` được dùng ở cả 3 chart trong tournament (GF bar, GA bar, scatter). Thay đổi `POS_COLORS` ảnh hưởng đồng thời cả 3 chart — đây là điều mong muốn.

---

#### Task 1.2 — Xác nhận màu CVD-safe trong upsets.py

**Ưu tiên:** P0 — Khẩn cấp  
**Loại:** Bugfix / Accessibility  
**Liên quan plan:** "[KHẨN CẤP — CVD] Sửa màu Upset trong `upsets.py` — `COLOR_UPSET = '#f97316'` (orange). [KHẨN CẤP — CVD] Sửa màu trong neutral_result chart — `COLOR_HOME = '#1d4ed8'` (blue), `COLOR_AWAY = '#f97316'` (orange)."  
**File/component ảnh hưởng:** `pages/upsets.py` dòng 12–16  
**Mục tiêu:** Đảm bảo trang Upsets dùng bảng màu Blue-Orange thay vì Red-Green hoặc Red-Gray.

**Các bước thực hiện:**
1. Mở `pages/upsets.py`, kiểm tra dòng 12–16:
   ```python
   COLOR_UPSET  = "#f97316"   # orange — CVD-safe
   COLOR_NORMAL = "#94a3b8"   # grey
   COLOR_HOME   = "#1d4ed8"   # blue — CVD-safe
   COLOR_AWAY   = "#f97316"   # orange — CVD-safe
   COLOR_DRAW   = "#cbd5e1"   # grey nhạt
   ```
2. Nếu bất kỳ giá trị nào vẫn là đỏ (`#c44536`) hoặc xanh lá (`#2f855a`), đổi theo bảng trên.
3. Reload app, kiểm tra scatter plot: upset points phải là màu cam nổi bật trên nền xám.
4. Kiểm tra stacked bar: Home Win = xanh dương, Away Win = cam, Draw = xám nhạt.

**Tiêu chí chấp nhận:**
- [x] `COLOR_UPSET = "#f97316"` (orange).
- [x] `COLOR_HOME = "#1d4ed8"` (blue).
- [x] `COLOR_AWAY = "#f97316"` (orange).
- [x] Scatter plot: Điểm cam (upset) nổi bật rõ trên nền xám.
- [x] Stacked bar: 3 màu phân biệt rõ, Blue/Orange/LightGray.

**Bước kiểm tra:** Mở Upsets page. Chụp màn hình scatter plot và stacked bar. Xác nhận không có màu đỏ.

**Ghi chú / rủi ro:** `COLOR_HOME` và `COLOR_AWAY` đều là orange (`#f97316`) — đây là thiết kế hiện tại. Nếu cần phân biệt Home và Away rõ hơn, có thể đổi `COLOR_AWAY` sang `#ea580c` (orange đậm hơn) nhưng không bắt buộc.

---

#### Task 1.3 — Kiểm tra màu đường _avg_goals_figure trong overview.py

**Ưu tiên:** P1  
**Loại:** Visualization  
**Liên quan plan:** "Đổi màu đường sang `COLORS['accent']` (teal) — màu trung tính, không gây liên tưởng cảnh báo"  
**File/component ảnh hưởng:** `pages/overview.py`, hàm `_avg_goals_figure()` dòng 187–236, `go.Scatter` trace  
**Mục tiêu:** Đường avg goals/game hiện dùng `COLORS["accent_3"]` (đỏ `#c44536`) — màu này gây liên tưởng "cảnh báo/nguy hiểm" không phù hợp với xu hướng trung tính. Đổi sang teal để nhất quán với tông màu chung.

**Các bước thực hiện:**
1. Mở `pages/overview.py`, tìm hàm `_avg_goals_figure()`.
2. Tìm dòng `line={"width": 3, "color": COLORS["accent_3"]}` (khoảng dòng 200).
3. Đổi `COLORS["accent_3"]` thành `COLORS["accent"]` (teal `#007c89`).
4. Reload app, kiểm tra trang Overview — đường avg goals phải là màu teal.

**Tiêu chí chấp nhận:**
- [x] Đường avg goals/game là màu teal (`#007c89`), không phải đỏ.
- [x] Đường hline trung bình vẫn là `COLORS["muted"]` (xám).

**Bước kiểm tra:** Mở Overview, cuộn đến chart avg goals. Xác nhận màu đường là teal.

**Ghi chú / rủi ro:** Thay đổi đơn giản, không ảnh hưởng logic. Chỉ cần sửa 1 dòng trong 1 hàm.

---

### Phase 2 — Chuẩn hóa Tiêu đề và Insight Cards

#### Task 2.1 — Chuẩn hóa tiêu đề biểu đồ — trang Overview

**Ưu tiên:** P0  
**Loại:** Visualization / Storytelling  
**Liên quan plan:** "[P0] Chuẩn hóa tiêu đề biểu đồ — Ngắn gọn, mô tả đúng nội dung, không cần chứa insight. Insight phải tự hiện ra qua design: annotation, highlight màu, reference line, thứ tự sắp xếp."  
**File/component ảnh hưởng:** `pages/overview.py`, ba hàm `_scale_figure()`, `_avg_goals_figure()`, `_champion_timeline_figure()`  
**Mục tiêu:** Tiêu đề phải ngắn (tối đa 8 từ tiếng Việt), mô tả đúng nội dung, để trống không gian cho insight tự hiện ra qua annotation và highlight màu trực tiếp trên biểu đồ.

**Các bước thực hiện:**

Cho `_scale_figure()` (dòng ~163):
1. Tiêu đề hiện tại: "Từ 13 lên 32 Đội: Cuộc Bành Trướng 92 Năm của World Cup" — quá dài (12 từ).
2. Đổi thành: `"Quy mô World Cup theo năm (1930–2022)"`.
3. Insight về "mở rộng lên 32 đội" đã có annotation trực tiếp tại 1998 — đó là nơi insight thuộc về, không phải title.

Cho `_avg_goals_figure()` (dòng ~233):
1. Tiêu đề hiện tại: "Bàn Thắng/Trận: Đỉnh cao 1954, Đáy thấp 1990 — Xu hướng hiện đại ổn định" — quá dài.
2. Đổi thành: `"Trung bình bàn thắng / trận"`.
3. Insight về 1954 và 1990 đã có annotation trực tiếp — đó là nơi insight thuộc về.

Cho `_champion_timeline_figure()` (dòng ~282):
1. Tiêu đề hiện tại: "8 Triều Đại Thống Trị: Ai Sở Hữu Chiếc Cúp Vàng Suốt 92 Năm?" — quá dài.
2. Đổi thành: `"Lịch sử nhà vô địch World Cup (1930–2022)"`.
3. Insight về số lần vô địch sẽ có từ annotation và hover tooltip.

**Tiêu chí chấp nhận:**
- [x] `_scale_figure()`: title ≤ 8 từ, không có dấu chấm than hoặc câu hỏi.
- [x] `_avg_goals_figure()`: title ≤ 6 từ tiếng Việt.
- [x] `_champion_timeline_figure()`: title ≤ 8 từ, có năm phạm vi.
- [x] Tất cả annotations trên chart vẫn hoạt động đúng sau khi đổi title.

**Bước kiểm tra:** Reload trang Overview, đọc tiêu đề 3 chart — kiểm tra không có tiêu đề dài quá 10 từ.

**Ghi chú / rủi ro:** Không thay đổi logic biểu đồ, chỉ thay đổi chuỗi `title=`. Rủi ro rất thấp.

---

#### Task 2.2 — Chuẩn hóa tiêu đề biểu đồ — trang Dominance

**Ưu tiên:** P0  
**Loại:** Visualization / Storytelling  
**Liên quan plan:** "Tiêu đề ngắn chuẩn cho champion bar chart, top4 stacked bar, goals bar chart."  
**File/component ảnh hưởng:** `pages/dominance.py`, hàm `update_dominance()` dòng 300–415  
**Mục tiêu:** Đồng nhất tiêu đề các chart trang Dominance — ngắn, mô tả rõ, để insight tự hiện qua màu sắc và thứ tự sắp xếp.

**Các bước thực hiện:**

Cho `dominance-champion-bar` (dòng ~344):
1. Tiêu đề hiện tại: "Bức Tường Pha Lê: 9 Đội Chia Nhau 22 Chức Vô Địch Trong 92 Năm" — quá dài.
2. Đổi thành: `"Số lần vô địch theo đội"`.
3. Insight "9 đội chia nhau 22 danh hiệu" đã có trong `.insight-card` phía trên.

Cho `dominance-top4-by-continent` (dòng ~370):
1. Tiêu đề hiện tại: "Châu Âu & Nam Mỹ: Hai Đại Lục Thống Trị Các Suất Top 4" — quá dài.
2. Đổi thành: `"Số suất Top 4 theo châu lục qua các kỳ"`.
3. Insight về EU và SA tự hiện ra qua màu sắc stacked bar.

Cho `dominance-goals-for-chart` (dòng ~394):
1. Tiêu đề hiện tại: "Sức Mạnh Ghi Bàn Tích Lũy: Top 20 Đội Nhiều Bàn Nhất Lịch Sử" — quá dài.
2. Đổi thành: `"Tổng bàn thắng — Top 20 đội (lịch sử)"`.

**Tiêu chí chấp nhận:**
- [x] `dominance-champion-bar`: title ≤ 6 từ.
- [ ] `dominance-top4-by-continent`: title ≤ 8 từ.
- [x] `dominance-goals-for-chart`: title ≤ 8 từ.

**Bước kiểm tra:** Reload trang Dominance, kiểm tra 3 chart titles.

**Ghi chú / rủi ro:** Hàm `update_dominance()` là callback — đổi title trong callback body, không trong layout.

---

#### Task 2.3 — Chuẩn hóa tiêu đề biểu đồ — trang Upsets

**Ưu tiên:** P0  
**Loại:** Visualization / Storytelling  
**Liên quan plan:** "Tiêu đề ngắn chuẩn cho scatter, top upsets bar, neutral stacked bar."  
**File/component ảnh hưởng:** `pages/upsets.py`, ba hàm `_scatter_figure()`, `_top_upsets_figure()`, `_neutral_result_figure()`  
**Mục tiêu:** Tiêu đề ngắn, mô tả đúng nội dung. Insight tự hiện qua màu cam (upset) nổi bật trên nền xám.

**Các bước thực hiện:**

Cho `_scatter_figure()` (dòng ~281):
1. Tiêu đề hiện tại: "Đội Yếu Hơn Vẫn Thắng: Hạng FIFA Không Quyết Định Tất Cả" — quá dài.
2. Đổi thành: `"Chênh lệch hạng FIFA vs chênh lệch bàn thắng"`.
3. Insight "đội yếu vẫn thắng" tự hiện qua các điểm cam phân tán ở mọi vùng rank gap.

Cho `_top_upsets_figure()` (dòng ~319):
1. Tiêu đề hiện tại: "5 Cú Sốc Lớn Nhất: Khi Đội Yếu Đánh Bại Người Khổng Lồ" — quá dài.
2. Đổi thành: `"Top 5 upset lớn nhất theo chênh lệch hạng"`.

Cho `_neutral_result_figure()` (dòng ~364):
1. Tiêu đề hiện tại: "Lợi Thế Sân Nhà Biến Mất ở Sân Trung Lập — Tỷ Lệ Thắng Giảm Rõ Rệt" — quá dài.
2. Đổi thành: `"Kết quả trận theo loại địa điểm thi đấu"`.
3. Insight về "lợi thế sân nhà giảm" tự hiện qua annotation "Tổng: X trận" và chiều cao các phân đoạn màu.

**Tiêu chí chấp nhận:**
- [x] `_scatter_figure()`: title ≤ 8 từ.
- [x] `_top_upsets_figure()`: title ≤ 8 từ.
- [x] `_neutral_result_figure()`: title ≤ 8 từ.

**Bước kiểm tra:** Reload trang Upsets, kiểm tra 3 chart titles.

**Ghi chú / rủi ro:** Không thay đổi logic, chỉ đổi chuỗi `title=`. Rủi ro thấp.

---

#### Task 2.4 — Chuẩn hóa tiêu đề biểu đồ — trang Tournament

**Ưu tiên:** P0  
**Loại:** Visualization / Storytelling  
**Liên quan plan:** "Tiêu đề ngắn chuẩn: 'Bàn ghi được — {year}' và 'Bàn thủng lưới — {year}', 'Bàn ghi vs bàn thủng — {year}'"  
**File/component ảnh hưởng:** `pages/tournament.py`, hàm `update_all()` dòng 287–444  
**Mục tiêu:** Tiêu đề chart tournament dynamic (theo năm) phải ngắn gọn, rõ năm.

**Các bước thực hiện:**

Cho Goals For chart (dòng ~327):
1. Tiêu đề hiện tại: `f"Bàn ghi được — {year}"` — đã đúng.
2. Giữ nguyên.

Cho Goals Against chart (dòng ~349):
1. Tiêu đề hiện tại: `f"Bàn thủng lưới — {year}  (ít hơn = tốt hơn)"` — hơi dài nhưng có thông tin hữu ích.
2. Cân nhắc giữ nguyên "(ít hơn = tốt hơn)" vì đây là hướng dẫn đọc chart quan trọng, hoặc rút ngắn thành `f"Bàn thủng lưới — {year}"` và thêm annotation "Ít hơn = phòng ngự tốt hơn" trực tiếp trên chart.
3. Nếu đổi, thêm annotation: `fig_ga.add_annotation(x=0, y=1.05, xref="paper", yref="paper", text="Ít hơn = phòng ngự tốt hơn", showarrow=False, font={"size":10, "color": COLORS["muted"]})`.

Cho Scatter chart (dòng ~379):
1. Tiêu đề hiện tại: `f"Bàn ghi vs Bàn thủng — {year}"` — đổi từ 'Tấn công vs Phòng ngự' theo yêu cầu người dùng.
2. Cập nhật.

**Tiêu chí chấp nhận:**
- [x] Goals For: title có năm, ≤ 6 từ.
- [x] Goals Against: title có năm và gợi ý đọc chart, hoặc annotation thay thế.
- [x] Scatter: title có năm, ≤ 6 từ.

**Bước kiểm tra:** Chọn năm 2022 và năm 1930 — kiểm tra title thay đổi đúng theo năm.

**Ghi chú / rủi ro:** Tất cả 3 chart trong tournament dùng dynamic title theo `year`. Đảm bảo f-string đúng cú pháp sau khi chỉnh sửa.

---

### Phase 3 — Cải thiện trang Overview

#### Task 3.1 — Bổ sung annotation chiến lược cho _scale_figure

**Ưu tiên:** P1  
**Loại:** Visualization / Storytelling  
**Liên quan plan:** "Annotation tại 1998 trên subplot Teams: '32 đội' với mũi tên → người xem tự thấy bước nhảy. Annotation tại năm có bàn thắng cao nhất và thấp nhất trên subplot Goals."  
**File/component ảnh hưởng:** `pages/overview.py`, hàm `_scale_figure()` dòng 130–184  
**Mục tiêu:** Người xem nhìn vào Scale Chart phải thấy ngay mốc 1998 (32 đội) và điểm bước ngoặt về tổng bàn thắng, không cần đọc title hay text bên ngoài.

**Các bước thực hiện:**
1. Trong hàm `_scale_figure()`, sau khi đã add 3 traces, xác nhận đoạn code annotation tại 1998 (dòng 169–182) đang hoạt động đúng:
   - Annotation trên subplot row=1 (Teams): "1998: Mở rộng lên 32 đội".
   - Annotation trên subplot row=2 (Matches): "64 trận từ 1998".
2. Thêm annotation trên subplot Goals (row=3) tại năm có tổng bàn cao nhất:
   ```python
   idx_max_goals = df["goals_scored"].idxmax()
   yr_goals_max = df.loc[idx_max_goals, "year"]
   val_goals_max = df.loc[idx_max_goals, "goals_scored"]
   if yr_goals_max in df["year"].values:
       fig.add_annotation(
           x=yr_goals_max, y=val_goals_max,
           text=f"{yr_goals_max}: {int(val_goals_max)} bàn",
           showarrow=True, arrowhead=2, ax=50, ay=-30,
           font={"size": 10, "color": COLORS["muted"]},
           row=3, col=1,
       )
   ```
3. Highlight marker tại năm 1998 trên subplot Teams bằng size lớn hơn:
   - Thay `marker={"size": 7}` thành marker size theo điều kiện: `[12 if y == 1998 else 7 for y in df["year"]]`.
   - Lưu ý: cần dùng `go.Scatter` với `marker={"size": [...],...}` thay vì constant size.

**Tiêu chí chấp nhận:**
- [x] Annotation "1998: Mở rộng lên 32 đội" hiển thị trên subplot Teams với mũi tên.
- [x] Annotation "64 trận từ 1998" hiển thị trên subplot Matches.
- [x] Annotation tổng bàn thắng cao nhất hiển thị trên subplot Goals.
- [x] Marker tại 1998 trên Teams lớn hơn các năm khác (size 12 vs 7).
- [x] Không có lỗi khi filter chọn khoảng năm không bao gồm 1998.

**Bước kiểm tra:** Mở Overview với bộ lọc mặc định (1930–2022). Kiểm tra 3 annotation xuất hiện đúng vị trí. Thử filter 2000–2022 — annotation 1998 không được xuất hiện (vì check `if 1998 in df["year"].values`).

**Ghi chú / rủi ro:** Annotation trong subplot Plotly cần tham số `row=X, col=1`. Nếu quên tham số này, annotation sẽ xuất hiện sai vị trí hoặc không hiện. Kiểm tra kỹ syntax.

---

#### Task 3.2 — Cải thiện champion timeline — legend và annotation Brazil

**Ưu tiên:** P1–P2  
**Loại:** Visualization / Storytelling  
**Liên quan plan:** "Bật legend rõ ràng: 'Chủ nhà vô địch ★' / 'Đội khách vô địch ●'. Annotation trực tiếp tại hàng Brazil: '5 lần vô địch'. Dùng symbol='star' cho host thắng."  
**File/component ảnh hưởng:** `pages/overview.py`, hàm `_champion_timeline_figure()` dòng 239–288  
**Mục tiêu:** Người xem nhìn vào champion timeline phải thấy ngay: (1) Brazil có nhiều chức vô địch nhất qua annotation "5 lần", (2) Phân biệt chủ nhà vô địch vs đội khách qua legend.

**Các bước thực hiện:**
1. Xác nhận code hiện tại đã dùng `symbol="star"` cho host_won và `symbol="circle"` cho đội khách (dòng 249–251). Đây đã là thiết kế tốt.
2. Xác nhận `showlegend=True` (dòng 283). Đây đã đúng.
3. Thêm annotation "5 lần" bên cạnh hàng Brazil nếu Brazil có trong data:
   ```python
   brazil_rows = df[df["champion_norm"] == "Brazil"]
   if not brazil_rows.empty:
       last_brazil_year = brazil_rows["year"].max()
       fig.add_annotation(
           x=last_brazil_year + 2,
           y="Brazil",
           text="5 lần",
           showarrow=False,
           font={"size": 11, "color": COLORS["accent_2"], "weight": 700},
           xanchor="left",
       )
   ```
4. Kiểm tra annotation không bị cắt ở cạnh chart — nếu cần, tăng `margin={"r": 60}`.

**Tiêu chí chấp nhận:**
- [x] Legend hiển thị "Chủ nhà vô địch" (star symbol) và "Đội khách vô địch" (circle).
- [x] Annotation "5 lần" xuất hiện bên phải hàng Brazil.
- [x] Annotation không bị cắt (xanchor="left", đủ margin phải).
- [x] Khi filter không bao gồm Brazil, annotation không xuất hiện.

**Bước kiểm tra:** Mở Overview mặc định. Kiểm tra legend timeline. Zoom vào hàng Brazil — annotation "5 lần" phải hiển thị rõ.

**Ghi chú / rủi ro:** Annotation dùng `y="Brazil"` — phải đảm bảo tên đúng chính xác với giá trị trong `champion_norm`. Nếu `champion_norm` dùng tên khác (ví dụ "Brazil ★"), cần điều chỉnh.

---

### Phase 4 — Cải thiện trang Dominance

#### Task 4.1 — Highlight Brazil trong champion bar chart

**Ưu tiên:** P1  
**Loại:** Visualization / Storytelling  
**Liên quan plan:** "Highlight Brazil bằng màu amber đậm, các đội khác muted gray — người xem thấy ngay đội nhiều nhất mà không đọc trục. Annotation trực tiếp bên phải bar Brazil: '5 lần'."  
**File/component ảnh hưởng:** `pages/dominance.py`, hàm `update_dominance()` dòng 333–353 (phần tạo `champion_fig`)  
**Mục tiêu:** Pop-out effect — Brazil (5 lần vô địch) phải nổi bật ngay lập tức qua màu amber đậm, các đội khác fade thành xám. Người xem thấy ngay "ai nhiều nhất" mà không cần đọc số.

**Các bước thực hiện:**
1. Trong `update_dominance()`, sau khi tính `champion_counts`, tạo cột màu:
   ```python
   # Tạo cột màu cho highlight
   max_team = champion_counts.loc[champion_counts["titles"].idxmax(), "Team"] if not champion_counts.empty else ""
   champion_counts["bar_color"] = champion_counts["Team"].apply(
       lambda t: COLORS["accent_2"] if t == max_team else "#cbd5e1"
   )
   ```
2. Đổi từ `color_discrete_sequence=[COLORS["accent"]]` sang dùng `color="bar_color"` với `color_discrete_map`:
   ```python
   champion_fig = px.bar(
       champion_counts.tail(20),
       x="titles", y="Team", orientation="h",
       title="Số lần vô địch theo đội",
       labels={"titles": "Số lần vô địch", "Team": ""},
       color="bar_color",
       color_discrete_map={COLORS["accent_2"]: COLORS["accent_2"], "#cbd5e1": "#cbd5e1"},
   )
   champion_fig.update_layout(showlegend=False)
   ```
   Hoặc đơn giản hơn, dùng `marker_color`:
   ```python
   champion_fig = px.bar(champion_counts.tail(20), x="titles", y="Team", orientation="h", title="Số lần vô địch theo đội")
   colors = [COLORS["accent_2"] if t == max_team else "#cbd5e1" for t in champion_counts.tail(20)["Team"]]
   champion_fig.update_traces(marker_color=colors)
   ```
3. Thêm annotation bên phải bar của max_team:
   ```python
   max_titles = int(champion_counts["titles"].max())
   champion_fig.add_annotation(
       x=max_titles, y=max_team,
       text=f"{max_titles} lần",
       showarrow=False, xanchor="left", xshift=6,
       font={"size": 12, "color": COLORS["accent_2"], "weight": 700},
   )
   ```
4. Reload app — kiểm tra chart: đội nhiều nhất (thường là Brazil) phải có màu amber nổi bật.

**Tiêu chí chấp nhận:**
- [x] Đội có số lần vô địch nhiều nhất (Brazil = 5) có màu amber (`#d98324`).
- [x] Tất cả đội khác có màu xám nhạt (`#cbd5e1`).
- [x] Annotation "5 lần" xuất hiện bên phải bar Brazil.
- [x] Khi filter thay đổi (ví dụ: chỉ xem châu Âu), đội khác (Germany = 4) trở thành amber.
- [x] Legend ẩn (`showlegend=False`).

**Bước kiểm tra:** Mở Dominance mặc định. Xác nhận bar Brazil màu amber. Dùng filter chọn chỉ châu Âu — Germany phải trở thành amber.

**Ghi chú / rủi ro:** Đây là callback — `max_team` được tính động trong mỗi lần callback triggered. Nếu `champion_counts` rỗng (không có nhà vô địch trong filter), phải handle edge case (`if not champion_counts.empty`).

---

#### Task 4.2 — Thêm vrect phân tách giai đoạn lịch sử trong stacked bar continent

**Ưu tiên:** P2  
**Loại:** Visualization / Storytelling  
**Liên quan plan:** "Vrect phân tách giai đoạn thể thức (13/16/24/32 đội) → người xem thấy pattern thay đổi theo thời kỳ. `fig.add_vrect(x0=1930, x1=1950, fillcolor=..., opacity=0.05)`"  
**File/component ảnh hưởng:** `pages/dominance.py`, hàm `update_dominance()` dòng 355–377 (phần tạo `top4_fig`)  
**Mục tiêu:** Phân tách giai đoạn lịch sử bằng vùng tô nhẹ giúp người xem thấy pattern "châu lục nào thống trị giai đoạn nào".

**Các bước thực hiện:**
1. Sau khi tạo `top4_fig`, thêm vrect cho 4 giai đoạn thể thức:
   ```python
   # Giai đoạn 13–16 đội (1930–1954)
   top4_fig.add_vrect(x0=1928, x1=1956, fillcolor="#f6f8fb", opacity=0.3, layer="below", line_width=0)
   # Giai đoạn 16 đội (1958–1982)
   top4_fig.add_vrect(x0=1956, x1=1984, fillcolor="#eef4f5", opacity=0.3, layer="below", line_width=0)
   # Giai đoạn 24 đội (1986–1994)
   top4_fig.add_vrect(x0=1984, x1=1996, fillcolor="#f6f8fb", opacity=0.3, layer="below", line_width=0)
   # Giai đoạn 32 đội (1998–2022)
   top4_fig.add_vrect(x0=1996, x1=2024, fillcolor="#eef4f5", opacity=0.3, layer="below", line_width=0)
   ```
2. Thêm nhãn nhỏ cho mỗi giai đoạn (tùy chọn):
   ```python
   for x_pos, label in [(1935, "13-16 đội"), (1965, "16 đội"), (1988, "24 đội"), (2008, "32 đội")]:
       top4_fig.add_annotation(x=x_pos, y=4.1, text=label, showarrow=False, font={"size": 9, "color": COLORS["muted"]})
   ```
3. Xoay nhãn trục X 45°: `top4_fig.update_xaxes(tickangle=-45)`.

**Tiêu chí chấp nhận:**
- [x] 4 vùng vrect hiển thị nhẹ (opacity thấp, không che khuất bars).
- [x] Nhãn giai đoạn nhỏ, màu muted, không cạnh tranh với data.
- [x] Nhãn X axis xoay 45° không chồng chéo.
- [x] Chart vẫn hiển thị đúng khi filter year range.

**Bước kiểm tra:** Mở Dominance. Scroll đến stacked bar. Kiểm tra 4 vùng phân tách thấy rõ nhưng không che khuất bars.

**Ghi chú / rủi ro:** vrect dùng `layer="below"` để không che phủ bars. `x0/x1` cần dùng giá trị năm chính xác. Nếu filter year range nhỏ hơn, các vrect ra ngoài phạm vi vẫn ổn (Plotly tự clip).

---

#### Task 4.3 — Nâng cấp tooltip Goals For chart — thêm bàn/lần tham dự

**Ưu tiên:** P1  
**Loại:** Visualization  
**Liên quan plan:** "Thêm cột bàn thắng/lần tham dự làm tooltip bổ sung — `hovertemplate='... Avg: {gf/app:.1f}/tournament'`"  
**File/component ảnh hưởng:** `pages/dominance.py`, hàm `update_dominance()` dòng 379–402 (phần tạo `goals_fig`)  
**Mục tiêu:** Brazil luôn đứng đầu về tổng bàn thắng vì tham dự nhiều nhất (22 kỳ). Thêm "bàn/lần tham dự" vào tooltip giúp người xem hiểu giá trị tương đối.

**Các bước thực hiện:**
1. Trong `goals_by_team` aggregation (dòng 379), đã có cột `appearances`. Tính thêm `goals_per_appearance`:
   ```python
   goals_by_team["goals_per_appearance"] = (goals_by_team["total_goals_for"] / goals_by_team["appearances"]).round(1)
   ```
2. Thêm `custom_data=["appearances", "goals_per_appearance"]` vào `px.bar()`.
3. Cập nhật `hovertemplate`:
   ```python
   goals_fig.update_traces(
       hovertemplate=(
           "<b>%{y}</b><br>"
           "Tổng bàn thắng: %{x}<br>"
           "Số lần tham dự: %{customdata[0]}<br>"
           "Trung bình: %{customdata[1]} bàn/kỳ<extra></extra>"
       )
   )
   ```

**Tiêu chí chấp nhận:**
- [x] Hover vào Brazil: hiển thị "Tổng bàn thắng: X, Số lần tham dự: 22, Trung bình: Y.Y bàn/kỳ".
- [x] Không có lỗi khi `appearances = 0` (chia cho 0) — đã xử lý bằng `.round(1)` và Pandas sẽ trả về `NaN`.

**Bước kiểm tra:** Mở Dominance, hover vào bar Brazil trong Goals For chart — kiểm tra tooltip hiện đầy đủ 3 dòng thông tin.

**Ghi chú / rủi ro:** Nếu `appearances = 0`, `goals_per_appearance` sẽ là `inf` hoặc `NaN`. Thêm `.fillna(0)` sau khi tính toán.

---

### Phase 5 — Cải thiện trang Upsets

#### Task 5.1 — Thêm annotation vùng quadrant cho scatter plot

**Ưu tiên:** P2  
**Loại:** Visualization / Storytelling  
**Liên quan plan:** "Thêm annotation vùng quadrant: 'Đội thấp rank thắng lớn' tại góc phải-dưới."  
**File/component ảnh hưởng:** `pages/upsets.py`, hàm `_scatter_figure()` dòng 269–303  
**Mục tiêu:** Người xem nhìn vào scatter phải hiểu ngay 4 vùng quadrant mà không cần đọc chú thích ngoài. Annotation nhỏ, màu muted, đặt tại góc.

**Các bước thực hiện:**
1. Sau khi tạo figure và add hline/vline, tính `max_rank_gap` và `min_goal_diff`:
   ```python
   max_rg = float(df["rank_gap"].quantile(0.95)) if not df.empty else 100
   min_gd = float(df["home_goal_diff"].quantile(0.05)) if not df.empty else -5
   ```
2. Thêm annotation tại góc phải-dưới (rank cao, thua nhiều — kết quả bình thường):
   ```python
   fig.add_annotation(
       x=max_rg * 0.7, y=min_gd * 0.7,
       text="Đội yếu hơn, thua nhiều<br>(dự đoán được)",
       showarrow=False,
       font={"size": 9, "color": COLORS["muted"]},
       align="center",
   )
   ```
3. Thêm annotation tại góc phải-trên (rank cao, thắng — đây là upset!):
   ```python
   fig.add_annotation(
       x=max_rg * 0.7, y=float(df["home_goal_diff"].quantile(0.9)) * 0.7 if not df.empty else 3,
       text="Đội yếu hơn, nhưng THẮNG<br>(upset!)",
       showarrow=False,
       font={"size": 9, "color": COLOR_UPSET},
       align="center",
   )
   ```

**Tiêu chí chấp nhận:**
- [x] 2 annotation xuất hiện ở góc phải-dưới và phải-trên.
- [x] Annotation màu muted và orange — nhỏ, không che điểm dữ liệu.
- [x] Không có lỗi khi df rỗng (return sớm với `empty_figure`).

**Bước kiểm tra:** Mở Upsets, xem scatter plot. Kiểm tra 2 annotation vùng quadrant nhỏ ở góc phải.

**Ghi chú / rủi ro:** Annotation sử dụng percentile thay vì max để tránh outlier cực đoan đẩy annotation ra ngoài tầm nhìn. Kiểm tra với nhiều bộ filter khác nhau.

---

#### Task 5.2 — Xác nhận legend scatter plot hiển thị tên mô tả

**Ưu tiên:** P1  
**Loại:** Visualization  
**Liên quan plan:** "Đổi tên trace legend: 'Upset (Đội yếu thắng)' / 'Kết quả thông thường'. Đổi legend từ 'True'/'False'."  
**File/component ảnh hưởng:** `pages/upsets.py`, hàm `_scatter_figure()`, `fig.for_each_trace()` dòng 293–300  
**Mục tiêu:** Legend phải hiển thị tên mô tả, không phải "True"/"False".

**Các bước thực hiện:**
1. Xác nhận đoạn code `for_each_trace` (dòng 293–300) đang đổi tên trace từ "True" → "Upset — Đội yếu thắng" và "False" → "Kết quả thông thường".
2. Nếu code này chưa có hoặc không hoạt động, thêm:
   ```python
   fig.for_each_trace(
       lambda trace: trace.update(name="Upset — Đội yếu thắng") if trace.name == "True"
       else trace.update(name="Kết quả thông thường")
   )
   ```
3. Reload app — kiểm tra legend scatter plot hiển thị tên đúng.

**Tiêu chí chấp nhận:**
- [x] Legend hiển thị "Upset — Đội yếu thắng" (màu cam) và "Kết quả thông thường" (màu xám).
- [x] Không có "True" hoặc "False" trong legend.

**Bước kiểm tra:** Mở Upsets, nhìn legend của scatter plot.

**Ghi chú / rủi ro:** `for_each_trace` trong Plotly Express so sánh `trace.name` với string. Nếu `color_discrete_map` key là boolean `True`/`False`, Plotly Express có thể convert thành string "True"/"False" — kiểm tra kỹ.

---

### Phase 6 — Cải thiện trang Tournament Detail

#### Task 6.1 — Xác nhận đường diagonal GF=GA trong scatter chart

**Ưu tiên:** P1 — Quan trọng  
**Loại:** Visualization  
**Liên quan plan:** "Đường diagonal GF=GA (nét đứt, màu muted) → người xem tự thấy đội nào thiên tấn công / thiên phòng ngự mà không cần đọc label. `fig.add_shape(type='line', x0=0, y0=0, x1=max_val, y1=max_val, line_dash='dot')`"  
**File/component ảnh hưởng:** `pages/tournament.py`, hàm `update_all()` dòng 383–393  
**Mục tiêu:** Đường GF=GA là đường tham chiếu quan trọng nhất trong scatter — phân biệt "đội thiên tấn công" (phải đường) và "đội thiên phòng ngự" (trái đường).

**Các bước thực hiện:**
1. Xác nhận đoạn code `fig_sc.add_shape()` (dòng 385–388) đang tồn tại và đúng syntax:
   ```python
   fig_sc.add_shape(
       type="line", x0=0, y0=0, x1=max_val, y1=max_val,
       line={"dash": "dot", "color": COLORS["muted"], "width": 1.5},
   )
   ```
2. Xác nhận annotation "GF = GA" (dòng 389–393) hiển thị đúng góc nghiêng.
3. Mở Tournament 2022 — kiểm tra đường diagonal xuất hiện.
4. Thêm annotation vùng hướng dẫn đọc chart:
   ```python
   fig_sc.add_annotation(
       x=max_val * 0.15, y=max_val * 0.85,
       text="Nhiều GA hơn GF<br>(thiên phòng ngự)",
       showarrow=False, font={"size": 9, "color": COLORS["muted"]},
   )
   fig_sc.add_annotation(
       x=max_val * 0.85, y=max_val * 0.15,
       text="Nhiều GF hơn GA<br>(thiên tấn công)",
       showarrow=False, font={"size": 9, "color": COLORS["muted"]},
   )
   ```

**Tiêu chí chấp nhận:**
- [x] Đường diagonal (nét đứt, màu xám) hiển thị từ góc (0,0) đến (max, max).
- [x] Label "GF = GA" hiển thị gần đường diagonal.
- [x] Champion (ARG 2022) nằm ở góc phải-trên (nhiều GF, ít GA — do `yaxis_autorange="reversed"`).
- [x] `yaxis_autorange="reversed"` vẫn được giữ nguyên.

**Bước kiểm tra:** Mở Tournament 2022. Kiểm tra scatter: Argentina phải nằm gần góc phải-trên. Đường diagonal phải đi từ góc dưới-trái sang góc trên-phải (với trục Y đảo).

**Ghi chú / rủi ro:** Với `yaxis_autorange="reversed"`, trục Y đảo ngược — ít GA ở trên. Đường GF=GA vẫn đúng vì `add_shape` dùng giá trị data thực, không phải pixel position.

---

#### Task 6.2 — Đồng nhất thứ tự sắp xếp Goals Against chart

**Ưu tiên:** P1  
**Loại:** Visualization  
**Liên quan plan:** "Đồng nhất thứ tự sắp xếp Goals Against thành `ascending=True` — ít GA ở trên cùng → người xem thấy ngay đội phòng ngự tốt nhất."  
**File/component ảnh hưởng:** `pages/tournament.py`, hàm `update_all()` dòng 339–341  
**Mục tiêu:** Goals Against chart sắp xếp ít GA ở trên = đội phòng ngự tốt nhất ở trên. Nhất quán với Goals For chart (nhiều GF ở trên).

**Các bước thực hiện:**
1. Tìm dòng sắp xếp `ga_df`:
   ```python
   ga_df = ga_df.dropna(subset=["Goals Against"]).sort_values("Goals Against", ascending=True)
   ```
2. Xác nhận `ascending=True` — ít GA ở trên cùng.
3. Nếu hiện tại là `ascending=False`, đổi thành `True`.
4. Kiểm tra: Trang Tournament 2022, chart GA — Morocco (4 GA) và France (8 GA) phải ở gần trên, các đội tệ nhất ở dưới.

**Tiêu chí chấp nhận:**
- [x] Goals Against chart: đội ít bị thủng lưới nhất ở trên cùng.
- [x] Nhất quán với Goals For (nhiều GF ở trên = đội tấn công mạnh nhất ở trên).

**Bước kiểm tra:** Mở Tournament 2022. Kiểm tra GA chart: team ở đỉnh phải có số GA nhỏ nhất.

**Ghi chú / rủi ro:** Thay đổi `ascending=True` → `False` hoặc ngược lại — đơn giản, rủi ro thấp.

---

#### Task 6.3 — Thêm màu sắc position_group rõ ràng cho insight 2022 panel

**Ưu tiên:** P2  
**Loại:** Storytelling  
**Liên quan plan:** "2022 insight panel đã có — mở rộng cho năm khác. Màu sắc position_group tự nói insight."  
**File/component ảnh hưởng:** `pages/tournament.py`, hàm `_build_insight_panel()` dòng 450–503  
**Mục tiêu:** Insight panel 2022 hiện dùng `COLORS["accent_3"]` (đỏ) cho France — cặp màu amber (Argentina) và đỏ (France) chưa ổn. Đổi màu France sang teal hoặc neutral để tránh liên tưởng "xấu".

**Các bước thực hiện:**
1. Trong `_build_insight_panel()`, tìm màu cho France:
   ```python
   {"team": "France", "color": COLORS["accent_3"], ...}
   ```
2. Đổi thành `COLORS["accent"]` (teal) — nhất quán với `POS_COLORS["Top 4"]`.
3. Kiểm tra: Tournament 2022 — insight panel hiển thị 4 cards với màu phân biệt rõ.

**Tiêu chí chấp nhận:**
- [x] Argentina: amber (`#d98324`) — Champion color.
- [x] France: teal (`#007c89`) — Runner-up/Top 4 color.
- [x] Croatia: accent teal hoặc neutral.
- [x] Morocco: không dùng xanh lá (`#2f855a`) trong cùng panel với đỏ.

**Bước kiểm tra:** Mở Tournament 2022. Scroll xuống insight panel. Kiểm tra 4 màu card.

**Ghi chú / rủi ro:** Đây là panel hard-coded cho 2022. Thay đổi chỉ ảnh hưởng file `tournament.py`, không ảnh hưởng các năm khác.

---

### Phase 7 — Polish Tương tác và Usability

#### Task 7.1 — Xử lý empty state khi filter Dominance trả về rỗng

**Ưu tiên:** P2  
**Loại:** Interaction / QA  
**Liên quan plan:** "Thiếu 'Reset All Filters' rõ ràng. No-data Warning — `empty_figure()` đã có. Thêm text hướng dẫn reset filter."  
**File/component ảnh hưởng:** `pages/dominance.py`, hàm `update_dominance()` dòng 300–415  
**Mục tiêu:** Khi filter quá hẹp trả về 0 kết quả, hiển thị thông báo rõ ràng hướng dẫn người dùng reset filter thay vì để chart trống không giải thích.

**Các bước thực hiện:**
1. Kiểm tra các đoạn `if champion_counts.empty:` và `if top4_by_continent.empty:` — xác nhận đã có `empty_figure()`.
2. Cập nhật message trong `empty_figure()` để hướng dẫn reset:
   ```python
   champion_fig = empty_figure(
       "Số lần vô địch theo đội",
       "Không có dữ liệu. Thử mở rộng bộ lọc hoặc chọn lại châu lục / đội."
   )
   ```
3. Tương tự cho `top4_fig` và `goals_fig`.
4. Kiểm tra `dominance-summary-table` khi `filtered` rỗng — `table_data = []` đã được handle đúng.

**Tiêu chí chấp nhận:**
- [x] Filter chọn một team không có title → champion bar hiện message "Không có dữ liệu. Thử..."
- [x] Message rõ ràng, ngắn gọn, hướng dẫn hành động.

**Bước kiểm tra:** Trang Dominance, filter chọn "Tunisia" (team chưa từng vô địch). Champion bar phải hiện empty state với message hướng dẫn.

**Ghi chú / rủi ro:** `empty_figure()` trong `theme.py` nhận tham số `message`. Đảm bảo truyền đúng tham số.

---

#### Task 7.2 — Thêm nút Reset Filters cho trang Dominance

**Ưu tiên:** P2  
**Loại:** Interaction  
**Liên quan plan:** "Thêm nút 'Đặt lại bộ lọc' — Filter Dominance không có 'Reset All' rõ ràng. Chương 8 yêu cầu 'Reset All Filters là bắt buộc'."  
**File/component ảnh hưởng:** `pages/dominance.py`, hàm `layout()` và `register_callbacks()`, hàm `update_dominance()`  
**Mục tiêu:** Người dùng có thể reset tất cả filter về mặc định bằng một click.

**Các bước thực hiện:**
1. Thêm `html.Button("Đặt lại bộ lọc", id="dominance-reset-btn", ...)` vào filter panel trong `layout()`.
2. Đăng ký callback riêng để reset:
   ```python
   @app.callback(
       Output("dominance-year-range", "value"),
       Output("dominance-team-filter", "value"),
       Output("dominance-continent-filter", "value"),
       Output("dominance-position-filter", "value"),
       Input("dominance-reset-btn", "n_clicks"),
       prevent_initial_call=True,
   )
   def reset_dominance_filters(n_clicks):
       return [min(AVAILABLE_YEARS), max(AVAILABLE_YEARS)], [], CONTINENT_OPTIONS, POSITION_OPTIONS
   ```
3. Style button:
   ```python
   html.Button(
       "Đặt lại", id="dominance-reset-btn",
       style={"padding": "8px 16px", "background": "var(--surface-alt)",
              "border": "1px solid var(--border)", "borderRadius": "6px",
              "cursor": "pointer", "fontSize": "13px", "color": "var(--muted)"},
   )
   ```

**Tiêu chí chấp nhận:**
- [x] Nút "Đặt lại" xuất hiện trong filter panel.
- [x] Click nút: tất cả filter reset về mặc định (1930–2022, tất cả team, tất cả continent, tất cả position).
- [x] `prevent_initial_call=True` đảm bảo không trigger khi load lần đầu.

**Bước kiểm tra:** Set filter hẹp (chọn 1 team, 1 continent). Click "Đặt lại" — filter phải trở về mặc định và chart reload đầy đủ data.

**Ghi chú / rủi ro:** Callback reset trả về 4 Output — đảm bảo thứ tự Output/Return khớp nhau. `n_clicks` bắt đầu là `None` — `prevent_initial_call=True` bắt buộc.

---

#### Task 7.3 — Nâng cấp hovertemplate Overview — thêm context % thay đổi

**Ưu tiên:** P2  
**Loại:** Interaction / Visualization  
**Liên quan plan:** "Nâng cấp Tooltip Overview — Thêm context '% thay đổi so với kỳ trước' trong hovertemplate."  
**File/component ảnh hưởng:** `pages/overview.py`, hàm `_scale_figure()` dòng 130–184  
**Mục tiêu:** Tooltip hover trên Scale Chart hiện chỉ có "Năm: X, Teams: Y". Thêm "% thay đổi so với kỳ trước" để tạo context "So What?".

**Các bước thực hiện:**
1. Tính cột % change trước khi vẽ:
   ```python
   for col in ["teams", "matches_played", "goals_scored"]:
       df[f"{col}_pct"] = df[col].pct_change().multiply(100).round(1)
   ```
2. Thêm `customdata` và cập nhật `hovertemplate` cho mỗi trace:
   ```python
   hovertemplate=f"Năm: %{{x}}<br>{label}: %{{y:,}}<br>Thay đổi: %{{customdata:.1f}}%<extra></extra>"
   ```
   và `customdata=df[f"{column}_pct"]` cho mỗi trace.

**Tiêu chí chấp nhận:**
- [x] Hover vào điểm 1998 trên subplot Teams: hiện "Teams: 32, Thay đổi: +33.3%".
- [x] Điểm đầu tiên (1930): "Thay đổi: nan%" — xử lý bằng `fillna("")`.

**Bước kiểm tra:** Hover vào điểm 1998 trên Scale Chart — kiểm tra tooltip có dòng "Thay đổi".

**Ghi chú / rủi ro:** `pct_change()` trả về `NaN` cho năm đầu tiên. Dùng `.fillna(0)` hoặc hiển thị "N/A". Khi filter thay đổi, phép tính % thay đổi phải được tính lại trên `df` đã filter.

---

### Phase 8 — QA Cuối, Chụp màn hình, Căn chỉnh Báo cáo

#### Task 8.1 — QA toàn diện 4 trang

**Ưu tiên:** P0  
**Loại:** QA  
**Liên quan plan:** "Checklist Kỹ thuật — NO CRASH: Chạy app không lỗi, chuyển 4 trang không callback error. ZERO-BASELINE: Tất cả bar charts xác nhận Y-axis bắt đầu từ 0. CVD: Không có cặp màu đỏ-xanh."  
**File/component ảnh hưởng:** Tất cả 4 trang  
**Mục tiêu:** Xác nhận toàn bộ checklist trước khi nộp.

**Các bước thực hiện:**
1. Chạy `python app.py`, mở browser, kiểm tra console không có lỗi.
2. Lần lượt kiểm tra từng trang:
   - **Overview**: Insight card hiển thị. 3 charts render. Annotation 1998 hiển thị. Annotation avg goals max/min hiển thị. Timeline legend đúng.
   - **Dominance**: Insight card hiển thị. Champion bar có highlight màu amber cho đội đứng đầu. Stacked bar có vrect giai đoạn. Goals bar tooltip có bàn/kỳ.
   - **Upsets**: Insight card hiển thị. Scatter màu cam/xám. Stacked bar màu xanh/cam/xám nhạt. Legend tên mô tả.
   - **Tournament**: POS_COLORS CVD-safe. Scatter có diagonal line. GA chart sắp xếp ascending. 2022 insight panel.
3. Test tương tác: filter, slider, dropdown, click detail panel (Upsets).
4. Test responsive: thu nhỏ cửa sổ xuống 1120px và 720px — kiểm tra layout không bị vỡ.

**Tiêu chí chấp nhận — Checklist hoàn chỉnh:**
- [x] **CVD-FIX**: `POS_COLORS["Top 8"]` = `"#7c3aed"` (purple).
- [x] **CVD-FIX**: `COLOR_UPSET` = `"#f97316"` (orange).
- [x] **CVD-FIX**: `COLOR_HOME`/`COLOR_AWAY` = Blue/Orange.
- [x] **TITLES**: Tất cả chart titles ≤ 10 từ.
- [x] **INSIGHT QUA DESIGN**: Ít nhất 1 annotation lịch sử trên line charts.
- [x] **HIGHLIGHT**: Champion bar có màu nổi bật cho đội đứng đầu.
- [x] **DIAGONAL LINE**: Scatter tournament-scatter-chart có đường GF=GA.
- [x] **SORTING**: Goals Against chart sắp xếp ascending (ít GA ở trên).
- [x] **LEGEND**: Scatter upsets legend hiển thị "Upset — Đội yếu thắng".
- [x] **EMPTY STATE**: Tất cả charts có `empty_figure()` khi filter trả về rỗng.
- [x] **NO CRASH**: Không có callback exception nào.
- [x] **INSIGHT CARDS**: Cả 3 trang (Overview, Dominance, Upsets) có insight card.
- [x] **2022 PANEL**: Insight panel hiển thị khi chọn năm 2022.
- [x] **RESPONSIVE**: Layout đúng ở 1120px và 720px.

**Bước kiểm tra:** Dùng checklist này như công cụ kiểm tra — đánh dấu từng mục sau khi xác nhận.

**Ghi chú / rủi ro:** Nếu có lỗi callback, kiểm tra `suppress_callback_exceptions=True` trong `app.py` dòng 44 — đây là cài đặt an toàn cho multi-page app.

---

#### Task 8.2 — Chụp màn hình 4 trang cho báo cáo

**Ưu tiên:** P0  
**Loại:** QA / Báo cáo  
**Liên quan plan:** "Screenshot được chụp: Overview, Dominance, Upsets, Tournament 2022."  
**File/component ảnh hưởng:** Không có (task thủ công)  
**Mục tiêu:** Chuẩn bị tài liệu hình ảnh cho báo cáo nhóm.

**Các bước thực hiện:**
1. Chạy app ở chế độ sản phẩm (`debug=False` trong `app.py`).
2. Chụp màn hình full-page cho 4 trang ở trạng thái mặc định.
3. Chụp thêm màn hình khi hover vào điểm dữ liệu quan trọng (ví dụ: hover 1998 trên scale chart).
4. Chụp màn hình Tournament 2022 với scatter chart và insight panel.
5. Lưu với tên file mô tả: `screenshot_overview.png`, `screenshot_dominance.png`, `screenshot_upsets.png`, `screenshot_tournament_2022.png`.

**Tiêu chí chấp nhận:**
- [ ] 4 screenshots rõ nét, đầy đủ nội dung trang.
- [ ] Ít nhất 1 screenshot có tooltip hiển thị.
- [ ] Tournament 2022 screenshot bao gồm cả 2022 insight panel.

---

### Phase 9 — Tùy chọn / Bonus (P3)

> **Lưu ý:** Các task trong Phase 9 là **tùy chọn hoàn toàn**, chỉ thực hiện nếu còn thời gian sau Phase 8. Không bắt buộc để hoàn thành yêu cầu project.

#### Task 9.1 — [P3] Choropleth Map trang Dominance

**Ưu tiên:** P3  
**Loại:** Visualization (Bonus)  
**Liên quan plan:** "Choropleth Map đơn giản vào trang Dominance dùng `px.choropleth` với `color=championship_count`, bảng màu YlOrBr."  
**File/component ảnh hưởng:** `pages/dominance.py`  
**Mục tiêu:** Thêm chiều không gian địa lý — hiển thị số lần vô địch theo màu trên bản đồ thế giới.

**Ghi chú:** Rủi ro cao về việc mapping tên đội sang ISO country code (West Germany, FR Yugoslavia, etc.). Chỉ triển khai nếu đã hoàn thành Phase 0–8.

---

#### Task 9.2 — [P3] Small Multiples trang Dominance

**Ưu tiên:** P3  
**Loại:** Visualization (Bonus)  
**Liên quan plan:** "Thêm Small Multiples cho Dominance page: mỗi ô là một châu lục, X=Year, Y=số lần top 4. Dùng `px.bar(..., facet_col='continent')`."  
**File/component ảnh hưởng:** `pages/dominance.py`  
**Mục tiêu:** So sánh xu hướng top 4 của từng châu lục song song.

---

#### Task 9.3 — [P3] Animated Race Chart

**Ưu tiên:** P3  
**Loại:** Visualization (Bonus)  
**Liên quan plan:** "`px.bar(..., animation_frame='Year', ...)` cho champion count accumulation qua các năm."  
**File/component ảnh hưởng:** `pages/dominance.py`  
**Mục tiêu:** Race chart hiển thị tích lũy số lần vô địch qua từng kỳ World Cup.

---

#### Task 9.4 — [P3] Closing Note về World Cup 48 đội 2026

**Ưu tiên:** P3  
**Loại:** Storytelling (Bonus)  
**Liên quan plan:** "Thêm text block về World Cup 2026 (48 đội) ở cuối trang Overview."  
**File/component ảnh hưởng:** `pages/overview.py`, `layout()`  
**Mục tiêu:** Kết thúc narrative arc bằng câu hỏi mở về tương lai.

---

## 4. Bảng Phụ thuộc

| Task | Phụ thuộc vào | Lý do |
|---|---|---|
| Task 1.1 (CVD tournament) | Task 0.1 (baseline check) | Cần biết trạng thái hiện tại trước khi sửa |
| Task 1.2 (CVD upsets) | Task 0.1 | Tương tự |
| Task 2.1–2.4 (titles) | Task 1.1, 1.2 | Tiêu đề thay đổi không ảnh hưởng CVD, nhưng cần đảm bảo màu đúng trước khi QA |
| Task 3.1 (annotations scale) | Task 2.1 (title scale) | Title đúng trước khi thêm annotation |
| Task 3.2 (champion timeline) | Task 2.1 | Title đúng trước khi thêm annotation |
| Task 4.1 (highlight Brazil) | Task 2.2 (title dominance) | Title đúng, sau đó thêm highlight |
| Task 4.2 (vrect) | Task 4.1 | Cùng hàm `update_dominance()`, thực hiện sau Task 4.1 |
| Task 4.3 (tooltip goals) | Task 4.1 | Cùng hàm, thực hiện tuần tự |
| Task 5.1 (quadrant annotation) | Task 1.2, 2.3 | Màu CVD-safe và title đúng |
| Task 5.2 (legend names) | Task 1.2 | Màu đã đúng, thêm legend tên |
| Task 6.1 (diagonal line) | Task 1.1 | CVD-safe POS_COLORS đã đúng |
| Task 6.2 (GA sorting) | Task 1.1 | Chart màu đúng |
| Task 7.1–7.2 (empty state, reset) | Phase 3–6 | Cần chart đúng trước khi test tương tác |
| Task 8.1 (QA) | Tất cả Phase 1–7 | QA cuối sau tất cả thay đổi |
| Task 8.2 (screenshot) | Task 8.1 | Sau QA pass |
| Phase 9 (bonus) | Task 8.2 | Chỉ sau khi hoàn thành tất cả |

---

## 5. Thứ tự Thực thi Đề xuất

```
[NGÀY 1 — Buổi sáng]
  Task 0.1 → Task 0.2  (baseline check — 30 phút)
  Task 1.1 → Task 1.2 → Task 1.3  (CVD fixes — 45 phút)

[NGÀY 1 — Buổi chiều]
  Task 2.1 → Task 2.2 → Task 2.3 → Task 2.4  (titles — 60 phút)
  Task 3.1 → Task 3.2  (overview improvements — 60 phút)

[NGÀY 2 — Buổi sáng]
  Task 4.1 → Task 4.2 → Task 4.3  (dominance improvements — 90 phút)
  Task 5.1 → Task 5.2  (upsets improvements — 45 phút)

[NGÀY 2 — Buổi chiều]
  Task 6.1 → Task 6.2 → Task 6.3  (tournament improvements — 60 phút)
  Task 7.1 → Task 7.2 → Task 7.3  (polish — 60 phút)

[NGÀY 3]
  Task 8.1 (QA toàn diện — 45 phút)
  Task 8.2 (chụp màn hình — 15 phút)
  [Nếu còn thời gian] Phase 9 (bonus tasks)
```

---

## 6. Rủi ro và Kế hoạch Rollback

| Rủi ro | Xác suất | Tác động | Kế hoạch Rollback |
|---|---|---|---|
| Annotation trong subplot Plotly dùng sai tham số `row/col` → hiển thị sai vị trí | Trung bình | Thấp | Xóa annotation, kiểm tra Plotly docs về `add_annotation()` với subplot |
| `for_each_trace()` không match đúng trace name "True"/"False" → legend vẫn hiển thị boolean | Thấp | Thấp | Dùng `fig.data[0].name = "..."` trực tiếp thay vì `for_each_trace` |
| Highlight Brazil bằng `marker_color` list → lỗi nếu thứ tự `tail(20)` không nhất quán với list màu | Trung bình | Trung bình | Tạo dict `{team: color}` và map thay vì list |
| vrect với năm range nhỏ → vrect ra ngoài domain → Plotly warning | Thấp | Rất thấp | Giữ vrect, Plotly tự clip, không gây lỗi |
| Reset filter callback trigger vòng lặp với `update_dominance` | Thấp | Cao | Dùng `prevent_initial_call=True`, kiểm tra không có circular dependency |
| `pct_change()` với 1 điểm dữ liệu (filter hẹp) → tất cả NaN | Trung bình | Thấp | `.fillna("N/A")` trong hovertemplate |
| Annotation Brazil "5 lần" dùng sai `champion_norm` name | Thấp | Thấp | In `df["champion_norm"].unique()` để xác nhận tên chính xác |
| CVD colors đã đúng trong code nhưng browser cache cũ → màu cũ vẫn hiển thị | Thấp | Thấp | Hard refresh (Ctrl+F5) hoặc clear browser cache |

**Rollback tổng thể:** Nếu bất kỳ thay đổi nào gây lỗi không khắc phục được, dùng `git diff` để xem thay đổi và `git checkout pages/<file>.py` để khôi phục file gốc.

---

## 7. Definition of Done

### Kỹ thuật
- [x] `python app.py` chạy không lỗi trên Python 3.9+ với Dash 2.x.
- [x] Cả 4 trang render đúng, không có callback exception trong console.
- [x] Tất cả filter (RangeSlider, Dropdown, MatchType) hoạt động và cập nhật chart.
- [x] Click detail panel trong Upsets hoạt động (scatter + bar).
- [x] Trang Tournament hiển thị đúng khi thay đổi năm.
- [x] Layout responsive đúng ở 3 breakpoint: 1440px, 1120px, 720px.

### CVD Accessibility
- [x] Không có cặp màu đỏ (`#c44536`) + xanh lá (`#2f855a`) trong cùng một chart.
- [x] `POS_COLORS["Top 8"]` = `"#7c3aed"` (purple).
- [x] Upset scatter và neutral stacked bar dùng Blue-Orange scheme.

### Visualization Quality
- [x] Tất cả chart titles ≤ 10 từ, không có dấu chấm than hoặc câu hỏi dài.
- [x] Insight tự hiện ra qua: annotation trực tiếp trên chart (ít nhất 1 chart), highlight màu (champion bar), reference line (diagonal GF=GA), thứ tự sắp xếp (GA ascending).
- [x] Zero-baseline: tất cả bar charts có X/Y axis bắt đầu từ 0.
- [x] Tooltip có context "So What?" cho ít nhất 2 charts.

### Storytelling
- [x] 3 trang (Overview, Dominance, Upsets) có `.insight-card` với nội dung đúng narrative arc.
- [x] Tournament 2022 hiển thị insight panel với 4 storylines.
- [x] Narrative arc 4 Act tự hiện qua visual: Mở rộng → Thống trị → Bất ngờ → Case Study.

### Báo cáo
- [ ] 4 screenshots đã chụp, sẵn sàng cho báo cáo.
- [x] Mỗi quyết định thiết kế có thể giải thích theo framework Mackinlay (Position > Length > Area > Color) và nguyên tắc Chương 1–9.

---

*Tài liệu này được tạo dựa trên phân tích toàn bộ source code tại `DV_project/` và kế hoạch cải tiến trong `dashboard_visualization_improvement_plan.md`. Mọi task đều tham chiếu function name, line number ước tính, và component ID cụ thể để coding agent có thể thực thi mà không cần đọc lại toàn bộ plan.*
