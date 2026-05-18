# Sự cám dỗ của biểu đồ tròn và donut

## 1. Tổng quan

Như đã thảo luận trong Chương 1, hai phương pháp mã hóa tốt nhất để so sánh định lượng chính xác là:

- Sử dụng chiều dài hoặc chiều cao từ một đường cơ sở chung để so sánh, ví dụ biểu đồ cột (bar chart).
- Sử dụng vị trí để so sánh, cũng thường dựa trên một đường cơ sở chung, ví dụ biểu đồ điểm (dot plot).

Khi cố gắng thể hiện các so sánh định lượng chính xác, việc sử dụng góc, cung, diện tích hoặc kích thước của hình tròn không tốt bằng việc sử dụng chiều dài hoặc vị trí để mã hóa dữ liệu. Vì lý do này, biểu đồ tròn (pie chart) và biểu đồ donut (donut chart) thường không phải là những lựa chọn tốt để trực quan hóa dữ liệu.

## 2. Những trường hợp sử dụng biểu đồ tròn và donut

### a. Sử dụng biểu đồ tròn trên bản đồ

![Hình 34.1: Biểu đồ tròn trên bản đồ thể hiện các khiếu nại đã được giải quyết và chưa được giải quyết tại mỗi bang của nước Mỹ](figure/Pic34.1_Piechart_on_map.png)

**Hình 34.1:** Biểu đồ tròn trên bản đồ thể hiện các khiếu nại đã được giải quyết (màu xanh lam) và chưa được giải quyết (màu cam) tại mỗi bang của nước Mỹ.

Do không có cách nào dễ dàng để trình bày nhiều biểu đồ cột trên một bản đồ nơi không có đường cơ sở chung để thực hiện so sánh, biểu đồ tròn có thể là một lựa chọn chấp nhận được trong trường hợp này. Sử dụng kích thước của hình tròn cho các so sánh chính xác có thể đặc biệt khó khăn, nhưng việc dùng kích thước như một phương pháp mã hóa phụ trong biểu đồ phân tán để hiển thị thêm bối cảnh cho dữ liệu có thể hữu ích.

Mặc dù ta vẫn có thể tự tạo ra một đường cơ sở chung ở bên ngoài để biểu diễn số liệu qua biểu đồ cột, cách làm đó sẽ không thể hiện tốt vị trí địa lý giữa các bang.

### b. Sử dụng kích thước hình tròn làm mã hóa phụ trong biểu đồ phân tán

![Hình 34.2: Biểu đồ phân tán thể hiện tuổi thọ trung bình khi sinh so với tỷ lệ sinh theo quốc gia](figure/Pic34.2_ScatterPlot.png)

**Hình 34.2:** Biểu đồ phân tán thể hiện tuổi thọ trung bình khi sinh so với tỷ lệ sinh theo quốc gia vào năm 1995.

Biểu đồ phân tán (scatterplot) trực quan hóa sự so sánh giữa tỷ lệ sinh và tuổi thọ trung bình khi sinh theo quốc gia. Kích thước của hình tròn mã hóa dân số theo quốc gia, một số liệu phụ không quá quan trọng đối với phân tích, còn màu sắc của hình tròn mã hóa lục địa.

Mục đích chính của trực quan hóa này là so sánh tỷ lệ sinh và tuổi thọ trung bình, chứ không phải để thể hiện dân số. Tuy nhiên, dân số vẫn cung cấp thêm ngữ cảnh cho toàn bộ câu chuyện. Người xem cũng dễ dàng nhận ra các quốc gia đông dân nhất thế giới như Trung Quốc và Ấn Độ, chính là những hình tròn lớn màu đỏ.

## 3. Cách giải quyết sự cám dỗ của biểu đồ tròn và donut

### a. Biểu đồ tròn

Ta dễ dàng nhận ra biểu đồ tròn và donut chỉ hiệu quả trong một số ít trường hợp đặc thù. Tuy nhiên, sếp hoặc khách hàng đôi khi vẫn muốn có một biểu đồ tròn, kể cả khi dữ liệu có rất nhiều danh mục. Mục đích của biểu đồ tròn là thể hiện mối quan hệ giữa các phần với tổng thể.

