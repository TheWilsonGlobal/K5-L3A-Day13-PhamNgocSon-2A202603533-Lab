"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm cá nhân.

Chạy: python lab13.py
Cần: pandas, numpy, scipy, statsmodels, pyyaml.
Đọc logix_runs.csv và logix_requests.csv từ thư mục cha (repo) hoặc thư mục hiện tại.
Mọi số tính từ cột *_simulated đều là GIẢ LẬP và được in kèm nhãn [sim].
"""
import math
import os
import sys
from statistics import NormalDist

import pandas as pd

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng."""
    return 1 / p if k is None else (1 - (1 - p) ** k) / p


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    return 1.0 if k is None else 1 - (1 - p) ** k


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy."""
    return so_lan_chay_ky_vong(p, k) / ti_le_thanh_cong(p, k)


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
def mo_hinh(runs, reqs, gia_vao=GIA_VAO, gia_ra=GIA_RA, gia_tool=GIA_TOOL, luong_phut=LUONG_PHUT,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, chay_lai, xem_lai, lam_lai, tong, thanh_cong, cps, hoa_don_moi_yc.
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi.
    - xem_lai, lam_lai: số phút (cột *_simulated) × luong_phut. Đây là số GIẢ LẬP.
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong'.
    - max_lan_chay (B1, B3): bỏ lần chạy có attempt > giới hạn; yêu cầu vượt giới hạn
      thành chuyen_nhan_vien và phút xem lại, làm lại bằng 0.
    """
    reqs = reqs.copy()
    runs = runs[runs['request_id'].isin(reqs['request_id'])]
    if max_lan_chay is not None:
        runs = runs[runs['attempt'] <= max_lan_chay]
        vuot = reqs['so_lan_chay'] > max_lan_chay
        reqs.loc[vuot, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0
    tien_token = runs['tokens_in'] / 1000 * gia_vao + runs['tokens_out'] / 1000 * gia_ra
    tien_tool = runs['tool_calls'] * gia_tool
    xem_lai = reqs['phut_xem_lai_simulated'].sum() * luong_phut * he_so_xem_lai
    lam_lai = reqs['phut_lam_lai_simulated'].sum() * luong_phut * he_so_lam_lai
    tong = tien_token.sum() + tien_tool.sum() + xem_lai + lam_lai
    thanh_cong = int((reqs['ket_qua'] == 'thanh_cong').sum())
    assert thanh_cong > 0
    return dict(token=tien_token.sum(), tool=tien_tool.sum(),
                chay_lai=(tien_token + tien_tool)[runs['attempt'] > 1].sum(),
                xem_lai=xem_lai, lam_lai=lam_lai, tong=tong,
                thanh_cong=thanh_cong, cps=tong / thanh_cong,
                hoa_don_moi_yc=(tien_token.sum() + tien_tool.sum()) / len(reqs))


def in_bang_a2(runs, reqs):
    ket_qua = mo_hinh(runs, reqs)
    print('\n== A2 · Bảng chi phí (token/tool đo từ trace; xem lại, làm lại là [sim]) ==')
    nhan = {
        'token': 'đo từ trace', 'tool': 'đo từ trace', 'chay_lai': 'đo từ trace (attempt > 1)',
        'xem_lai': '[sim]', 'lam_lai': '[sim]', 'tong': 'có phần [sim]',
        'thanh_cong': '', 'cps': '[sim]', 'hoa_don_moi_yc': 'đo từ trace',
    }
    for ten, gia_tri in ket_qua.items():
        print(f'{ten:16s} {gia_tri:>16,.2f}   {nhan[ten]}')
    return ket_qua


# ---------- Nhiệm vụ A3 · Tách theo loại yêu cầu ----------
def bang_a3(runs, reqs):
    print('\n== A3 · Theo loại yêu cầu ==')
    print(f"{'loai':10s} {'n':>5s} {'tyle_tc':>8s} {'lan/yc':>7s} {'cps[sim]':>10s} {'so 12k':>7s}")
    ket = {}
    for loai in ['noi_dia', 'hang_nang', 'quoc_te', 'doi_tac']:
        con = reqs[reqs.loai == loai]
        m = mo_hinh(runs, con)
        so_yc = len(con)
        tyle = m['thanh_cong'] / so_yc
        lan = len(runs[runs.request_id.isin(con.request_id)]) / so_yc
        ket[loai] = dict(n=so_yc, tyle=tyle, lan=lan, cps=m['cps'], so_12k=m['cps'] / BASELINE)
        print(f"{loai:10s} {so_yc:5d} {tyle*100:7.1f}% {lan:7.2f} {m['cps']:10,.0f} {m['cps']/BASELINE:6.2f}x")
    # Tỉ lệ ok theo từng lần thử, theo loại
    gop = runs.merge(reqs[['request_id', 'loai']], on='request_id')
    bang = gop.pivot_table(index='loai', columns='attempt', values='status',
                           aggfunc=lambda s: (s == 'ok').mean())
    print('\nTỉ lệ ok theo lần thử (mỗi lần chạy):')
    print((bang * 100).round(1).to_string())
    return ket


# ---------- Nhiệm vụ B · Bảng độ nhạy ----------
KICH_BAN = {
    'Giá token gấp đôi':        dict(gia_vao=52, gia_ra=260),
    'Giá token giảm một nửa':   dict(gia_vao=13, gia_ra=65),
    'Xem lại gấp đôi':          dict(he_so_xem_lai=2),
    'Xem lại giảm một nửa':     dict(he_so_xem_lai=0.5),
    'Làm lại gấp đôi':          dict(he_so_lam_lai=2),
    'Làm lại giảm một nửa':     dict(he_so_lam_lai=0.5),
    'Lương tăng 25%':           dict(luong_phut=2500),
    'Tối đa 2 lần chạy':        dict(max_lan_chay=2),
    'Chỉ 1 lần chạy':           dict(max_lan_chay=1),
}


def bang_b1(runs, reqs):
    print('\n== B1 · Đổi từng yếu tố ==')
    goc = mo_hinh(runs, reqs)['cps']
    ket = {'Gốc (A2)': goc}
    print(f"{'Gốc (A2)':25s} {goc:8,.0f} [sim]")
    for ten, kw in KICH_BAN.items():
        cps = mo_hinh(runs, reqs, **kw)['cps']
        ket[ten] = cps
        print(f'{ten:25s} {cps:8,.0f} {(cps / goc - 1) * 100:+6.1f}%')
    # Kiểm tự động: giảm một nửa phải bằng đúng nửa mức tăng của gấp đôi
    for ten_tang, ten_giam in [('Xem lại gấp đôi', 'Xem lại giảm một nửa'),
                               ('Làm lại gấp đôi', 'Làm lại giảm một nửa'),
                               ('Giá token gấp đôi', 'Giá token giảm một nửa')]:
        tang = ket[ten_tang] / goc - 1
        giam = ket[ten_giam] / goc - 1
        print(f'  kiểm đối xứng {ten_tang}: tăng {tang*100:+.2f}%, giảm {ten_giam}: {giam*100:+.2f}%')
    return ket


def bang_b2_b3_b4(runs, reqs):
    print('\n== B2 · Đổi một cặp ==')
    goc = mo_hinh(runs, reqs)['cps']
    cap = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2)['cps']
    rieng_gia = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260)['cps'] - goc
    rieng_xem = mo_hinh(runs, reqs, he_so_xem_lai=2)['cps'] - goc
    print(f'Giá token ×2 + xem lại ×2: {cap:,.0f} ({(cap/goc-1)*100:+.1f}%); '
          f'cộng hai tác động riêng: {goc + rieng_gia + rieng_xem:,.0f}; '
          f'tuyến tính: {abs(cap - (goc + rieng_gia + rieng_xem)) < 1e-6}')

    print('\n== B3 · Giới hạn chạy lại (chi phí cả hệ thống) ==')
    print(f"{'Giới hạn':>9s} {'Tổng trợ lý[sim]':>18s} {'Không TC':>9s} {'Cả hệ thống[sim]':>18s} {'cps[sim]':>10s}")
    b3 = {}
    for gioi_han in [1, 2, 3]:
        m = mo_hinh(runs, reqs, max_lan_chay=gioi_han)
        khong_tc = len(reqs) - m['thanh_cong']
        he_thong = m['tong'] + BASELINE * khong_tc
        b3[gioi_han] = dict(tong=m['tong'], khong_tc=khong_tc, he_thong=he_thong, cps=m['cps'])
        print(f"{gioi_han:>9d} {m['tong']:18,.0f} {khong_tc:9d} {he_thong:18,.0f} {m['cps']:10,.0f}")
    re_nhat = min(b3, key=lambda g: b3[g]['he_thong'])
    print(f"Rẻ nhất cho công ty: giới hạn {re_nhat}; cps thấp nhất: giới hạn "
          f"{min(b3, key=lambda g: b3[g]['cps'])}")
    return b3


