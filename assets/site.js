// 들어올 때 한 번 움직인다. 스크립트가 없으면 모든 내용이 그대로 보인다.
(function () {
  var root = document.documentElement;
  root.classList.add('js');
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 구역의 부분마다 차례로 들어오게: 제목 → 글 → 그림. 마크업에 일일이 적지 않고 여기서 붙인다.
  ['.index-head > *', '.more-head > *', '.mini-row', '.made > h2', '.line > h2', '.line .note', '.with > h2',
   '.about > h2', '.about .facts > div', '.else > h2', '.else li', '.contact > h2', '.nums > div',
   '.d-hero .cells > div', '.tree .roots', '.tree .trunk', '.next > h2', '.next .name', '.next .desc', '.foot .name'
  ].forEach(function (sel) {
    document.querySelectorAll(sel).forEach(function (el, i) {
      if (el.classList.contains('rise')) return;
      el.classList.add('rise');
      if (!el.style.getPropertyValue('--i')) el.style.setProperty('--i', i % 6);
    });
  });

  var targets = document.querySelectorAll('.rise, .pop-group, .shutter, .grow');
  function showAll() { targets.forEach(function (el) { el.classList.add('is-in'); }); }

  if (!('IntersectionObserver' in window)) {
    showAll();
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    targets.forEach(function (el) { io.observe(el); });
  }
  // 인쇄 · 전체 쪽 찍기처럼 스크롤 없이 보는 때에도 내용이 남지 않게
  window.addEventListener('beforeprint', showAll);

  // 영상: 보일 때만 돌고, 움직임 줄이기 설정이면 멈춘 채 조작 단추를 보인다
  var clips = document.querySelectorAll('video[data-loop]');
  clips.forEach(function (v) {
    if (still || !('IntersectionObserver' in window)) { v.controls = true; return; }
    v.muted = true;
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function () { v.controls = true; }); }
        else { v.pause(); }
      });
    }, { threshold: 0.35 }).observe(v);
  });
})();
