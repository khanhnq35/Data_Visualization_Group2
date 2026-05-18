# Giám sát quá trình xử lý của máy chủ

## 1. Tổng quan

Chương 18 - giám sát quá trình xử lý của máy chủ được thiết kế bởi Mark Jackson cho tổ chức Piedmont Healthcare. Dashboard dưới đây giám sát máy chủ và hiển thị các quy trình bị trì hoãn hoặc thất bại trong mọi ngày.

![Dashboard tổng quan](figure/dashboard_overview.png)

Một nhà quản lý Business Intelligence (khai thác dữ liệu doanh nghiệp) cần hệ thống dữ liệu phải sẵn sàng và được cập nhật mới nhất ngay khi họ đến văn phòng vào buổi sáng. Dashboard này sinh ra để xem có sự cố nào xảy ra với các tiến trình chạy qua đêm hay không, từ đó nhảy thẳng vào xử lý lỗi và xem xét lịch sử xem lỗi này có thường xuyên xảy ra không.

## 2. Phân tích dashboard

Dashboard bao gồm 2 biểu đồ: biểu đồ cột và biểu đồ Gantt.

### a. Biểu đồ cột

Biểu đồ cột hiển thị phần trăm lỗi của 14 ngày qua, với một đường nét đứt thể hiện mức lỗi trung bình. Ta thấy ngày 20 tháng 3 có 6.7% tiến trình thất bại - cao hơn mức trung bình nên cần phải xem xét. Ngoài ra, cùng ngày (13 tháng 3) của tuần trước cũng có phần trăm lỗi vượt quá mức trung bình, thể hiện khả năng xảy ra lỗi lớn vào ngày Chủ nhật.

Trong biểu đồ này, tác giả sử dụng toàn bộ màu đỏ để biểu thị phần trăm lỗi. Mức lỗi trung bình được thể hiện qua màu nét đứt, giúp người xem dễ so sánh với các cột mà không bị mất tập trung vào đường kẻ. Khi ấn vào cụ thể các cột, dashboard sẽ hiển thị thêm biểu đồ Gantt bên dưới.

### b. Biểu đồ Gantt

Biểu đồ Gantt là công cụ quản lý dự án trực quan, sử dụng các thanh ngang để biểu diễn tiến độ công việc theo dòng thời gian. Cụ thể trong dashboard trên, trục dọc biểu diễn danh sách các tiến trình, trục ngang biểu diễn thời gian trong ngày với độ chia là 1 tiếng.

Với các thanh ngang, màu xám thể hiện tiến trình đã thực hiện thành công, bắt đầu và kết thúc trong khoảng thời gian đó. Màu đỏ thể hiện tiến trình đang bị lỗi, thời gian bắt đầu xảy ra và thời gian ngắt và báo lỗi về hệ thống. Đường nét đứt dọc thể hiện thời gian bắt đầu dự kiến, còn đường nét liền dọc thể hiện thời lượng trung bình để hoàn thành hoặc báo lỗi của một tiến trình. Vùng màu xanh kéo dài từ 8:00 am đến 5:00 pm biểu thị cho giờ hành chính, phù hợp với bối cảnh của doanh nghiệp.

![Tooltip bổ sung chi tiết về lỗi](figure/fig18.1_The_tool_tip.png)

Ngoài ra, khi di chuột vào thanh tác vụ, một bảng chú thích (tooltip) hiện ra cho thấy tác vụ đó mất cụ thể bao nhiêu tiếng để hoàn thành, thời gian bắt đầu, v.v. Nhìn lướt qua biểu đồ, ta có thể thấy 4 khoảng thời gian dự kiến của các tiến trình sẽ bắt đầu gồm 7:30 am, 8:00 am, 10:30 am, 11:00 am.

Đặc biệt, tiến trình "Epic Radiant Orders" đang bị lỗi. Tiến trình này mất gần 7 tiếng mới báo lỗi, trong khi bình thường chỉ mất 2 tiếng. Qua bảng chú thích, lỗi có thể xảy ra do kết nối từ SQL Server đến Tableau và do dữ liệu rỗng trong khi dùng các hàm tính toán tổng hợp của SQL.

