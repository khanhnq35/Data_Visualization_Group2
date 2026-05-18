# Data Visualization Group 2

Tài liệu học tập và trình bày cho môn Data Visualization.

## Nội dung

- `Chap18/`: tài liệu chương 18 về dashboard giám sát quá trình xử lý của máy chủ.
- `Chap34/`: tài liệu chương 34 về sự cám dỗ của biểu đồ tròn và donut.
- Các thư mục `figure/`: ảnh minh họa dùng trong file Markdown và HTML slide.

## File chính

- `Chap18/Chap18_Book.md`: nội dung chương 18 chuyển sang Markdown.
- `Chap18/Chap18_Analysis.md`: phần phân tích chương 18.
- `Chap18/Chap18_Slide.md`: nội dung slide Marp chương 18.
- `Chap18/Chap18_Slide.html`: bản trình chiếu HTML chương 18.
- `Chap34/Chap34_Book.md`: nội dung chương 34 chuyển sang Markdown.
- `Chap34/Chap34_Analysis.md`: phần phân tích chương 34.
- `Chap34/Chap34_Slide.md`: nội dung slide Marp chương 34.
- `Chap34/Chap34_Slide.html`: bản trình chiếu HTML chương 34.

## Cách xem slide

Chạy từ Terminal:

```bash
open Chap18/Chap18_Slide.html
open Chap34/Chap34_Slide.html
```

Hoặc mở từng chapter:

```bash
open Chap18/Chap18_Slide.html
```

```bash
open Chap34/Chap34_Slide.html
```

Trong bản HTML, có thể dùng phím mũi tên, Space hoặc nút điều hướng để chuyển slide.

Nếu muốn dùng `make`:

```bash
make open-slide
```

Các target có sẵn:

- `make open-slide`: mở slide của cả Chap18 và Chap34.
- `make open-chap18`: mở slide Chap18.
- `make open-chap34`: mở slide Chap34.
