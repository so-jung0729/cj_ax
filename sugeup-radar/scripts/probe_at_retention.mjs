// aT 경매 API의 과거 보존 기간과 산지명 품질을 확인한다. 키는 출력하거나 저장하지 않는다.
import { readFileSync, writeFileSync } from 'node:fs';

const KEY = (readFileSync('.env', 'utf8').match(/^DATA_GO_KR_SERVICE_KEY=(.*)$/m) || [])[1]?.trim();
if (!KEY) throw new Error('.env에 키가 없습니다');
const MARKET = '110001';
async function call(params) {
  const q = new URLSearchParams({ serviceKey: KEY, returnType: 'json', ...params });
  const res = await fetch(`https://apis.data.go.kr/B552845/katRealTime2/trades2?${q}`, { signal: AbortSignal.timeout(30000) });
  const j = await res.json();
  const raw = j?.response?.body?.items?.item;
  return { total: j?.response?.body?.totalCount ?? null, code: j?.response?.header?.resultCode, items: Array.isArray(raw) ? raw : raw ? [raw] : [] };
}
const fmt = d => d.toISOString().slice(0, 10);
const out = { market: MARKET, by_date: {} };

// 최근 며칠과 과거 간격을 함께 확인
const today = new Date('2026-11-06T00:00:00Z');
const offsets = [0, 1, 2, 3, 4, 7, 14, 21, 30, 45, 60, 90, 120, 180, 270, 300, 330];
for (const n of offsets) {
  const d = fmt(new Date(today - n * 864e5));
  const r = await call({ pageNo: 1, numOfRows: 1, 'cond[trd_clcln_ymd::EQ]': d, 'cond[whsl_mrkt_cd::EQ]': MARKET });
  out.by_date[d] = r.total;
  console.log(d, r.total);
}

// 가장 최근에 데이터가 있는 날의 표본으로 필드와 산지명 품질 확인
const latest = Object.entries(out.by_date).find(([, t]) => t > 0)?.[0];
out.latest = latest;
if (latest) {
  const rows = [];
  for (let p = 1; p <= 5; p++) {
    const r = await call({ pageNo: p, numOfRows: 1000, 'cond[trd_clcln_ymd::EQ]': latest, 'cond[whsl_mrkt_cd::EQ]': MARKET });
    rows.push(...r.items);
    if (r.items.length < 1000) break;
  }
  const count = key => { const m = {}; for (const x of rows) { const v = x[key] ?? ''; m[v] = (m[v] || 0) + 1; } return Object.entries(m).sort((a, b) => b[1] - a[1]); };
  const plor = count('plor_nm');
  const blankPlor = rows.filter(x => !String(x.plor_nm || '').trim()).length;
  out.sample_rows = rows.length;
  out.items_top = count('gds_mclsf_nm').slice(0, 25);
  out.origin_unique = plor.length;
  out.origin_blank = blankPlor;
  out.origin_top = plor.slice(0, 30);
  out.origin_bottom = plor.slice(-15);
  out.units = count('unit_nm').slice(0, 10);
  out.first_row = rows[0];
  const test = ['감자', '양파', '배추', '무', '콩나물', '숙주', '사과'];
  out.test_items = Object.fromEntries(test.map(t => [t, rows.filter(x => [x.gds_mclsf_nm, x.gds_sclsf_nm, x.corp_gds_item_nm].some(v => String(v || '').includes(t))).length]));
  console.log('표본 행', rows.length, '산지 고유값', plor.length, '산지 빈값', blankPlor);
  console.log('품목 상위', JSON.stringify(out.items_top.slice(0, 15)));
  console.log('산지 상위', JSON.stringify(out.origin_top.slice(0, 20)));
  console.log('산지 하위', JSON.stringify(out.origin_bottom));
  console.log('단위', JSON.stringify(out.units));
  console.log('시험 품목', JSON.stringify(out.test_items));
  console.log('첫 행', JSON.stringify(out.first_row));
}
writeFileSync('research/data/raw/at_retention_report.json', JSON.stringify(out, null, 1).split(KEY).join('[KEY]'));
