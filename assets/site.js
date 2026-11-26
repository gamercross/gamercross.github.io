// gamercross 사이트: 폰 메뉴 · 작품 거르기 · 크게 보기 · 조용히 드러나기 · 첫 문장 낱말 바꾸기 · 움직이는 그림
// 위 메뉴(폰 메뉴 펼침)와 지금 쪽 표시는 로드맵도 같이 쓴다: <body data-page="roadmap">
document.documentElement.classList.add('js');
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

// 위 메뉴: 지금 쪽 표시 + 폰에서 메뉴 단추로 펼치기 (Esc로 닫고 단추로 초점이 돌아온다)
(() => {
  const page = document.body.dataset.page;
  document.querySelectorAll('.menu a[data-nav]').forEach(a => { if (a.dataset.nav === page) a.setAttribute('aria-current', a.pathname === location.pathname && !a.hash ? 'page' : 'true'); });
  const btn = document.querySelector('.menu-btn'), menu = document.getElementById('site-menu');
  if (!btn || !menu) return;
  const set = open => { btn.setAttribute('aria-expanded', open); menu.classList.toggle('is-open', open); btn.querySelector('.t').textContent = open ? '닫기' : '메뉴'; };
  btn.addEventListener('click', () => set(btn.getAttribute('aria-expanded') !== 'true'));
  menu.addEventListener('click', e => { if (e.target.closest('a')) set(false); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') { set(false); btn.focus(); } });
  matchMedia('(min-width: 761px)').addEventListener('change', e => { if (e.matches) set(false); });
})();

// 작품 그리기 (works.js의 한 줄 = 작품 하나)
(() => {
  const list = document.querySelector('[data-works]');
  if (!list || !window.WORKS) return;
  const scope = list.dataset.works;            // home | design
  const kinds = list.dataset.kinds.split(',');
  const hasPic = w => !!(w.img || w.pair);
  const items = WORKS.filter(w => kinds.includes(w.kind) && (scope !== 'home' || w.home))
    .sort((x, y) => kinds.indexOf(x.kind) - kinds.indexOf(y.kind) || hasPic(y) - hasPic(x));
  const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text) n.textContent = text; return n; };
  const pic = w => {
    const box = el('div', 'pic');
    if (w.pair) {
      box.classList.add('pair');
      w.pair.forEach(([src, alt]) => { const im = new Image(w.w, w.h); im.src = src; im.alt = alt; im.loading = 'lazy'; im.decoding = 'async'; box.append(im); });
    } else if (w.img) {
      const im = new Image(w.w, w.h); im.src = w.img; if (w.srcset) { im.srcset = w.srcset; im.sizes = '(max-width: 760px) 92vw, 46vw'; }
      im.alt = w.alt || ''; im.loading = 'lazy'; im.decoding = 'async'; box.append(im);
    } else {
      box.insertAdjacentHTML('beforeend', '<svg class="playmark" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="23"/><path d="M19 15.5v17a1 1 0 0 0 1.5.86l14-8.5a1 1 0 0 0 0-1.72l-14-8.5A1 1 0 0 0 19 15.5z"/></svg>');
    }
    return box;
  };
  items.forEach(w => {
    const li = el('li', `work k-${w.kind}${hasPic(w) ? '' : ' noimg'}`); li.dataset.kind = w.kind;
    if (w.anchor) li.id = w.anchor;   // 옛 주소의 #floe · #dotci · #minimall
    const h = el('h3'); const a = el('a', null, w.title);
    if (w.kind === 'video') { a.href = `https://www.youtube.com/watch?v=${w.yt}`; a.rel = 'noopener'; }
    else if (w.kind === 'graphic') { a.href = w.big; a.dataset.zoom = w.id; }
    else a.href = w.href;
    // 그림도 같은 곳으로 가는 길(키보드 · 화면 읽기 도구는 제목 링크 하나만 만난다)
    const pa = el('a', 'pic-a'); pa.href = a.href; pa.tabIndex = -1; pa.setAttribute('aria-hidden', 'true');
    if (a.dataset.zoom) pa.dataset.zoom = w.id; if (a.rel) pa.rel = a.rel;
    pa.append(pic(w)); li.append(pa);
    h.append(a); li.append(h);
    if (w.line) li.append(el('p', 'line', w.line));
    // 메타는 한 줄: 해 · 맡은 일만. 어디로 가는지는 링크 이름(화면 읽기 도구)에 둔다
    if (w.kind === 'video') a.setAttribute('aria-label', `${w.title}, 유튜브에서 보기`);
    if (w.kind === 'graphic') a.setAttribute('aria-label', `${w.title}, 크게 보기`);
    const metaText = w.kind === 'video' ? '유튜브' : (w.meta || '').replace(/^경상롤드컵 제1회 · /, '');
    if (metaText) li.append(el('p', 'meta', metaText));
    list.append(li);
  });
  // 디자인 쪽: 갈래마다 마지막 줄이 비지 않게 남은 칸을 나눠 넓힌다 (영상 네 칸씩).
  // 그래픽은 두 칸씩, 하나가 남으면 마지막 셋을 세 칸 줄로(하나만 화면 너비로 늘리지 않는다)
  if (list.classList.contains("wide")) {
    const per = { graphic: 2, video: 4 };
    kinds.forEach(k => {
      const row = per[k]; if (!row) return;
      const lis = [...list.querySelectorAll(`.work.k-${k}`)]; const r = lis.length % row;
      if (k === 'graphic' && r === 1 && lis.length >= 3) { lis.slice(-3).forEach(li => li.classList.add('fill-3')); return; }
      if (r) lis.slice(-r).forEach(li => li.classList.add(`fill-${r}`));
    });
  }
  // 그려진 뒤 옛 주소의 # 자리로 옮겨 간다
  if (location.hash) { const t = document.getElementById(decodeURIComponent(location.hash.slice(1))); if (t && list.contains(t)) requestAnimationFrame(() => t.scrollIntoView()); }

  // 거르기 단추 묶음: aria-pressed, 화면 읽기 도구에는 몇 개가 보이는지 알린다
  const bar = document.querySelector('[data-filter]');
  const count = document.querySelector('[data-count]');
  if (!bar) return;
  const groups = [['all', '전체', items.length], ...kinds.map(k => [k, KINDS[k], items.filter(w => w.kind === k).length])].filter(g => g[2] > 0);
  const btns = groups.map(([k, name, n]) => {
    const b = el('button'); b.type = 'button'; b.dataset.k = k; b.setAttribute('aria-pressed', k === 'all');
    b.append(name); const s = el('span', 'n', String(n)); s.setAttribute('aria-hidden', 'true'); b.append(s);
    b.setAttribute('aria-label', `${name} ${n}개`);
    bar.append(b); return b;
  });
  const apply = k => {
    let shown = 0;
    list.querySelectorAll('.work').forEach(li => {
      const on = k === 'all' || li.dataset.kind === k;
      li.hidden = !on; li.classList.remove('enter'); li.style.animationDelay = '';
      if (on) { shown++; if (!reduce) { void li.offsetWidth; li.classList.add('enter'); } }
    });
    btns.forEach(b => b.setAttribute('aria-pressed', b.dataset.k === k));
    if (count) count.textContent = k === 'all' ? `작품 ${shown}개 모두` : `${KINDS[k]} ${shown}개`;
  };
  btns.forEach(b => b.addEventListener('click', () => apply(b.dataset.k)));
  // 처음 보일 때 작품마다 한 번 떠오르기 (차례로 70ms씩)
  if (!reduce && 'IntersectionObserver' in window) {
    const seen = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { const li = e.target; li.style.animationDelay = (([...list.children].indexOf(li) % 4) * 70) + 'ms'; li.classList.add('enter'); seen.unobserve(li); } }), { rootMargin: '0px 0px -8% 0px' });
    list.querySelectorAll('.work').forEach(li => seen.observe(li));
  }
  if (count) count.textContent = `작품 ${items.length}개 모두`;
})();

