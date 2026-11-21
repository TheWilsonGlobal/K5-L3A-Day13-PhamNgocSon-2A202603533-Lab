# Đặc tả chỉ số, danh sách event và rủi ro kinh tế (Nhiệm vụ E)

## E1 · Đặc tả chỉ số

Tính trên 1.200 yêu cầu trong đợt chạy thử (không có nhóm đối chứng).

| Loại | Chỉ số | Công thức | Giá trị thử |
| --- | --- | --- | --- |
| Chính | % đóng trong 24 giờ và không mở lại trong 7 ngày | `mean((dong_trong_24h == 1) & (mo_lai_trong_7_ngay == 0))` | 82,83% (994/1.200) |
| Dùng | Tỉ lệ bỏ qua gợi ý | `(sua + bo) / số yêu cầu có duoc_xem_lai = 1` | 27,12% (48/177) |
| An toàn | Tỉ lệ lỗi lọt đến khách: mở lại trong 7 ngày | `mean(mo_lai_trong_7_ngay == 1)` | 4,25% (51/1.200) |
| Dùng (tự đề xuất) | % yêu cầu của nhóm can thiệp được mở bằng trợ lý | `count(distinct request_id có agent_suggestion_shown) / yêu cầu nhóm can thiệp` | chưa đo, không có dữ liệu nhóm can thiệp |
| An toàn (tự đề xuất) | % đơn hoàn sai tiền qua kiểm tra mẫu hằng tuần | `so đơn sai / số đơn kiểm tra` từ `audit_sample_checked` | chưa đo, chưa có event |

Ghi chú: chỉ số trong đợt chạy thử là 82,83%. Không viết rằng trợ lý đã nâng chỉ số từ 0,70, vì đợt chạy thử không có nhóm đối chứng.

## Danh sách event (10 event, đều có `trace_id`)

| Event | Ai tạo | Thuộc tính chính | Thời điểm | Chỉ số dùng |
| --- | --- | --- | --- | --- |
| `refund_request_created` | App khách | request_id, loai, so_tien, arm, trace_id | Khi khách gửi | mẫu số của mọi chỉ số |
| `agent_run_completed` | Agent | attempt, tokens_in, tokens_out, tool_calls, status, trace_id | Sau mỗi lần chạy, kể cả lỗi | chi phí A2, B |
| `agent_suggestion_shown` | Giao diện nhân viên | staff_id, so_tien_de_xuat, trace_id | Khi gợi ý hiện ra | Dùng (tự đề xuất) |
| `staff_review_decision` | Nhân viên | giu / sua / bo, phut_xem_lai (đo thật), trace_id | Khi bấm gửi, sửa hoặc bỏ | Dùng; thay phút [sim] |
| `staff_rework_completed` | Nhân viên | phut_lam_lai (đo thật), ly_do, trace_id | Khi làm lại xong | thay phút [sim] làm lại |
| `refund_ledger_write` | Dịch vụ sổ cái | idempotency_key, so_tien, ket_qua, trace_id | Khi ghi sổ | đối soát ca 7, 20 |
| `handoff_to_staff` | Agent | reason, tom_tat, trace_id | Khi chuyển nhân viên | rủi ro giới hạn (ca 4, 19) |
| `ticket_closed` | Hệ thống ticket | closed_at, trace_id | Khi đóng | Chính |
| `ticket_reopened` | Khách | reopened_at, reason, trace_id | Khi mở lại | An toàn |
| `audit_sample_checked` | Kế toán | so_tien_da_hoan, so_tien_dung, trace_id | Hằng tuần | An toàn (tự đề xuất), ca 17 |

**Kiểm tra chéo:** cả ba chỉ số đều tính được từ event (`ticket_closed`, `ticket_reopened`, `staff_review_decision`). Hai chỉ số tự đề xuất cần `agent_suggestion_shown` và `audit_sample_checked`, đều có trong danh sách.

## E2 · Rủi ro kinh tế

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động | Người phụ trách |
| --- | --- | --- | --- | --- |
| Số ca làm lại tăng gấp đôi | +51,8%, lên 6.787 đ/việc thành công [sim] | Tỉ lệ làm lại theo tuần > 7% (đợt chạy thử: 4,9% trong phạm vi noi_dia + hang_nang) | Thu hẹp về noi_dia, rà 20 trace làm lại | PM trợ lý hoàn phí |
| Phải xem lại 100% kéo dài | 11.743 đ/việc thành công = 0,98× nhân viên tự làm [sim] | % yêu cầu được xem lại còn > 50% sau bước 0,25 | Giảm xem lại theo bậc khi tỉ lệ sửa + bỏ < 15% | Trưởng nhóm CSKH |

Ghi chú: 4,9% = 48 ca `lam_lai` / 982 yêu cầu noi_dia + hang_nang, tính từ `logix_requests.csv`. Các con số tính từ cột `_simulated` đều thuộc [sim].
