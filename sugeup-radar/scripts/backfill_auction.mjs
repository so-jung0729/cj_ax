// aT 경매 API에서 시험 품목의 최근 데이터를 날짜·품목별 원본 파일로 저장한다.
// 이미 받은 날짜는 건너뛰므로 다시 실행해도 안전하다. 키는 출력하거나 저장하지 않는다.
// 실행: 저장소의 sugeup-radar 폴더에서 node scripts/backfill_auction.mjs [시작일] [종료일]
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';

const KEY = (readFileSync('.env', 'utf8').match(/^DATA_GO_KR_SERVICE_KEY=(.*)$/m) || [])[1]?.trim();
if (!KEY) throw new Error('.env에 DATA_GO_KR_SERVICE_KEY가 없습니다');
const START = process.argv[2] || '2026-10-06';
const END = process.argv[3] || '2026-11-05'; // 당일은 경매가 끝나지 않았을 수 있어 기본값에서 제외
const OUT = 'research/data/raw/auction';
mkdirSync(OUT, { recursive: true });
let calls = 0;

async function call(params, tries = 4) {
  for (let i = 1; ; i++) {
    try {
      calls++;
      const q = new URLSearchParams({ serviceKey: KEY, returnType: 'json', ...params });
      const res = await fetch(`https://apis.data.go.kr/B552845/katRealTime2/trades2?${q}`, { signal: AbortSignal.timeout(60000) });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const j = await res.json();
      if (j?.response?.header?.resultCode !== '0') throw new Error(`결과 코드 ${j?.response?.header?.resultCode}`);
      const raw = j.response.body?.items?.item;
      return { total: j.response.body?.totalCount ?? 0, items: Array.isArray(raw) ? raw : raw ? [raw] : [] };
    } catch (e) {
      if (i >= tries) throw new Error(String(e.message).split(KEY).join('[KEY]'));
      await new Promise(r => setTimeout(r, 1500 * i));
    }
  }
}

// 무의 코드는 근채류(11)에서 이름으로 찾는다.
async function findRadish() {
  for (let m = 1; m <= 20; m++) {
    const mc = String(m).padStart(2, '0');
    const r = await call({ numOfRows: 1, 'cond[trd_clcln_ymd::EQ]': END, 'cond[gds_lclsf_cd::EQ]': '11', 'cond[gds_mclsf_cd::EQ]': mc });
    const nm = String(r.items[0]?.gds_mclsf_nm || '').trim();
    if (nm === '무' || nm.startsWith('무(')) return { lc: '11', mc, name: nm };
  }
  return null;
}

const items = [
  { key: 'potato', name: '감자', lc: '05', mc: '01' },
  { key: 'onion', name: '양파', lc: '12', mc: '01' },
  { key: 'cabbage', name: '배추', lc: '10', mc: '01' },
  { key: 'bean_sprout', name: '콩나물', lc: '10', mc: '16' },
  { key: 'mung_sprout', name: '숙주나물', lc: '10', mc: '17' },
];
const radish = await findRadish();
if (radish) items.push({ key: 'radish', ...radish });
console.log('무 코드', radish ? `${radish.lc}/${radish.mc} ${radish.name}` : '찾지 못함');

const dates = [];
for (let d = new Date(`${START}T00:00:00Z`); d <= new Date(`${END}T00:00:00Z`); d = new Date(d.getTime() + 864e5)) dates.push(d.toISOString().slice(0, 10));

const manifest = [];
for (const it of items) {
  for (const date of dates) {
    const file = `${OUT}/${date}_${it.key}.jsonl`;
    const metaFile = `${file}.meta.json`;
    if (existsSync(metaFile)) { manifest.push(JSON.parse(readFileSync(metaFile, 'utf8'))); continue; }
    const base = { 'cond[trd_clcln_ymd::EQ]': date, 'cond[gds_lclsf_cd::EQ]': it.lc, 'cond[gds_mclsf_cd::EQ]': it.mc };
    const rows = [];
    let total = 0;
    for (let p = 1; ; p++) {
      const r = await call({ ...base, pageNo: p, numOfRows: 1000 });
      total = r.total;
      rows.push(...r.items);
      if (r.items.length < 1000 || rows.length >= total) break;
    }
    const uniq = new Set(rows.map(x => `${x.whsl_mrkt_cd}|${x.corp_cd}|${x.auctn_seq}|${x.spm_no}|${x.scsbd_dt}|${x.corp_gds_cd}|${x.plor_cd}|${x.scsbd_prc}|${x.qty}`)).size;
    writeFileSync(file, rows.map(x => JSON.stringify(x)).join('\n') + (rows.length ? '\n' : ''));
    const meta = { date, item: it.name, key: it.key, lclsf: it.lc, mclsf: it.mc, api_total: total, saved: rows.length, unique_rows: uniq, ok: total === rows.length, fetched_at: new Date().toISOString() };
    writeFileSync(metaFile, JSON.stringify(meta));
    manifest.push(meta);
  }
  const m = manifest.filter(x => x.key === it.key);
  console.log(it.name, '날짜', m.length, '건수 있는 날', m.filter(x => x.saved).length, '저장', m.reduce((a, x) => a + x.saved, 0), '불일치', m.filter(x => !x.ok).length);
}
writeFileSync(`${OUT}/manifest.json`, JSON.stringify({ start: START, end: END, source: 'https://www.data.go.kr/data/15141808/openapi.do', items, rows: manifest }, null, 1));
console.log('호출 수', calls, '불일치 합계', manifest.filter(x => !x.ok).length);
