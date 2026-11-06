// 경매 원본 폴더를 압축 파일 하나로 묶거나 되돌린다. 다른 컴퓨터로 옮길 때 쓴다.
// 묶기: node scripts/raw_archive.mjs pack
// 복원: node scripts/raw_archive.mjs restore
import { readFileSync, writeFileSync, readdirSync, mkdirSync } from 'node:fs';
import { gzipSync, gunzipSync } from 'node:zlib';

const DIR = 'research/data/raw/auction';
const ARCHIVE = 'research/data/archive/auction_raw_2026-10-06_2026-11-05.json.gz';
const mode = process.argv[2];

if (mode === 'pack') {
  const files = readdirSync(DIR).sort();
  const data = Object.fromEntries(files.map(f => [f, readFileSync(`${DIR}/${f}`, 'utf8')]));
  mkdirSync('research/data/archive', { recursive: true });
  writeFileSync(ARCHIVE, gzipSync(JSON.stringify(data), { level: 9 }));
  console.log('묶음', files.length, '파일');
} else if (mode === 'restore') {
  const data = JSON.parse(gunzipSync(readFileSync(ARCHIVE)).toString('utf8'));
  mkdirSync(DIR, { recursive: true });
  for (const [f, text] of Object.entries(data)) writeFileSync(`${DIR}/${f}`, text);
  console.log('복원', Object.keys(data).length, '파일');
} else {
  throw new Error('pack 또는 restore를 지정하세요');
}