Vấn đề chính khi đọc biểu đồ tròn là so sánh các lát cắt với nhau. Vì vậy, cần tránh chia biểu đồ tròn hoặc biểu đồ donut thành quá nhiều lát cắt. Khi số lát cắt tăng lên, dữ liệu trở nên khó giải mã hơn.

![Hình 34.3: Biểu đồ tròn có 17 danh mục](figure/Pic34.3_Piechart_17categories.png)

**Hình 34.3:** Biểu đồ tròn thể hiện doanh thu từ các mảng trong doanh nghiệp.

Hình 34.3 thể hiện một biểu đồ tròn có quá nhiều lát cắt. Mỗi danh mục là một lát cắt đại diện bằng một màu khác nhau. Ngay cả khi biểu đồ tròn được sắp xếp có trật tự, việc thực hiện so sánh giữa các danh mục vẫn rất khó và đòi hỏi mắt chúng ta phải nhìn qua nhìn lại từ chú giải đến biểu đồ.

Bây giờ hãy xem xét Hình 34.4. Cùng dữ liệu đó được trực quan hóa trong một biểu đồ tròn nhưng có một vài thay đổi lớn. Đầu tiên, chỉ có một lát cắt duy nhất có nhãn, là danh mục được làm nổi bật. Thay vì 17 màu sắc danh mục, chỉ có hai màu: danh mục được làm nổi bật có màu xanh lam và tất cả danh mục khác có màu xám. Một biểu đồ cột được thêm vào để thay thế bảng chú giải màu. Bây giờ người dùng có thể thực hiện so sánh chính xác bằng biểu đồ cột, và nếu có tính tương tác, người dùng có thể chọn một cột để làm nổi bật bất kỳ danh mục nào trong biểu đồ tròn.

![Hình 34.4: Biểu đồ tròn kết hợp biểu đồ cột](figure/Pic34.4_PieChart_SingleCategory_Comparison_BarChart.png)

**Hình 34.4:** Biểu đồ tròn kết hợp biểu đồ cột thể hiện doanh thu từ các mảng trong doanh nghiệp.

Hình 34.4 đáp ứng yêu cầu sử dụng biểu đồ tròn, nhưng đồng thời cung cấp cho người đọc một giải pháp thay thế tận dụng thế mạnh của hệ thống thị giác: độ chính xác mà biểu đồ cột mang lại. Lưu ý rằng giải pháp này cung cấp một thông tin bổ sung không hiển thị ngay lập tức trong các biểu đồ khác: phép so sánh 85,6% so với 14,4%.

### b. Biểu đồ donut

Biểu đồ donut thường được sử dụng như một giải pháp thay thế cho biểu đồ tròn để thể hiện mối quan hệ giữa các phần với tổng thể. Chúng cũng thường được sử dụng để biểu diễn chỉ số hiệu suất (KPI). Hình 34.5 cho thấy khu vực bán hàng phía Bắc đã đạt được 64% mục tiêu.

![Hình 34.5: Biểu đồ donut thể hiện KPI đạt 64% mục tiêu](figure/Pic34.5_DonutChart_KPI.png)

**Hình 34.5:** Biểu đồ donut thể hiện KPI đã đạt 64% mục tiêu.

Vì chỉ có một chỉ số KPI duy nhất, biểu đồ donut này dễ hiểu hơn ví dụ biểu đồ tròn có 17 danh mục. Biểu đồ donut này không yêu cầu người đọc so sánh danh mục này với danh mục khác. Nó chỉ đơn giản là một giá trị thực tế đi quanh vòng tròn để trở lại mức 100% mục tiêu.

Tuy nhiên, hãy xem xét điều gì sẽ xảy ra khi bốn khu vực được đem ra so sánh, như ở Hình 34.6. Phép so sánh này khó hơn nhiều so với việc diễn giải một biểu đồ donut KPI duy nhất, và người dùng có thể sẽ phải phụ thuộc vào các nhãn bên trong biểu đồ donut.

![Hình 34.6: Biểu đồ donut thể hiện KPI của bốn khu vực](figure/Pic34.6_DonutChart_KPI_4Region.png)

**Hình 34.6:** Biểu đồ donut thể hiện phần trăm KPI đạt được so với mục tiêu của bốn khu vực.

