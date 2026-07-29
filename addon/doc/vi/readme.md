# Liên kết yêu thích

* **Tác giả**: Edilberto Fonseca ([edilberto.fonseca@outlook.com](mailto:edilberto.fonseca@outlook.com))
* **Ngày tạo**: 11/04/2024
* **Giấy phép**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## Giới thiệu

Tiện ích bổ sung **FavoriteLinks** là một công cụ giúp quản lý các liên kết yêu thích của bạn một cách có tổ chức và hiệu quả. Nó cho phép bạn lưu, chỉnh sửa và xóa các liên kết trong danh sách được phân loại, cung cấp giao diện trực quan với các tính năng như thêm liên kết mới, đổi tên tiêu đề, xóa các mục không mong muốn và quản lý danh mục. Ngoài ra, tiện ích bổ sung cho phép nhập dấu trang trực tiếp từ tệp HTML được trình duyệt xuất.

Khi mở tiện ích bổ sung, bạn có thể truy cập nhanh vào các liên kết của mình và có thể mở chúng trực tiếp trong trình duyệt mặc định. Hiện tại cũng có hỗ trợ mở liên kết trong trình duyệt phụ, trong trường hợp bạn cần linh hoạt hơn.

## Cài đặt

Thực hiện theo các bước bên dưới để cài đặt tiện ích **FavoriteLinks** trong NVDA:

1. Trong NVDA, mở menu **Tools** và chọn **Add-ons Store**.
2. Trong tab **Tiện ích bổ sung có sẵn**, hãy điều hướng đến trường **Tìm kiếm**.
3. Tìm kiếm "Liên kết yêu thích". Trong kết quả, nhấn **Enter** hoặc **Áp dụng**, sau đó chọn **Cài đặt**.
4. Khởi động lại NVDA để áp dụng các thay đổi.

## Cấu hình

Bạn có toàn quyền kiểm soát nơi lưu liên kết của mình và trình duyệt nào sẽ mở chúng.

1. Truy cập menu NVDA: `NVDA+N` > *Preferences* > *Settings*.
2. Trong danh sách danh mục, chọn **Liên kết yêu thích**.

Bạn có thể chọn vị trí tùy chỉnh để lưu tệp liên kết bằng nút **"Chọn hoặc thêm thư mục"** (`Alt+S`).

Để xác định trình duyệt phụ, có thể được cài đặt hoặc di động:

1. Điều hướng bằng `Tab` đến trường **Đường dẫn trình duyệt**.
2. Sử dụng nút **"Chọn đường dẫn trình duyệt"** (`Alt+N`) để thêm tệp thực thi của trình duyệt mong muốn.

## Cách sử dụng

### Truy cập tiện ích bổ sung

* Nhấn `Alt+Windows+K`.
* Hoặc truy cập qua `NVDA+N` > *Công cụ* > *Liên kết yêu thích*.

### Giao diện chính

Giao diện chính bao gồm hai trường chính, có thể được điều hướng bằng phím `Tab`:

1. **Danh mục**: Hộp tổ hợp chứa các danh mục hiện có.
2. **Danh sách liên kết**: Danh sách hiển thị các liên kết được liên kết với danh mục đã chọn.

Sử dụng **menu ngữ cảnh** (phím ứng dụng) trong bất kỳ trường nào trong số này để truy cập các tùy chọn bổ sung.

### Hành động có sẵn

#### Trong Hộp Tổ Hợp Danh Mục

* **Thêm danh mục**: Tạo danh mục mới.
* **Chỉnh sửa danh mục**: Đổi tên danh mục đã chọn.
* **Xóa danh mục**: Xóa danh mục và tất cả các liên kết của nó.
* **Xuất liên kết**: Lưu tất cả liên kết và danh mục vào tệp `.json`.
* **Nhập liên kết**: Tải các liên kết và danh mục từ tệp `.json`.

#### Trong Danh sách Liên kết

* **Mở liên kết**: Mở liên kết trong trình duyệt bạn đã định cấu hình.
    > **Lưu ý**: Cần phải định cấu hình trước trình duyệt phụ trong cài đặt.
* **Thêm liên kết**: Cho phép chèn URL mới. Tiêu đề sẽ được lấy tự động,nhưng bạn có thể nhập thủ công nếu việc truy xuất không thành công.
* **Chỉnh sửa liên kết**: Sửa đổi tiêu đề và URL của liên kết hiện có.
* **Xóa liên kết**: Xóa liên kết đã chọn.
* **Xuất liên kết** / **Nhập liên kết**: Tương tự như các tùy chọn danh mục.
* **Nhập dấu trang HTML**: Nhập liên kết từ tệp `.html` được trình duyệt xuất.
* **Sắp xếp liên kết**: Sắp xếp các liên kết của danh mục hiện tại theo thứ tự bảng chữ cái.

### Nhập dấu trang HTML

