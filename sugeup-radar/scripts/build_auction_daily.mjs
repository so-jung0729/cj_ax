// 경매 원본(research/data/raw/auction)을 검사하고 일별·산지별 정리본 CSV를 만든다.
// 가격: scsbd_prc는 단량당 낙찰가로 보고 kg당 가격 = scsbd_prc / unit_qty 로 계산한다. 물량: qty × unit_qty (kg만 사용).
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';

const DIR = 'research/data/raw/auction';
const man = JSON.parse(readFileSync(`${DIR}/manifest.json`, 'utf8'));
const loaded = [];
for (const m of man.rows) {
  if (!m.saved) continue;
  for (const l of readFileSync(`${DIR}/${m.date}_${m.key}.jsonl`, 'utf8').split('\n')) {
    if (l) loaded.push({ ...JSON.parse(l), _item: m.item, _key: m.key, _date: m.date });
  }
}
// 같은 경매 건이 수정 시각만 다르게 반복되면 가장 최근 수정본만 남긴다.
const keyOf = r => [r.whsl_mrkt_cd, r.corp_cd, r.auctn_seq, r.spm_no, r.scsbd_dt, r.corp_gds_cd, r.plor_cd, r.scsbd_prc, r.qty].join('|');
const latest = new Map();
for (const r of loaded) { const k = keyOf(r), o = latest.get(k); if (!o || String(r.mdfcn_dt) > String(o.mdfcn_dt)) latest.set(k, r); }
const rows = [...latest.values()];
const num = v => { const n = Number(v); return Number.isFinite(n) ? n : null; };
const qs = (a, p) => { if (!a.length) return null; const s = [...a].sort((x, y) => x - y); return s[Math.min(s.length - 1, Math.floor(p * s.length))]; };
const originClass = raw => {
  const s = String(raw || '').trim().replace(/\s+/g, ' ');
  if (!s || s === '-') return { origin: '', cls: 'blank' };
  const m = s.match(/^(\S+(?:도|시|특별자치도|광역시|특별시))\s+(\S+?[시군구])(\s|$)/);
  if (m) return { origin: `${m[1]} ${m[2]}`, cls: 'sigungu' };
  if (/(도|광역시|특별시|특별자치시)$/.test(s)) return { origin: s, cls: 'sido_only' };
  if (/^[가-힣]+$/.test(s) && !/[시군구동면읍리]$/.test(s)) return { origin: s, cls: 'foreign_or_other' };
  return { origin: s, cls: 'other' };
};

const report = { loaded_rows: loaded.length, duplicates_removed: loaded.length - rows.length, total_rows: rows.length, items: {} };
const daily = new Map(), byOrigin = new Map();
const add = (map, k, base, kg, val, perKg) => { const o = map.get(k) || { ...base, rows: 0, kg: 0, value: 0, _p: [] }; o.rows++; o.kg += kg; o.value += val; o._p.push(perKg); map.set(k, o); };

for (const r of rows) {
  const it = (report.items[r._item] ||= { rows: 0, excluded: { non_kg: 0, bad_number: 0, price_outlier: 0 }, cls: {}, per_kg: [], weights: {} });
  it.rows++;
  const { origin, cls } = originClass(r.plor_nm);
  it.cls[cls] = (it.cls[cls] || 0) + 1;
  const prc = num(r.scsbd_prc), qty = num(r.qty), uq = num(r.unit_qty);
  if (String(r.unit_nm).trim().toLowerCase() !== 'kg') { it.excluded.non_kg++; continue; }
  if (!prc || !qty || !uq || prc <= 0 || qty <= 0 || uq <= 0) { it.excluded.bad_number++; continue; }
  it.per_kg.push(prc / uq);
  r._perKg = prc / uq; r._kg = qty * uq; r._value = prc * qty; r._origin = origin; r._cls = cls;
}
for (const name of Object.keys(report.items)) {
  const it = report.items[name];
  const med = qs(it.per_kg, 0.5);
  it.per_kg_p01 = qs(it.per_kg, 0.01); it.per_kg_median = med; it.per_kg_p99 = qs(it.per_kg, 0.99); it.per_kg_max = Math.max(...it.per_kg); it.per_kg_min = Math.min(...it.per_kg);
  it._lo = med / 10; it._hi = med * 10;
  delete it.per_kg; delete it.weights;
}
for (const r of rows) {
  if (r._perKg == null) continue;
  const it = report.items[r._item];
  if (r._perKg < it._lo || r._perKg > it._hi) { it.excluded.price_outlier++; continue; }
  add(daily, `${r._date}|${r._key}`, { date: r._date, item: r._item }, r._kg, r._value, r._perKg);
  if (r._cls === 'sigungu') add(byOrigin, `${r._date}|${r._key}|${r._origin}`, { date: r._date, item: r._item, origin: r._origin }, r._kg, r._value, r._perKg);
}
const csv = (cols, list) => '﻿' + [cols.join(','), ...list.map(o => cols.map(c => { const v = o[c]; return typeof v === 'string' && /[,"\n]/.test(v) ? `"${v.replace(/"/g, '""')}"` : v; }).join(','))].join('\n') + '\n';
const finish = ({ _p, ...o }) => ({ ...o, kg: Math.round(o.kg), value: Math.round(o.value), price_per_kg: Math.round(o.value / o.kg * 10) / 10, median_price_per_kg: Math.round(qs(_p, 0.5) * 10) / 10 });
const dailyList = [...daily.values()].map(finish).sort((a, b) => a.item.localeCompare(b.item) || a.date.localeCompare(b.date));
const originList = [...byOrigin.values()].map(finish).sort((a, b) => a.item.localeCompare(b.item) || a.date.localeCompare(b.date) || b.kg - a.kg);
mkdirSync('research/data', { recursive: true });
writeFileSync('research/data/auction_item_daily.csv', csv(['date', 'item', 'rows', 'kg', 'value', 'price_per_kg', 'median_price_per_kg'], dailyList));
writeFileSync('research/data/auction_item_origin_daily.csv', csv(['date', 'item', 'origin', 'rows', 'kg', 'value', 'price_per_kg', 'median_price_per_kg'], originList));
report.daily_rows = dailyList.length; report.origin_rows = originList.length;
report.dates_with_data = [...new Set(dailyList.map(x => x.date))];
report.dates_without_data = man.rows.filter(m => !m.saved).map(m => m.date).filter((d, i, a) => a.indexOf(d) === i);
for (const name of Object.keys(report.items)) {
  const it = report.items[name]; delete it._lo; delete it._hi;
  const list = dailyList.filter(x => x.item === name);
  const prices = list.map(x => x.price_per_kg);
  it.daily_price_min = Math.min(...prices); it.daily_price_max = Math.max(...prices);
  it.first_price = list[0]?.price_per_kg; it.last_price = list.at(-1)?.price_per_kg;
  const oTot = {};
  originList.filter(x => x.item === name).forEach(x => { oTot[x.origin] = (oTot[x.origin] || 0) + x.kg; });
  const sum = Object.values(oTot).reduce((a, b) => a + b, 0);
  it.top_origins = Object.entries(oTot).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([k, v]) => [k, Math.round(v / sum * 1000) / 10]);
  it.origin_count = Object.keys(oTot).length;
}
writeFileSync('research/data/raw/auction_quality_report.json', JSON.stringify(report, null, 1));
console.log(JSON.stringify(report));