def bang_b4(runs, reqs):
    print('\n== B4 · Xem lại 100% (noi_dia + hang_nang) ==')
    con = reqs[reqs.loai.isin(['noi_dia', 'hang_nang'])]
    runs_con = runs[runs.request_id.isin(con.request_id)]
    co_ok = runs_con[runs_con.status == 'ok'].request_id.nunique()
    xem = co_ok * 5 * LUONG_PHUT
    lam = (con.ket_qua == 'lam_lai').sum() * 9 * LUONG_PHUT
    token_tool = (runs_con.tokens_in / 1000 * GIA_VAO + runs_con.tokens_out / 1000 * GIA_RA
                  + runs_con.tool_calls * GIA_TOOL).sum()
    tong = xem + lam + token_tool
    thanh_cong = int((con.ket_qua == 'thanh_cong').sum())
    cps = tong / thanh_cong
    print(f'yêu cầu: {len(con)}; có lần chạy ok: {co_ok} → xem lại {xem:,.0f} đ [sim]')
    print(f'ca làm lại: {(con.ket_qua == "lam_lai").sum()} → {lam:,.0f} đ [sim]')
    print(f'token + tool: {token_tool:,.0f} đ; tổng {tong:,.0f} đ; việc thành công {thanh_cong}')
    print(f'chi phí mỗi việc thành công: {cps:,.0f} đ [sim] = {cps/BASELINE:.2f}x của 12.000 đ')
    return dict(cps=cps, xem=xem, lam=lam, token_tool=token_tool, thanh_cong=thanh_cong)