![Biểu đồ chi tiết tiến trình Epic Radiant Orders](figure/fig18.2_Detail_view.png)

Tuy nhiên, có một vấn đề xảy ra trong biểu đồ Gantt: nếu chỉ nhìn vào những tiến trình cùng lúc trên một biểu đồ, ta sẽ khó so sánh và quan sát một tiến trình trong một khoảng thời gian. Trên đây là biểu đồ chi tiết hơn của tiến trình "Epic Radiant Orders" trong khoảng 1 tháng.

Biểu đồ sử dụng trục hoành để thể hiện thời gian trong ngày và trục tung cho các ngày. Độ dài và vị trí của mỗi thanh ngang mã hóa chính xác thời điểm bắt đầu cũng như thời lượng của tác vụ. Đặc biệt, việc sử dụng màu sắc có chủ đích kết hợp với đường tham chiếu dọc nét đứt (biểu thị thời gian dự kiến bắt đầu) giúp người quản trị ngay lập tức nhận ra một xu hướng cốt lõi: tiến trình này đã hỏng 7 lần trong tháng qua và dường như cứ hôm nào khởi chạy trễ (thanh biểu đồ nằm lệch hẳn sang phải so với đường nét đứt) thì hệ thống lại báo lỗi, từ đó cung cấp căn cứ trực quan mạnh mẽ để khoanh vùng và chẩn đoán nguyên nhân sự cố.

## 3. Đánh giá thiết kế từ tác giả

### a. Vị trí đặt nhãn tối ưu tốc độ nhìn

Thông thường, tên của các tiến trình sẽ được đặt gọn gàng ở lề bên trái của biểu đồ. Tuy nhiên, Mark Jackson đã chọn cách dán trực tiếp nhãn tên lên ngay đầu các thanh Gantt. Ông đánh giá đây là một sự hy sinh có chủ đích: khi mắt người quản trị nhìn thấy một thanh màu đỏ (lỗi), tên tiến trình cũng nằm ngay tại vị trí đó. Họ không cần phải dò mắt sang tận lề trái để đối chiếu xem đó là tiến trình nào, giúp tiết kiệm thời gian phản ứng.

![So sánh vị trí nhãn trên thanh Gantt và nhãn ở lề trái](figure/fig18.3_Label_position_compare.png)

### b. Đường tham chiếu giúp phát hiện độ trễ

Các đường tham chiếu trong biểu đồ Gantt giúp người xem nhận biết thời điểm dự kiến bắt đầu và thời lượng trung bình của từng tác vụ. Nhờ đó, Mark có thể thấy "Epic Radiant Orders" không chỉ thất bại mà còn bắt đầu muộn đáng kể so với lịch trình.

![Đường nét đứt và đường liền trong biểu đồ Gantt](figure/fig18.4_Dot_line.png)

### c. Lỗi thẩm mỹ

Andy chỉ ra lỗi thiết kế phần chữ của các nhãn dán bị đè lộn xộn lên các đường kẻ tham chiếu dọc. Tuy nhiên, dashboard này được thiết kế dành riêng cho một mình Mark sử dụng. Nếu dashboard này được xuất bản cho toàn bộ nhân viên công ty cùng xem, thiết kế bắt buộc phải được làm chỉn chu.

### d. Tuân thủ nguyên tắc về khám phá dữ liệu

Luồng khám phá dữ liệu đi từ tổng quan, đến lọc và phóng to, rồi đến chi tiết khi cần:

1. Tổng quan: biểu đồ cột cho biết tỷ lệ lỗi trong các ngày gần đây.
2. Lọc và phóng to: click vào một ngày để ra biểu đồ Gantt của ngày đó.
3. Chi tiết khi cần: click vào thanh Gantt để xem tooltip, xem link máy chủ, hoặc mở biểu đồ lịch sử 1 tháng.

Luồng đi từ trên xuống dưới này rất trực quan và dễ theo dõi.

![Dashboard có luồng phân tích từ trên xuống dưới](figure/fig18.5_Dashboard_good_top_down_workflow.png)
