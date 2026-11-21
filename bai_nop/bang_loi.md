# Bảng lỗi và cách khắc phục (Nhiệm vụ C)

## Định nghĩa dùng để gắn nhãn (theo Google PAIR)

| Loại | Quy tắc phân biệt |
| --- | --- |
| Do người dùng | Đầu vào hoặc lựa chọn của khách sai. Gốc lỗi nằm ở khách. |
| Hệ thống | Trợ lý làm sai so với thiết kế hoặc chính sách, và sai đã lộ ra. |
| Ngữ cảnh | Trợ lý làm đúng thiết kế, nhưng giả định của thiết kế không khớp hoàn cảnh khách. |
| Giới hạn hệ thống | Không làm được: thiếu dữ liệu, ngoài phạm vi, hoặc dạng đầu vào không xử lý được. |
| Ngầm | Có sai nhưng không ai nhận ra cho tới khi kiểm tra mẫu. |

Quy tắc chung: gắn nhãn theo **nguyên nhân gốc**, không theo chỗ cần sửa.

## Bộ nhãn 1 (gắn độc lập, 20 ca)

| Ca | Loại | Ca | Loại |
| ---: | --- | ---: | --- |
| 1 | Do người dùng | 11 | Giới hạn hệ thống |
| 2 | Hệ thống | 12 | Ngầm |
| 3 | Ngữ cảnh | 13 | Giới hạn hệ thống |
| 4 | Giới hạn hệ thống | 14 | Do người dùng |
| 5 | Ngầm | 15 | Hệ thống |
| 6 | Do người dùng | 16 | Ngữ cảnh |
| 7 | Hệ thống | 17 | Ngầm |
| 8 | Hệ thống | 18 | Ngữ cảnh |
| 9 | Do người dùng | 19 | Giới hạn hệ thống |
| 10 | Ngữ cảnh | 20 | Hệ thống |

## Bộ nhãn 2 và tỉ lệ đồng thuận

**Ghi chú về độc lập:** bài làm này do một người thực hiện. Bộ nhãn 2 là đáp án tham khảo trong hướng dẫn, không phải nhãn của người thứ hai. Tỉ lệ dưới đây **không phải đồng thuận liên người**. Nó chỉ cho biết bộ nhãn 1 khớp đáp án tham khảo, và người làm đã thấy đáp án trước khi gắn nhãn.

- Số ca trùng: **20 / 20 = 100%** (ngưỡng 80%, tức 16/20).
- Không có ca nào cần viết lại định nghĩa.
- Các ca dễ lẫn đã được xử lý theo quy tắc: ca 6 và 9 là do người dùng (gốc lỗi là khách chọn sai mục hoặc nhập sai mã); ca 13 là giới hạn dù trợ lý xử lý kém; ca 8 và 15 là hệ thống vì sai đã lộ ra; ca 18 là ngữ cảnh (số tiền đúng, chỉ cách tính không được ghi); ca 12 là ngầm (chi phí tăng mà không ai thấy).

Muốn có đồng thuận liên người, cần một bạn trong nhóm gắn nhãn 20 ca **trước khi xem** bộ nhãn 1.

## Bảng khắc phục (5 ca, mỗi loại một ca)

| Ca | Loại | Phát hiện bằng gì (đo được) | Khắc phục | Ai phụ trách |
| ---: | --- | --- | --- | --- |
| 9 | Do người dùng | Event `input_validation_failed` với `loai_ma = san_tmdt`; cảnh báo khi > 2% số yêu cầu mỗi ngày | Nhận diện mã đơn sàn thương mại điện tử và tra sang mã vận đơn; không tra được thì hướng dẫn khách kèm ảnh chụp | PM trợ lý hoàn phí |
| 7 | Hệ thống | Đối soát mỗi giờ: tin nhắn "đã hoàn" không có `refund_ledger_write` với `ket_qua = ok` cùng `trace_id`; ngưỡng 0 ca | Chỉ gửi "đã hoàn" khi sổ cái trả `ok`; sau 3 lần lỗi 503 thì gửi "đang xử lý" và chuyển nhân viên | Kỹ sư trưởng agent |
| 18 | Ngữ cảnh | Tỉ lệ yêu cầu mở lại vì số tiền, theo tuần; mục tiêu dưới 1% | Mẫu tin nhắn hoàn tiền luôn ghi cách tính, ví dụ "phí 30.000 đ × 50% = 15.000 đ" | Trưởng nhóm CSKH |
| 19 | Giới hạn hệ thống | Event `handoff_to_staff` với `reason = ngoai_du_lieu_thoi_gian`, theo tuần | Giữ cách chuyển kèm tóm tắt cho nhân viên; ghi chú giới hạn 12 tháng ngay trên màn hình khách | PM trợ lý hoàn phí |
| 17 | Ngầm | Kiểm tra mẫu 100 đơn mỗi tuần so với bảng giá hiện hành; ngưỡng 1% đơn lệch | Xoá bộ nhớ đệm khi có bảng giá mới; ghi phiên bản bảng giá vào trace | Kế toán trưởng |

Năm loại đều có mặt: Do người dùng (9), Hệ thống (7), Ngữ cảnh (18), Giới hạn hệ thống (19), Ngầm (17).