# ---------- Nhiệm vụ D1 · Cỡ mẫu ----------
def co_mau(p1, p2, alpha=0.05, power=0.8):
    """Cỡ mẫu mỗi nhóm để so sánh hai tỉ lệ (công thức hai mẫu độc lập)."""
    za = NormalDist().inv_cdf(1 - alpha / 2)
    zb = NormalDist().inv_cdf(power)
    pb = (p1 + p2) / 2
    return math.ceil((za * math.sqrt(2 * pb * (1 - pb))
                      + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2)


def design_effect(m, icc=0.02):
    return 1 + (m - 1) * icc


def bang_d1():
    print('\n== D1 · Cỡ mẫu ==')
    icc = 0.02
    a = co_mau(0.70, 0.75)
    print(f'a · chia theo yêu cầu: {a} yêu cầu mỗi nhóm')
    m_b = 75
    de_b = design_effect(m_b, icc)
    n_b = math.ceil(a * de_b)
    nguoi_b = math.ceil(n_b / m_b) * 2
    print(f'b · theo nhân viên, m={m_b}: DE={de_b:.2f}, n={n_b} mỗi nhóm → {math.ceil(n_b/m_b)} người mỗi nhóm, tổng {nguoi_b} người')
    c_max = 20 / icc
    print(f'c · 20 nhân viên mỗi nhóm: tối đa {c_max:.0f} yêu cầu mỗi nhóm; đạt {c_max >= a}')
    d_max = 6 / icc
    print(f'd · 6 depot mỗi nhóm: tối đa {d_max:.0f} yêu cầu mỗi nhóm')
    n_e = co_mau(0.70, 0.76)
    m_e = next(m for m in range(1, 10000) if 20 * m >= n_e * design_effect(m, icc))
    print(f'e · chênh 6 điểm: n={n_e} mỗi nhóm; 20 người mỗi nhóm cần m ≥ {m_e} '
          f'(DE {design_effect(m_e, icc):.2f})')
    # Power của mức chênh 5 điểm khi n = 859 (kiểm bằng statsmodels nếu có)
    try:
        from statsmodels.stats.proportion import proportion_effectsize
        from statsmodels.stats.power import NormalIndPower
        eff = proportion_effectsize(0.75, 0.70)
        pw = NormalIndPower().power(effect_size=eff, nobs1=859, alpha=0.05, ratio=1)
        print(f'power khi tác động thật 5 điểm, n=859: {pw:.3f}')
    except ImportError:
        pass
    return dict(a=a, n_b=n_b, nguoi_b=nguoi_b, c_max=c_max, d_max=d_max, n_e=n_e, m_e=m_e)


# ---------- Nhiệm vụ E1 · Chỉ số ----------
def chi_so(reqs):
    print('\n== E1 · Chỉ số (1.200 yêu cầu) ==')
    chinh = ((reqs.dong_trong_24h == 1) & (reqs.mo_lai_trong_7_ngay == 0)).mean()
    xem = reqs[reqs.duoc_xem_lai == 1]
    bo_qua = xem.quyet_dinh_xem_lai.isin(['sua', 'bo']).mean()
    an_toan = (reqs.mo_lai_trong_7_ngay == 1).mean()
    n_dung = int(((reqs.dong_trong_24h == 1) & (reqs.mo_lai_trong_7_ngay == 0)).sum())
    print(f'chính: {chinh*100:.2f}% ({n_dung}/{len(reqs)})')
    print(f'dùng (bỏ qua gợi ý): {bo_qua*100:.2f}% ({xem.quyet_dinh_xem_lai.isin(["sua","bo"]).sum()}/{len(xem)})')
    print(f'an toàn (mở lại 7 ngày): {an_toan*100:.2f}% ({(reqs.mo_lai_trong_7_ngay==1).sum()}/{len(reqs)})')
    print(f"tỉ lệ mở lại theo loại noi_dia+hang_nang: "
          f"{reqs[reqs.loai.isin(['noi_dia','hang_nang'])].mo_lai_trong_7_ngay.mean()*100:.2f}%")
    return dict(chinh=chinh, bo_qua=bo_qua, an_toan=an_toan)


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')  # console Windows mặc định cp1252
    except AttributeError:
        pass
    here = os.path.dirname(os.path.abspath(__file__))
    thu_muc = next(d for d in [os.getcwd(), here, os.path.dirname(here)]
                   if os.path.exists(os.path.join(d, 'logix_runs.csv')))
    runs = pd.read_csv(os.path.join(thu_muc, 'logix_runs.csv'))
    reqs = pd.read_csv(os.path.join(thu_muc, 'logix_requests.csv'), keep_default_na=False)
    print(f'Dữ liệu: {thu_muc}; {len(runs)} lần chạy, {len(reqs)} yêu cầu')
    kiem_tra_dap_an_biet_truoc()
    in_bang_a2(runs, reqs)
    bang_a3(runs, reqs)
    bang_b1(runs, reqs)
    bang_b2_b3_b4(runs, reqs)
    bang_b4(runs, reqs)
    bang_d1()
    chi_so(reqs)
    return 0


if __name__ == '__main__':
    sys.exit(main())
