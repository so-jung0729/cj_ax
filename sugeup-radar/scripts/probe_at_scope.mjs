// 보존 경계 날짜, 전국 하루 건수, 시험 품목 코드를 확인한다. 키는 출력하거나 저장하지 않는다.
import { readFileSync, writeFileSync } from 'node:fs';

const KEY = (readFileSync('.env', 'utf8').match(/^DATA_GO_KR_SERVICE_KEY=(.*)$/m) || [])[1]?.trim();
if (!KEY) throw new Error('.env에 키가 없습니다');
const LATEST = '2026-11-05', MARKET = '110001';
let calls = 0;
async function call(params) {
  calls++;
  const q = new URLSearchParams({ serviceKey: KEY, returnType: 'json', ...params });
  const res = await fetch(`https://apis.data.go.kr/B552845/katRealTime2/trades2?${q}`, { signal: AbortSignal.timeout(30000) });
  const j = await res.json();
  const raw = j?.response?.body?.items?.item;
  return { total: j?.response?.body?.totalCount ?? 0, items: Array.isArray(raw) ? raw : raw ? [raw] : [] };
}
const out = {};
const fmt = d => d.toISOString().slice(0, 10);

// 1. 보존 경계: 가락시장 기준으로 있음(10-07)과 없음(09-22) 사이를 찾음. 휴장일을 피하려고 앞뒤 날짜도 함께 봄
let lo = new Date('2026-09-22T00:00:00Z'), hi = new Date('2026-10-07T00:00:00Z');
const seen = {};
while (hi - lo > 864e5) {
  const mid = new Date(lo.getTime() + Math.floor((hi - lo) / 864e5 / 2) * 864e5);
  const r = await call({ numOfRows: 1, 'cond[trd_clcln_ymd::EQ]': fmt(mid), 'cond[whsl_mrkt_cd::EQ]': MARKET });
  seen[fmt(mid)] = r.total;
  if (r.total > 0) hi = mid; else lo = mid;
}
out.retention = { seen, oldest_found: fmt(hi), empty_before: fmt(lo) };
for (let i = 1; i <= 6; i++) {
  const d = fmt(new Date(lo.getTime() - i * 864e5));
  const r = await call({ numOfRows: 1, 'cond[trd_clcln_ymd::EQ]': d, 'cond[whsl_mrkt_cd::EQ]': MARKET });
  seen[d] = r.total;
}
console.log('보존', JSON.stringify(out.retention));

// 2. 전국 하루 건수
const all = await call({ numOfRows: 1, 'cond[trd_clcln_ymd::EQ]': LATEST });
out.national_rows = all.total;
out.calls_needed_per_day_at_1000 = Math.ceil(all.total / 1000);
console.log('전국 하루 건수', LATEST, all.total, '페이지(1000건)', out.calls_needed_per_day_at_1000);

// 3. 대분류 코드 찾기
out.lclsf = {};
for (let c = 1; c <= 12; c++) {
  const code = String(c).padStart(2, '0');
  const r = await call({ numOfRows: 1, 'cond[trd_clcln_ymd::EQ]': LATEST, 'cond[gds_lclsf_cd::EQ]': code });
  if (r.total) out.lclsf[code] = { name: r.items[0]?.gds_lclsf_nm, rows: r.total };
}
console.log('대분류', JSON.stringify(out.lclsf));

// 4. 시험 품목: 코드 번호를 순회해 이름 확인 (대분류별 중분류). 품목명이 맞는 코드와 산지 분포를 기록
const targets = ['감자', '양파', '배추', '무', '콩나물', '숙주'];
out.targets = {};
for (const lc of Object.keys(out.lclsf)) {
  for (let m = 1; m <= 40; m++) {
    if (targets.every(t => out.targets[t])) break;
    const mc = String(m).padStart(2, '0');
    const r = await call({ numOfRows: 1000, 'cond[trd_clcln_ymd::EQ]': LATEST, 'cond[gds_lclsf_cd::EQ]': lc, 'cond[gds_mclsf_cd::EQ]': mc });
    const nm = r.items[0]?.gds_mclsf_nm;
    if (!nm) continue;
    const t = targets.find(x => nm === x || nm.startsWith(x));
    if (t && !out.targets[t]) {
      const count = {};
      for (const x of r.items) { const k = String(x.plor_nm || '').trim(); count[k] = (count[k] || 0) + Number(x.qty || 0) * Number(x.unit_qty || 0); }
      const top = Object.entries(count).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([k, v]) => [k, Math.round(v)]);
      const domestic = r.items.filter(x => /[시군구]$/.test(String(x.plor_nm || '').trim())).length;
      out.targets[t] = { lclsf: lc, mclsf: mc, name: nm, national_rows: r.total, sample_rows: r.items.length, domestic_like: domestic, top_origins_kg_in_sample: top, unit: r.items[0]?.unit_nm };
      console.log(t, JSON.stringify(out.targets[t]));
    }
  }
}
out.calls = calls;
writeFileSync('research/data/raw/at_scope_report.json', JSON.stringify(out, null, 1).split(KEY).join('[KEY]'));
console.log('호출 수', calls);