// 크게 보기: <dialog> + showModal, 바깥 누르기 · Esc로 닫힘, 이전 · 다음
(() => {
  const dlg = document.querySelector('dialog.lb');
  if (!dlg) return;
  const img = new Image(); img.decoding = 'async';   // 처음 열 때 붙인다(빈 그림을 미리 두지 않음)
  const t = dlg.querySelector('figcaption b'), s = dlg.querySelector('figcaption span');
  let ids = [], at = 0, from = null;
  const visible = () => [...document.querySelectorAll('h3 [data-zoom]')].filter(a => !a.closest('.work').hidden).map(a => a.dataset.zoom);
  const show = i => {
    ids = visible();
    at = (i + ids.length) % ids.length;
    const w = WORKS.find(x => x.id === ids[at]);
    img.src = w.big; img.alt = w.alt; img.width = w.bw || w.w; img.height = w.bh || w.h;
    t.textContent = w.title; s.textContent = w.meta;
    if (!img.isConnected) dlg.querySelector('figure').prepend(img);
  };
  document.addEventListener('click', e => {
    const a = e.target.closest('[data-zoom]');
    if (!a) return;
    e.preventDefault(); from = a.closest('.work').querySelector('h3 a');
    show(visible().indexOf(a.dataset.zoom));
    dlg.showModal();
  });
  dlg.querySelector('[data-prev]').addEventListener('click', () => show(at - 1));
  dlg.querySelector('[data-next]').addEventListener('click', () => show(at + 1));
  dlg.querySelector('[data-close]').addEventListener('click', () => dlg.close());
  dlg.addEventListener('keydown', e => { if (e.key === 'ArrowLeft') show(at - 1); if (e.key === 'ArrowRight') show(at + 1); });
  dlg.addEventListener('close', () => { if (from) from.focus(); });
  if (!('closedBy' in HTMLDialogElement.prototype)) {
    dlg.addEventListener('click', e => {
      if (e.target !== dlg) return;
      const r = dlg.getBoundingClientRect();
      if (r.top <= e.clientY && e.clientY <= r.bottom && r.left <= e.clientX && e.clientX <= r.right) return;
      dlg.close();
    });
  }
})();

