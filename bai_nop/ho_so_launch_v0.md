# Hồ sơ launch v0: trợ lý hoàn phí LogiX-VN

Nhóm: cá nhân · Gate 2a · Dữ liệu giả lập · Chỉ duyệt kế hoạch pilot, không duyệt triển khai rộng.

| # | Mục | Con số chính | Trạng thái | Người phụ trách |
| --- | --- | --- | --- | --- |
| 1 | Chi phí mỗi việc thành công | 4.472 đ [sim], gấp 16,3× hoá đơn token chia số yêu cầu; làm lại 51,8% và xem lại 40,7% tổng chi phí [sim] | Giả lập | Kỹ sư trưởng agent |
| 2 | Ba yếu tố nhạy nhất | 1. số ca làm lại (+51,8% khi gấp đôi) · 2. tỉ lệ xem lại (+40,7%) · 3. lương nhân viên (+23,1% khi tăng 25%) [sim] | Giả lập | Kỹ sư trưởng agent |
| 3 | So với nhân viên tự làm | Trợ lý theo loại: noi_dia 0,22×, hang_nang 0,69×, doi_tac 0,85×, quoc_te 1,88× (sim). Khi xem lại 100%: 0,98× [sim] | Giả lập | PM trợ lý hoàn phí |
| 4 | Chỉ số chính, dùng, an toàn | Chính 82,83% (đợt chạy thử, không có đối chứng); dùng: bỏ qua gợi ý 27,12%; an toàn: mở lại 4,25% | Xong, có bằng chứng | Trưởng nhóm CSKH |
| 5 | Bảng lỗi và khắc phục | 20 ca gắn nhãn, khớp đáp án tham khảo 20/20 (không phải đồng thuận liên người); 5 ca khắc phục đủ 5 loại | Chưa (chưa có event đo phát hiện) | PM trợ lý hoàn phí |
| 6 | Pilot plan | Phạm vi noi_dia + hang_nang; cách chia theo nhân viên, 20 + 20 cụm; cỡ mẫu 859 mỗi nhóm; m ≥ 299 yêu cầu mỗi người; power 0,64 nếu tác động thật 5 điểm | Xong, có bằng chứng | Giám đốc vận hành LogiX-VN |
| 7 | Rủi ro kinh tế | Làm lại tăng gấp đôi: 6.787 đ [sim]; xem lại 100%: 0,98× [sim] | Giả lập | Trưởng nhóm CSKH |

## Đề xuất

**Go có điều kiện** cho pilot noi_dia + hang_nang, không mở quoc_te và doi_tac. Điều kiện:

1. Sửa khoá chống trùng và đối soát sổ cái (ca 7, 20) trước ngày bắt đầu. Kỹ sư trưởng agent xác nhận.
2. Giám đốc vận hành ký chấp nhận mức chênh 6 điểm. Ở mức tác động thật 5 điểm, power chỉ khoảng 0,64. Kiểm trước ngày bắt đầu.
3. Bật đủ event có `trace_id`. Thay phút [sim] bằng phút đo thật sau tuần 1. PM trợ lý hoàn phí kiểm.
4. Có kế hoạch giảm xem lại theo bậc, vì xem lại 100% không tiết kiệm (0,98×). Trưởng nhóm CSKH trình trước bước 0,25.

Ngưỡng an toàn so với đối chứng (+2 điểm, trần 6%), không đặt tuyệt đối 3%, vì tỉ lệ mở lại hiện tại là 4,25%.