FavoriteLinks cũng cho phép nhập dấu trang trực tiếp từ các tệp HTML, chẳng hạn như các dấu trang được xuất bởi trình duyệt (Chrome, Firefox, Edge, v.v.).

Tính năng này hữu ích để di chuyển dấu trang hiện có của bạn sang tiện ích bổ sung một cách nhanh chóng và có tổ chức.

#### Cách nhập dấu trang từ tệp HTML

1. Mở tiện ích bổ sung **Liên kết yêu thích**.
2. Truy cập menu ngữ cảnh trong **Hộp tổ hợp danh mục** hoặc sử dụng tùy chọn có sẵn trong menu chính.
3. Chọn **Nhập dấu trang HTML**.
4. Chọn tệp `.html` được xuất từ ​​trình duyệt của bạn.
5. Đợi các liên kết được xử lý.

Trong quá trình nhập khẩu:

* Tiến trình được hiển thị trên thanh tiến trình.
* Bạn có thể **hủy thao tác bất kỳ lúc nào**.
* NVDA vẫn phản hồi trong toàn bộ quá trình.

#### Tổ chức các liên kết đã nhập

* Các liên kết đã nhập sẽ tự động được thêm vào tệp JSON được định cấu hình trong tùy chọn tiện ích bổ sung.
* Theo mặc định, dấu trang được chèn vào danh mục **“Dấu trang đã nhập”**.
* Các liên kết trùng lặp (có cùng URL) sẽ không được thêm lại.

Khi kết thúc quá trình nhập, thông báo xác nhận sẽ hiển thị và giao diện tiện ích bổ sung được cập nhật tự động.

### Phím tắt

| Chức năng | Phím tắt |
| :--- | :--- |
| Mở liên kết | `Alt+B` hoặc `Enter` (trong danh sách liên kết) |
| Thêm liên kết | `Alt+A` |
| Thêm danh mục | `Alt+D` |
| Chỉnh sửa liên kết | `Alt+E` hoặc `F2` |
| Xóa liên kết | `Alt+L` hoặc `Del` |
| Lưu URL của trang hiện tại | `Shift+Control+D` |
| Hiển thị URL của trang hiện tại | `Windows+Control+P` Nhấn hai lần sẽ sao chép URL vào khay nhớ tạm. |
| Thoát | `Alt+S`, `Esc` hoặc `Alt+F4` |

## Hộp thoại "Thêm liên kết mới"

1. **Danh mục**: Chọn danh mục mong muốn.
2. **URL**: Dán hoặc nhập địa chỉ liên kết.
    > Nếu bạn đã sao chép một URL, nó sẽ được dán tự động.
3. **OK (`Alt+O`)**: Thêm liên kết.
    > Tiêu đề sẽ được tìm nạp tự động. Nếu việc truy xuất không thành công, bạn sẽ có thể nhập nó theo cách thủ công.
4. **Hủy (`Alt+C`)**: Đóng hộp thoại. `Esc` hoặc `Alt+F4` cũng hoạt động.

## Hộp thoại "Chỉnh sửa liên kết"

1. **Danh mục**: Khi thay đổi danh mục tại đây, liên kết sẽ được chuyển sang danh mục mới.
2. **Tiêu đề**: Chỉnh sửa tiêu đề liên kết.
3. **URL**: Thay đổi địa chỉ liên kết.
4. **OK (`Alt+O`)**: Lưu các thay đổi.
5. **Hủy (`Alt+C`)**: Đóng mà không lưu. `Esc` hoặc `Alt+F4` cũng hoạt động.

## Lời cảm ơn

Đặc biệt cảm ơn **Rue Fontes** và **Ângelo Abrantes** vì các cuộc thử nghiệm đã được thực hiện cũng như những gợi ý có giá trị đã góp phần đáng kể vào việc cải thiện dự án này.Tôi cũng cảm ơn **Abel Passos** vì đã đóng góp chức năng nhập dấu trang từ tệp HTML.

Tiện ích bổ sung FavoriteLinks được phát triển với sự hỗ trợ của **ChatGPT** và **Google Gemini**, được sử dụng để tạo các chức năng, tối ưu hóa và tái cấu trúc mã cũng như cải thiện tài liệu.

## 🌍 Người phiên dịch

* 🇸🇦 **Tiếng Ả Rập** — Ahmed Bakr
* 🇧🇷 **Tiếng Bồ Đào Nha (Brazil)** — Edilberto Fonseca
* 🇵🇹 **Tiếng Bồ Đào Nha (Bồ Đào Nha)** — Edilberto Fonseca
* 🇷🇺 **Tiếng Nga (Nga)** — Valentin Kupriyanov
* 🇹🇷 **Tiếng thổ Nhĩ Kỳ (Thổ Nhĩ Kỳ)** — Umut KORRMAZ
* 🇺🇦 **Tiếng Ukraina (Ukraine)** — Heorhii Halas
* 🇻🇳 **Tiếng Việt** - Hoàng Long