// 조용히 드러나기 (구역 안의 부분들이 차례로, 한 번만)
(() => {
  const secs = document.querySelectorAll('[data-reveal]');
  if (reduce || !('IntersectionObserver' in window)) { secs.forEach(s => s.classList.add('in')); return; }
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -10% 0px' });
  secs.forEach(s => io.observe(s));
})();

// 첫 문장의 낱말 바꾸기: "하나의 별이" → "하나의 꿈이" → "하나의 별이"에서 멈춘다 (5초 안에 끝)
(() => {
  const sw = document.querySelector('.swap');
  if (!sw || reduce) return;
  ['하나의 꿈이', '하나의 별이'].forEach((w, i) => setTimeout(() => {
    sw.classList.add('out');
    setTimeout(() => { sw.textContent = w; sw.classList.remove('out'); }, 600);
  }, 1400 + i * 2000));
})();

// 움직이는 그림: 보일 때만 소리 없이 되풀이, 멈춤 단추, 움직임 줄이기면 처음부터 멈춤
(() => {
  document.querySelectorAll('[data-clip]').forEach(box => {
    const v = box.querySelector('video'), b = box.querySelector('.pp');
    let userPaused = reduce;
    const set = () => { box.classList.toggle('paused', v.paused); b.setAttribute('aria-label', v.paused ? '영상 재생' : '영상 멈추기'); };
    const play = () => { const p = v.play(); if (p) p.catch(() => {}); };
    v.addEventListener('play', set); v.addEventListener('pause', set); set();
    b.addEventListener('click', () => { if (v.paused) { userPaused = false; play(); } else { userPaused = true; v.pause(); } });
    if (!('IntersectionObserver' in window)) return;
    new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting && !userPaused) play(); else if (!e.isIntersecting) v.pause();
    }), { threshold: 0.4 }).observe(box);
  });
})();
