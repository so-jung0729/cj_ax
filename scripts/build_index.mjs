// 기업별 Day09 원페이지와 Day10 맵을 한 파일(index.html)에 담는다.
// 원본 페이지를 고치면 저장소 루트에서 다시 실행: node scripts/build_index.mjs
import { readFileSync, writeFileSync } from 'node:fs';

const companies = [
  {
    id: 'cj', name: 'CJ프레시웨이', badge: '선정 기업', type: 'B2B 식자재 유통·급식', sales: '3조 4,811억', profit: '1,017억', rival: '현대그린푸드',
    cut: '주문·재구매가 생산자로 가는 경로 미확인', chance: '대구 식당용 7일 시세 전망·보충 알림', score: '3 · 3', fit: '높음', fitNote: '식당이 곧 고객',
    day9: 'research/company/CJ프레시웨이/onepager.html', day10: 'valuechain/valuechain_v1.html',
  },
  {
    id: 'pulmuone', name: '풀무원', type: '식품 제조사', sales: '3조 3,802억', profit: '932억', rival: '오리온',
    cut: '주문·판매가 농가로 가는 경로 미확인', chance: '계약 품목 기상·시세 위험 알림', score: '3 · 2', fit: '일부', fitNote: '외식 채널 비중이 작음',
    day9: 'research/company/풀무원/onepager.html', day10: 'valuechain/풀무원/valuechain_v1.html',
  },
  {
    id: 'kurly', name: '컬리', type: '온라인 식품 플랫폼 + 자체 배송', sales: '2조 3,671억', profit: '131억', rival: '오아시스',
    cut: '수요 예측의 생산자 공유 범위 미확인', chance: '지역 생산자용 시세·제철 출하 리포트', score: '2 · 3', fit: '낮음', fitNote: 'B2C라 고객이 다름',
    day9: 'research/company/컬리/onepager.html', day10: 'valuechain/컬리/valuechain_v1.html',
  },
  {
    id: 'hyundai', name: '현대그린푸드', badge: 'CJ프레시웨이 경쟁사', group: 'rival', type: '단체급식·식자재 유통', sales: '2조 3,296억', profit: '1,068억', rival: 'CJ프레시웨이',
    cut: '식수·주문이 농가로 가는 경로 미확인', chance: '외식 고객용 7일 시세 전망·보충 알림', score: '3 · 3', fit: '중간', fitNote: '외식 고객과 일부 겹침',
    day9: 'research/company/현대그린푸드/onepager.html', day10: 'valuechain/현대그린푸드/valuechain_v1.html',
  },
  {
    id: 'orion', name: '오리온', badge: '풀무원 경쟁사', group: 'rival', type: '제과 제조사', sales: '3조 3,324억', profit: '5,583억', rival: '풀무원',
    cut: '판매가 계약 농가로 가는 경로 미확인', chance: '계약 감자 기상·시세 위험 알림', score: '3 · 2', fit: '낮음', fitNote: '식당이 고객이 아님',
    day9: 'research/company/오리온/onepager.html', day10: 'valuechain/오리온/valuechain_v1.html',
  },
  {
    id: 'oasis', name: '오아시스', badge: '컬리 경쟁사', group: 'rival', type: '온라인 식품 + 직영 매장', sales: '5,645억', profit: '191억', rival: '컬리',
    cut: '수요 예측의 생산자 공유 범위 미확인', chance: '대구·경북 생산자 시세·제철 리포트', score: '2 · 3', fit: '낮음', fitNote: 'B2C라 고객이 다름',
    day9: 'research/company/오아시스/onepager.html', day10: 'valuechain/오아시스/valuechain_v1.html',
  },
];

// 외부 링크는 새 탭으로 열고, 페이지 안 이동(#)은 그대로 둔다.
const linkFix = `<script>document.querySelectorAll('a[href^="http"]').forEach(function(a){a.target='_blank';a.rel='noopener'});</script>`;
const embed = path => readFileSync(path, 'utf8')
  .replace('<html lang="ko">', '<html lang="ko" data-theme="light">')
  .replace('</body>', `${linkFix}</body>`);
const safe = obj => JSON.stringify(obj).replace(/</g, '\\u003c');

const pages = Object.fromEntries(companies.map(c => [c.id, { day9: embed(c.day9), day10: embed(c.day10) }]));
const meta = companies.map(({ id, name, day9, day10 }) => ({ id, name, day9, day10 }));

const cardsOf = list => list.map(c => `
      <a class="co" href="#${c.id}/day9" data-route="${c.id}/day9">
        <span class="top"><b class="name">${c.name}</b>${c.badge ? `<span class="badge${c.group === 'rival' ? ' plain' : ''}">${c.badge}</span>` : ''}</span>
        <span class="type">${c.type}</span>
        <span class="nums"><span><small>2025 매출</small><b>${c.sales}</b></span><span><small>2025 영업이익</small><b>${c.profit}</b></span></span>
        <span class="row"><small>먼저 할 일</small>${c.chance}</span>
        <span class="row"><small>살피와 맞는 정도</small><b>${c.fit}</b> · ${c.fitNote}</span>
        <span class="go">들어가기 →</span>
      </a>`).join('');

