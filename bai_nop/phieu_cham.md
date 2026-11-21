# Phiếu chấm hội đồng Gate 2a

> Phiếu này dùng cho phiên **duyệt chéo Gate 2a** và kèm phần **tự chấm hồ sơ của mình** trước khi gửi để đối chiếu đủ 3 tiêu chí hội đồng (30 điểm).

## 1. Phiếu chấm nhóm khác (điền khi duyệt chéo trên lớp)

Nhóm được chấm: ______ · Người ghi phiếu: Phạm Ngọc Sơn (`2A202603533`, vai giữ hồ sơ)

| Tiêu chí | Điểm (0 / 5 / 10) | Bằng chứng trong hồ sơ (ghi số, mục) |
| :--- | :---: | :--- |
| Đề xuất khớp bằng chứng | | |
| Số giả lập và phạm vi | | |
| Pilot ra được quyết định | | |
| **Tổng / 30** | | |

**Quyết định của hội đồng:** Go / Go có điều kiện / No-go. Lý do (1–2 câu, có số):

**Một câu hỏi phản biện cho đội trình hồ sơ:**
- *"Chi phí mỗi việc thành công của nhóm là bao nhiêu nếu tuần đầu phải xem lại 100% (`noi_dia` + `hang_nang`), và so với 12.000 đ khi nhân viên tự làm thì còn tiết kiệm không?"*
- *"Cách chia pilot của nhóm có đủ ít nhất 20 cụm mỗi nhóm không, và nếu tác động thật chỉ là +5 điểm thì power thực tế còn bao nhiêu?"*
- *"Với tỉ lệ mở lại 7 ngày hiện tại là 4,25% (51/1.200), ngưỡng dừng an toàn của nhóm có làm pilot bị dừng ngay trong tuần đầu không?"*

---

## 2. Tự chấm hồ sơ của mình (`ho_so_launch_v0.md` trước khi gửi)

| Tiêu chí | Tự chấm | Bằng chứng & Lý do cụ thể trong hồ sơ |
| :--- | :---: | :--- |
| **Đề xuất khớp bằng chứng** | **10 / 10** | Chọn **Go có điều kiện** cho `noi_dia + hang_nang`; nêu thẳng các con số bất lợi (Mục 3 & B4: xem lại 100% tốn `11.743 đ = 0,98×` [sim] gần như không tiết kiệm; `quoc_te` tốn `22.515 đ = 1,88×` [sim]; Mục 6: chấp nhận MDE `6 điểm` nên nếu tác động thật chỉ `5 điểm` thì power giảm còn `0,642`) kèm 4 điều kiện bắt buộc có vai trò phụ trách trước khi mở bước tiếp theo |
| **Số giả lập và phạm vi** | **10 / 10** | Mọi con số tính từ cột `*_simulated` (Mục 1, 2, 3, 7) đều gắn nhãn `[sim]` / trạng thái `Giả lập` và có cam kết thay bằng số đo thật từ event `staff_review_decision` / `staff_rework_completed` sau tuần 1; không viết "trợ lý đã nâng chỉ số từ 0,70 lên 82,83%" vì đợt chạy thử không có đối chứng; thu hẹp phạm vi về `noi_dia` (`0,22×`) và `hang_nang` (`0,69×`), loại `quoc_te` (`1,88×`) và `doi_tac` (`0,85×`) |
| **Pilot ra được quyết định** | **10 / 10** | Thiết kế thử nghiệm đối chứng đồng thời chia ngẫu nhiên theo cụm nhân viên (`20 + 20` cụm, phân tầng theo depot, `n = 859/nhóm`, `DE = 6,96`, `m ≥ 299` yêu cầu/người); có 3 luật dừng đủ 4 vế (`NẾU – TRONG – THÌ – KHÔNG THÌ`) cho an toàn (so với đối chứng `+2 điểm`, trần `6%` phù hợp mức nền `4,25%`), chi phí (`> 8.000 đ`) và mức dùng (`> 40%` bỏ qua gợi ý), kèm rollback `30 phút` |
| **Tổng cộng** | **30 / 30** | Đạt đủ checklist kỹ thuật và tiêu chí hội đồng Gate 2a |
