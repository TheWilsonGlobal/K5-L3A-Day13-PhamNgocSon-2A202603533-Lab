# Bảng chi phí, độ nhạy và phạm vi pilot (Nhiệm vụ A, B)

> Nguồn: `lab13.py` chạy trên `logix_runs.csv` (1.624 lần chạy) và `logix_requests.csv` (1.200 yêu cầu). Mọi số lấy từ cột `*_simulated` ghi nhãn **[sim]**.

## A1 · Ba phép thử (p = 0,8): ĐẠT

| Phép thử | Kết quả |
| --- | --- |
| Số lần chạy trung bình, tối đa 2 lần | 1,20 |
| Số lần chạy trung bình, chạy đến khi đúng | 1,25 |
| Hệ số chi phí mỗi việc thành công, tối đa 3 lần | 1,25 |

## A2 · Bảng chi phí từ trace

| Khoản | Số tiền (đ) | Nhãn |
| --- | ---: | --- |
| Token (mọi lần chạy) | 245.585 | đo từ trace |
| Tool (5.600 lần gọi) | 84.000 | đo từ trace |
| Trong đó, lần chạy thứ 2 và 3 | 93.804 | đo từ trace |
| Xem lại (890 phút) | 1.780.000 | [sim] |
| Làm lại (1.132 phút) | 2.264.000 | [sim] |
| Tổng chi phí | 4.373.585 | có phần [sim] |
| Số việc thành công (`thanh_cong`) | 978 | |
| **Chi phí mỗi việc thành công** | **4.472** | [sim] |
| Hoá đơn token + tool chia số yêu cầu | 274,7 | đo từ trace |

**Trả lời:**
- Chi phí mỗi việc thành công gấp **16,3 lần** hoá đơn chia số yêu cầu.
- Khoản lớn nhất là **làm lại, 51,8%** [sim], tiếp theo là **xem lại, 40,7%** [sim]. Giờ nhân viên chiếm **92,5%** tổng chi phí [sim].

## A3 · Theo loại yêu cầu

| Loại | Số yêu cầu | Tỉ lệ thành công | Lần chạy / yêu cầu | Chi phí mỗi việc thành công [sim] | So với 12.000 đ |
| --- | ---: | ---: | ---: | ---: | ---: |
| noi_dia | 824 | 95,0% | 1,11 | 2.696 đ | 0,22× |
| hang_nang | 158 | 74,1% | 1,47 | 8.221 đ | 0,69× |
| quoc_te | 150 | 27,3% | 2,32 | 22.515 đ | 1,88× |
| doi_tac | 68 | 54,4% | 1,88 | 10.215 đ | 0,85× |

Tỉ lệ lần chạy `ok` theo lần thử (từ trace):

| Loại | Lần 1 | Lần 2 | Lần 3 |
| --- | ---: | ---: | ---: |
| noi_dia | 91,0% | 75,7% | 38,9% |
| hang_nang | 70,9% | 39,1% | 17,9% |
| quoc_te | 30,0% | 11,4% | 2,2% |
| doi_tac | 51,5% | 18,2% | 14,8% |

**Kết luận:** `quoc_te` không đáng để trợ lý xử lý (1,88×, thành công 27,3%). Chạy lại tới 3 lần không giúp: tỉ lệ đúng giảm từ 30% xuống 2,2%, lỗi lặp lại trên cùng yêu cầu. `doi_tac` sát ngưỡng (0,85×) và có điều khoản riêng, nên loại khỏi pilot.

## B1 · Đổi từng yếu tố (gốc 4.472 đ [sim])

| Kịch bản | Chi phí mỗi việc thành công [sim] | Thay đổi |
| --- | ---: | ---: |
| Giá token gấp đôi (52 / 260) | 4.723 đ | +5,6% |
| Giá token giảm một nửa (13 / 65) | 4.346 đ | −2,8% |
| Tỉ lệ xem lại gấp đôi | 6.292 đ | +40,7% |
| Tỉ lệ xem lại giảm một nửa | 3.562 đ | −20,3% |
| Số ca làm lại gấp đôi | 6.787 đ | +51,8% |
| Số ca làm lại giảm một nửa | 3.315 đ | −25,9% |
| Lương nhân viên tăng 25% | 5.506 đ | +23,1% |
| Chỉ cho chạy tối đa 2 lần | 4.237 đ | −5,2% |
| Chỉ cho chạy 1 lần | 4.111 đ | −8,1% |

Kiểm tự động: kịch bản giảm một nửa bằng đúng nửa mức tăng của kịch bản gấp đôi (5,6 → 2,8; 40,7 → 20,3; 51,8 → 25,9), sai khác do làm tròn.

## B2 · Đổi một cặp và xếp hạng

Giá token gấp đôi cùng xem lại gấp đôi: **6.543 đ [sim] (+46,3%)**, đúng bằng tổng hai tác động riêng vì mô hình tuyến tính.

**Xếp hạng ba yếu tố:** 1. số ca làm lại · 2. tỉ lệ xem lại · 3. lương nhân viên.

## B3 · Giới hạn chạy lại (chi phí cả hệ thống)

Chi phí cả hệ thống = tổng trợ lý + 12.000 đ × yêu cầu không thành công.

| Giới hạn | Tổng trợ lý [sim] | Không thành công | Cả hệ thống [sim] | Chi phí mỗi việc thành công [sim] |
| --- | ---: | ---: | ---: | ---: |
| 1 lần | 3.621.781 đ | 319 | 7.449.781 đ | 4.111 đ (thấp nhất) |
| 2 lần | 4.093.220 đ | 234 | **6.901.220 đ (rẻ nhất)** | 4.237 đ |
| 3 lần | 4.373.585 đ | 222 | 7.037.585 đ | 4.472 đ |

**Trả lời:** giới hạn 2 lần rẻ nhất cho công ty. Nó không trùng với giới hạn cho chi phí mỗi việc thành công thấp nhất (1 lần). Tối ưu riêng chi phí mỗi việc thành công sẽ đẩy thêm 85 yêu cầu sang nhân viên.

## B4 · Nếu phải xem lại tất cả (noi_dia + hang_nang, 982 yêu cầu)

| Bước | Kết quả |
| --- | --- |
| Yêu cầu có ít nhất một lần chạy `ok` (948) × 5 phút × 2.000 đ | 9.480.000 đ [sim] |
| Ca `lam_lai` (48) × 9 phút × 2.000 đ | 864.000 đ [sim] |
| Token + tool của mọi lần chạy thuộc 982 yêu cầu | 224.513 đ |
| Tổng ÷ 900 việc thành công | **11.743 đ [sim] = 0,98×** của 12.000 đ |

**Trả lời:** xem lại 100% thì trợ lý gần như không tiết kiệm, vì tiền xem lại chiếm khoảng 90% chi phí [sim]. Pilot phải học được tỉ lệ xem lại có thể giảm an toàn xuống mức nào, và mỗi lần xem lại có thể ngắn hơn 5 phút không.
