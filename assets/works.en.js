// 작품 목록의 영어 글 — 영어판(/en/)만 works.js 다음에 불러온다. 한 줄이 작품 하나(works.js의 id와 짝).
// 그림 · 주소 · 갈래는 works.js 한 곳에 두고, 여기에는 보이는 글(title · line · value · meta · award · alt · pair · links)만 둔다.
// 여기에 없는 작품이나 칸은 works.js의 한국어 글을 그대로 쓴다.
window.WORKS_EN = {
  archi: { line: 'A Claude Code skill that reads your code and docs and draws one architecture board', value: 'Now I can lay out a system plan as one picture.', meta: 'Solo · Open-source skill (MIT) · Engine v1.6', href: '/en/work/archi-board/', alt: 'Back of the archi-board sample board: object maps and flowcharts linked across several panels' },
  floe: { line: 'A desktop app that helps people who code with AI see it through to the end', value: 'Helps people who stall halfway through AI coding keep going.', meta: 'Team lead · Project lead · AI integration (team of 5)', href: '/en/work/floe/', alt: 'Floe workspace: task columns for step 3, and a navy panel where Floro explains the current step' },
  dotci: { line: 'A web app for new students: arrive at a campus spot and a note from an older student opens', value: 'New students get to know a strange campus, one note at a time.', meta: 'System QA · Visual design · Presentation (team of 3)', href: '/en/work/dotci/', pair: [['/assets/img/dotci-map.webp', 'DOTCI map: a dot on each campus building with its note count'], ['/assets/img/dotci-opened.webp', 'DOTCI with a note opened at Woosong Library']] },
  mini: { line: 'A class project shop for practicing the problems vibe coding creates', value: 'Hands-on practice with what goes wrong in a vibe-coded online shop.', meta: 'Slides and script, user-side checks · 110 team tests passing', href: '/en/work/minimall/', alt: 'MiniMall product list: a search box, then “All products 4”' },
  'g-final': { title: 'Grand final poster', meta: 'Gyeongsang LoL Cup #1 · Dec 7, 2022', alt: 'Grand final poster: red and blue light above and below on crumpled black paper, “경상롤드컵 THE GRAND FINAL” in the middle, “GAME DAY 2022. 12. 07” below' },
  'g-offline': { title: 'Final-day screen OFFLINE', meta: 'Gyeongsang LoL Cup #1 · Dec 7, 2022', alt: 'Broadcast screen from the final: white “OFF” and outlined “LINE” on black paper, yellow brush lettering “VICTORY · MVP · WIN” on the right' },
  'g-vs': { title: 'Broadcast screen 1 VS 1', line: 'The 1-vs-1 score screen for the stream', meta: 'Gyeongsang LoL Cup #1 · Oct 22 – 23, 2022', alt: 'Stream screen: “2022 경상롤드컵” and the dates over a blue castle and clouds, a 1 VS 1 score bar in the middle' },
  'g-players': { title: 'Player intro screen', line: "Introduces each team's five players and their roles", meta: 'Gyeongsang LoL Cup #1 · 2022', alt: 'Player intro screen: team name “4 PLATINUM 1 SILBER” over a night sky, five gold-framed cards labeled TOP · JUG · MID · ADC · SUP. Faces, names, numbers and the teacher’s name are blurred.' },
  'g-recruit': { title: 'Sign-up poster', line: 'Call for esports tournament players', meta: 'Gyeongsang LoL Cup #1 · Oct 22 – 23, 2022', alt: 'Top of the sign-up poster: 1st Gyeongsang High School Principal’s Cup Esports Tournament, 2022 경상롤드컵, Oct 22 – 23, 2022, 9 a.m., total prize 1,000,000 won' },
  'v-school': { title: '2022 Gyeongsang High School promo video' },
  'v-2022': { title: '2022 Gyeongsang LoL Cup opening video' },
  'v-2021': { title: '2021 Gyeongsang LoL Cup opening video' },
  'v-switch': { title: 'Gyeongsang LoL Cup transition video for middle schoolers' },
  'v-2020': { title: '2020 Gyeongsang LoL Cup opening video' },
  'v-koreaming': { title: 'Editing for the gaming channel Koreaming', line: "Edited a friend's gaming videos and ran two channels, YouTube and Instagram", value: 'For six months I tested whether my editing and planning worked on real viewers.', meta: 'Editing · Channel management · Feb – Aug 2026', href: '/en/work/koreaming/', links: [{ name: 'YouTube channel', label: 'Koreaming · youtube.com/@koreaming', url: 'https://www.youtube.com/@koreaming' }, { name: 'Instagram', label: 'Koreaming', url: '' }] },
  'v-exam': { title: 'Good-luck video for the college entrance exam' },
  'v-grad': { title: 'Graduation video' },
};
window.KINDS_EN = { dev: 'Development', graphic: 'Graphics', video: 'Video' };
window.AWARDS_EN = {
  dotci: { rank: '1st place', name: '2026 Creative Convergence Collaborative Learning Competition', host: 'Woosong University' },
  floe: { rank: 'Excellence Award, finals (Hannam Univ. HUSS Director’s Award)', name: '2026 Daejeon Startup One Club AI Vibe Coding Idea Competition', host: 'Hannam University HUSS' },
};
window.AWARD_SCOPES_EN = { in: 'On-campus', out: 'External' };

// 짝 맞추기: 같은 id의 영어 칸을 덮어쓴다. links의 주소는 works.js 쪽을 따른다(주소는 한 곳).
WORKS.forEach(w => {
  const e = WORKS_EN[w.id]; if (!e) return;
  const links = e.links && w.links ? e.links.map((l, i) => ({ ...l, url: (w.links[i] || {}).url || '' })) : w.links;
  Object.assign(w, e, { links });
});
Object.assign(KINDS, KINDS_EN);
(window.AWARDS || []).forEach(a => Object.assign(a, AWARDS_EN[a.work]));
if (window.AWARD_SCOPES) Object.assign(AWARD_SCOPES, AWARD_SCOPES_EN);