const rows = [
  ['유형', 'type'], ['2025 매출', 'sales'], ['2025 영업이익', 'profit'], ['비교 경쟁사', 'rival'],
  ['데이터 단절', 'cut'], ['우선 기회', 'chance'], ['영향 · 실현 (AI 제안)', 'score'], ['살피와 맞는 정도', 'fit'],
].map(([label, key]) => `<tr><th scope="row">${label}</th>${companies.map(c => `<td>${c[key]}</td>`).join('')}</tr>`).join('\n          ');

const html = `<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>기업 리서치 모음</title>
<style>
  :root { color-scheme:light; --ink:#111418; --ink2:#4A5159; --ink3:#6B727A; --line:#E6E8EB; --band:#F5F6F7; --accent:#FFD400; }
  * { box-sizing:border-box; }
  html, body { height:100%; }
  body { margin:0; background:#fff; color:var(--ink); font-family:Pretendard,"Malgun Gothic","Apple SD Gothic Neo","Noto Sans KR",sans-serif; font-size:17px; line-height:1.5; word-break:keep-all; overflow-wrap:anywhere; }
  [hidden] { display:none !important; }
  a { color:inherit; }
  :focus-visible { outline:3px solid #1C64C8; outline-offset:2px; }

  /* 첫 화면 */
  .home { max-width:1280px; margin:0 auto; padding:36px 28px 48px; }
  h1 { margin:0; font-size:32px; line-height:1.3; font-weight:800; letter-spacing:-.03em; }
  .lead { margin:4px 0 24px; font-size:18px; color:var(--ink2); }
  .cos { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; }
  .co { display:flex; flex-direction:column; gap:12px; padding:22px 24px; background:var(--band); border-radius:16px; text-decoration:none; transition:background .12s; }
  .co:hover { background:#ECEEF0; }
  .co .top { display:flex; align-items:center; justify-content:space-between; gap:8px; }
  .co .name { font-size:27px; line-height:1.2; font-weight:800; letter-spacing:-.03em; }
  .badge { flex:none; padding:2px 10px; background:var(--accent); border-radius:99px; font-size:14px; font-weight:800; }
  .badge.plain { background:#E4E6E9; color:#3D444B; font-weight:700; }
  .group { margin:26px 0 10px; font-size:19px; line-height:1.3; font-weight:800; letter-spacing:-.02em; }
  .group:first-of-type { margin-top:0; }
  .co .type { color:var(--ink2); font-size:16px; margin-top:-8px; }
  .nums { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
  .nums b { display:block; font-size:21px; line-height:1.3; font-weight:800; letter-spacing:-.02em; }
  .co small { display:block; font-size:14px; font-weight:700; color:var(--ink3); }
  .row { font-size:16.5px; line-height:1.45; }
  .go { margin-top:auto; padding-top:4px; font-weight:800; }

  h2 { margin:40px 0 12px; font-size:24px; line-height:1.3; font-weight:800; letter-spacing:-.02em; }
  .scroll { overflow-x:auto; }
  table { width:100%; min-width:1160px; border-collapse:collapse; font-size:16px; line-height:1.45; }
  th, td { padding:11px 12px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }
  thead th { font-size:16px; font-weight:800; }
  tbody th { width:130px; font-size:15px; font-weight:700; color:var(--ink2); }
  .opinion { margin:18px 0 0; padding:14px 18px; background:var(--band); border-radius:12px; font-size:16.5px; }
  .foot { margin:18px 0 0; font-size:14px; color:var(--ink3); }

  /* 기업 화면 */
  .company { display:flex; flex-direction:column; height:100%; height:100dvh; }
  .bar { flex:none; display:flex; flex-wrap:wrap; align-items:center; gap:6px 14px; padding:8px 16px; background:var(--ink); color:#fff; }
  .back { color:#fff; font-size:15px; font-weight:700; text-decoration:none; padding:5px 10px; border-radius:8px; white-space:nowrap; }
  .back:hover { background:#2A2F36; }
  .cur { font-size:18px; font-weight:800; white-space:nowrap; }
  .tabs { display:flex; gap:4px; }
  .tab { padding:5px 14px; border-radius:99px; color:#E3E5E8; font-size:15px; font-weight:700; text-decoration:none; white-space:nowrap; }
  .tab:hover { background:#2A2F36; }
  .tab[aria-current="page"] { background:var(--accent); color:var(--ink); }
  .switch { display:flex; gap:4px; margin-left:auto; }
  .switch a { padding:4px 10px; border-radius:8px; color:#C9CDD2; font-size:14px; font-weight:700; text-decoration:none; white-space:nowrap; }
  .switch a:hover { background:#2A2F36; color:#fff; }
  .switch a[aria-current="true"] { color:#fff; box-shadow:inset 0 0 0 1.5px #6B727A; }
  .open { color:#C9CDD2; font-size:14px; font-weight:700; white-space:nowrap; }
  iframe { flex:1; min-height:0; width:100%; border:0; background:#fff; }

  @media (max-width:860px) {
    .home { padding:24px 16px 36px; }
    h1 { font-size:26px; }
    .cos { grid-template-columns:1fr; }
    .switch { margin-left:0; }
    .open { display:none; }
  }
</style>
</head>
<body>

<main class="home" id="home">
  <h1>기업 6곳 리서치와 밸류체인 맵</h1>
  <p class="lead">기업을 누르면 Day 09 원페이지와 Day 10 밸류체인 맵을 볼 수 있어요. 위아래 카드가 서로 경쟁사예요.</p>
  <h2 class="group">후보 기업</h2>
  <nav class="cos" aria-label="후보 기업 선택">${cardsOf(companies.filter(c => c.group !== 'rival'))}
  </nav>
  <h2 class="group">경쟁사</h2>
  <nav class="cos" aria-label="경쟁사 선택">${cardsOf(companies.filter(c => c.group === 'rival'))}
  </nav>

  <h2>여섯 곳 한눈에 비교</h2>
  <div class="scroll"><table>
    <thead><tr><th scope="col">항목</th>${companies.map(c => `<th scope="col">${c.name}</th>`).join('')}</tr></thead>
    <tbody>
          ${rows}
    </tbody>
  </table></div>
  <p class="opinion"><b>AI 의견</b> 살피와 가장 잘 맞는 곳은 CJ프레시웨이이고, 다음이 현대그린푸드예요. 나머지 네 곳은 식당이 아닌 새 고객을 잡아야 해요. 최종 판단은 팀 몫이에요.</p>
  <p class="foot">AX 데이터·서비스 트랙 · 2026-11-06 · 사람 검증 전 · 금액은 공시를 억원으로 환산한 값 · 점수는 AI 제안 · 개인 실습용 자료이며 투자 판단 자료가 아니에요.</p>
</main>

<div class="company" id="company" hidden>
  <header class="bar">
    <a class="back" href="#" data-route="">← 기업 목록</a>
    <span class="cur" id="cur"></span>
    <nav class="tabs" aria-label="일차 선택">
      <a class="tab" id="tab-day9">Day 09 원페이지</a>
      <a class="tab" id="tab-day10">Day 10 밸류체인 맵</a>
    </nav>
    <nav class="switch" id="switch" aria-label="다른 기업"></nav>
    <a class="open" id="open" target="_blank" rel="noopener">이 화면만 크게 ↗</a>
  </header>
  <iframe id="view" title="기업 자료"></iframe>
</div>

<script id="data" type="application/json">${safe(pages)}</script>
<script>
  (function () {
    var meta = ${safe(meta)};
    var pages = JSON.parse(document.getElementById('data').textContent);
    var home = document.getElementById('home'), company = document.getElementById('company');
    var view = document.getElementById('view'), shown = '';
    document.getElementById('switch').innerHTML = meta.map(function (c) { return '<a data-id="' + c.id + '">' + c.name + '</a>'; }).join('');

    function render(route) {
      var parts = route.split('/');
      var c = meta.filter(function (m) { return m.id === parts[0]; })[0];
      var day = parts[1] === 'day10' ? 'day10' : 'day9';
      home.hidden = !!c; company.hidden = !c;
      if (!c) { document.title = '기업 리서치 모음'; window.scrollTo(0, 0); return; }
      document.title = c.name + (day === 'day9' ? ' Day 09' : ' Day 10');
      document.getElementById('cur').textContent = c.name;
      ['day9', 'day10'].forEach(function (d) {
        var t = document.getElementById('tab-' + d);
        t.href = '#' + c.id + '/' + d; t.dataset.route = c.id + '/' + d;
        if (d === day) t.setAttribute('aria-current', 'page'); else t.removeAttribute('aria-current');
      });
      [].forEach.call(document.querySelectorAll('#switch a'), function (a) {
        a.href = '#' + a.dataset.id + '/' + day; a.dataset.route = a.dataset.id + '/' + day;
        a.setAttribute('aria-current', String(a.dataset.id === c.id));
      });
      // htmlpreview로 열었을 때는 원본 페이지도 htmlpreview로 연다.
      var q = location.search.slice(1);
      document.getElementById('open').href = q.indexOf('https://github.com/') === 0 && q.indexOf('/index.html') > 0 ? location.pathname + '?' + q.split('/index.html')[0] + '/' + encodeURI(c[day]) : encodeURI(c[day]);
      var key = c.id + '/' + day;
      if (shown !== key) { view.title = c.name + ' ' + day; view.srcdoc = pages[c.id][day]; shown = key; }
    }
    // 파일을 어떤 방식으로 열어도 동작하도록 클릭을 직접 처리하고, 가능하면 주소에도 남긴다.
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('[data-route]');
      if (!a) return;
      e.preventDefault();
      var route = a.dataset.route;
      render(route);
      try { history.pushState(null, '', '#' + route); } catch (err) { /* data: 주소 등에서는 주소만 안 바뀜 */ }
    });
    window.addEventListener('popstate', function () { render(location.hash.slice(1)); });
    render(location.hash.slice(1));
  })();
</script>
</body>
</html>
`;
writeFileSync('index.html', html, 'utf8');
console.log('index.html', Buffer.byteLength(html), 'bytes');
