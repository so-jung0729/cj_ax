// aT 경매·정산 API 시험 호출. 키는 .env에서 읽고 출력하거나 저장하지 않는다.
// 실행: 저장소 루트에서 node scripts/probe_at.mjs
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';

const env = readFileSync('.env', 'utf8');
const KEY = (env.match(/^DATA_GO_KR_SERVICE_KEY=(.*)$/m) || [])[1]?.trim();
if (!KEY) throw new Error('.env에 DATA_GO_KR_SERVICE_KEY가 없습니다');
const clean = s => String(s).split(KEY).join('[KEY]');
let calls = 0;

async function call(base, path, params) {
  const q = new URLSearchParams({ serviceKey: KEY, returnType: 'json', ...params });
  calls++;
  const res = await fetch(`https://apis.data.go.kr/B552845/${base}/${path}?${q}`, { signal: AbortSignal.timeout(30000) });
  const text = await res.text();
  let json = null;
  try { json = JSON.parse(text); } catch { /* XML 오류 응답 등 */ }
  const body = json?.response?.body;
  const header = json?.response?.header;
  const raw = body?.items?.item;
  return {
    http: res.status,
    code: header?.resultCode ?? null,
    msg: header?.resultMsg ?? (json ? null : clean(text).slice(0, 160)),
    total: body?.totalCount ?? null,
    items: Array.isArray(raw) ? raw : raw ? [raw] : [],
  };
}
const brief = r => ({ http: r.http, code: r.code, msg: r.msg, total: r.total, rows: r.items.length });

mkdirSync('research/data/raw', { recursive: true });
const report = {};

// 1. 경매 정보: 조건 없이 최신 표본
const a = await call('katRealTime2', 'trades2', { pageNo: 1, numOfRows: 100 });
report.auction_latest = brief(a);
console.log('경매 최신', brief(a));
if (a.items[0]) {
  writeFileSync('research/data/raw/at_auction_sample.json', clean(JSON.stringify(a.items.slice(0, 100), null, 1)));
  console.log('필드', Object.keys(a.items[0]).join(','));
  const pick = ({ trd_clcln_ymd, scsbd_dt, whsl_mrkt_cd, whsl_mrkt_nm, gds_mclsf_nm, gds_sclsf_nm, plor_cd, plor_nm, scsbd_prc, qty, unit_qty, unit_nm }) => ({ trd_clcln_ymd, scsbd_dt, whsl_mrkt_cd, whsl_mrkt_nm, gds_mclsf_nm, gds_sclsf_nm, plor_cd, plor_nm, scsbd_prc, qty, unit_qty, unit_nm });
  console.log('표본', JSON.stringify(a.items.slice(0, 3).map(pick)));
  console.log('시장', [...new Set(a.items.map(x => `${x.whsl_mrkt_cd}:${x.whsl_mrkt_nm}`))].slice(0, 8).join(' | '));
}

// 2. 정산 정보: 날짜를 거슬러 가며 제공 기간 확인. 가락시장 코드는 경매 표본에서 찾고, 없으면 첫 시장을 사용.
const garak = a.items.find(x => (x.whsl_mrkt_nm || '').includes('가락'))?.whsl_mrkt_cd || a.items[0]?.whsl_mrkt_cd || '110001';
report.market = garak;
console.log('시험 시장 코드', garak);
const dates = ['2026-11-05', '2026-11-04', '2026-06-02', '2025-11-04', '2025-06-03', '2025-01-07', '2024-06-04', '2024-01-09', '2023-06-07', '2022-06-07', '2020-06-02'];
report.sale_by_date = {};
for (const d of dates) {
  const r = await call('katSale', 'trades', { pageNo: 1, numOfRows: 5, 'cond[trd_clcln_ymd::EQ]': d, 'cond[whsl_mrkt_cd::EQ]': garak });
  report.sale_by_date[d] = brief(r);
  console.log('정산', d, JSON.stringify(brief(r)));
  if (r.items[0] && !report.sale_sample) report.sale_sample = r.items.slice(0, 3);
}
report.auction_by_date = {};
for (const d of ['2026-11-05', '2025-11-04', '2025-01-07', '2024-01-09']) {
  const r = await call('katRealTime2', 'trades2', { pageNo: 1, numOfRows: 5, 'cond[trd_clcln_ymd::EQ]': d, 'cond[whsl_mrkt_cd::EQ]': garak });
  report.auction_by_date[d] = brief(r);
  console.log('경매', d, JSON.stringify(brief(r)));
}
report.calls = calls;
report.checked_at = new Date().toISOString();
writeFileSync('research/data/raw/at_probe_report.json', clean(JSON.stringify(report, null, 1)));
if (report.sale_sample) console.log('정산 표본', clean(JSON.stringify(report.sale_sample[0])));
console.log('호출 수', calls);