Ngoài ra, cần lưu ý rằng loại trực quan hóa KPI này chỉ hữu ích khi mục tiêu có giới hạn trên là 100%. Một mục tiêu bán hàng có thể không có giới hạn trên. Rất có thể đội ngũ bán hàng bán với giá cao hơn dự kiến, bất kể số lượng, và đạt 106% mục tiêu. Một biểu đồ donut KPI sẽ rất khó sử dụng nếu việc thể hiện hiệu suất vượt mục tiêu là quan trọng.

Một giải pháp thay thế khác là thanh tiến trình. Thanh tiến trình rất phổ biến, và thường thì bạn có thể thậm chí không nhận ra khi chúng được sử dụng. Hình 34.7 hiển thị dữ liệu từ biểu đồ donut KPI dưới dạng một thanh tiến trình. Hãy chú ý xem việc so sánh khu vực này với khu vực khác dễ dàng như thế nào.

**Hình 34.7:** Biểu đồ thanh tiến trình thể hiện phần trăm KPI đạt được so với mục tiêu của bốn khu vực. *(Chưa có file ảnh tương ứng trong `figure/`.)*

Vậy trong những tình huống bị yêu cầu sử dụng biểu đồ donut dù hiệu quả không cao, giả định rằng bạn không có lựa chọn nào khác ngoài việc nhượng bộ trước yêu cầu của khách hàng hoặc sếp. Tác giả đề xuất rằng bạn nên điều chỉnh lựa chọn kém này bằng cách mã hóa dữ liệu lặp lại theo một hướng tốt hơn.

![Hình 34.8: Các biểu đồ donut thể hiện tỷ lệ lỗi](figure/Pic34.6_Series_DonutChart_DefectRate.png)

**Hình 34.8:** Các biểu đồ donut thể hiện tỷ lệ lỗi ở các danh mục hoặc thời gian khác nhau.

Như đã thảo luận trước đó, một chuỗi các biểu đồ donut khiến việc so sánh từ biểu đồ này sang biểu đồ khác trở nên thực sự khó khăn. Ví dụ cụ thể này cũng có vấn đề vì tất cả giá trị đều rất thấp, vì vậy việc nhìn thấy khác biệt trong dữ liệu là rất khó.

Bằng cách thêm một biểu đồ cột, có thể nhìn ra những khác biệt nhỏ trong tỷ lệ lỗi trong Hình 34.9. Điều này là do biểu đồ cột sử dụng chiều dài từ một đường cơ sở chung, cho phép một sự so sánh rất chính xác mà các biểu đồ donut không thể mang lại.

![Hình 34.9: Các biểu đồ donut kết hợp biểu đồ cột](figure/Pic34.7_Same_DonutChart_with_BarChart_Ontop.png)

**Hình 34.9:** Các biểu đồ donut và biểu đồ cột thể hiện tỷ lệ lỗi ở các danh mục hoặc thời gian khác nhau.

Trong Hình 34.10, tỷ lệ lỗi được vẽ bên dưới biểu đồ donut, một dấu chấm được sử dụng để thể hiện mỗi 1% lỗi. Hãy chú ý xem việc nhìn thấy sự khác biệt giữa 2% và 3% ở cả Hình 34.9 và 34.10 dễ dàng như thế nào.

![Hình 34.10: Các biểu đồ donut kết hợp biểu đồ điểm](figure/Pic34.8_Same_Donutchart_with_dots.png)

**Hình 34.10:** Các biểu đồ donut và biểu đồ điểm thể hiện tỷ lệ lỗi ở các danh mục hoặc thời gian khác nhau.

Có thể có những trường hợp bạn bị ép buộc phải đưa ra những quyết định thiết kế tồi, chẳng hạn sếp hoặc khách hàng chỉ muốn có một loạt hình donut. Bằng cách kết hợp chúng với biểu đồ cột hoặc biểu đồ điểm, bạn có thể giúp người đọc hiểu dữ liệu tốt hơn mà vẫn đáp ứng được yêu cầu đó. Và nếu may mắn, sếp hoặc khách hàng sẽ nhận ra rằng chính các cột hoặc dấu chấm mới đang làm cho việc so sánh trở nên dễ dàng, từ đó bạn có thể được toàn quyền xóa bỏ các biểu đồ donut.
