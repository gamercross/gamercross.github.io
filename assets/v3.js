// gamercross.github.io v3. 스크립트가 없어도 모든 내용이 그대로 보인다.
(function () {
  var root = document.documentElement;
  root.classList.add('js');
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;

  // 들어올 때 한 번: 제목 → 글 → 그림, 계단은 한 칸씩
  var targets = document.querySelectorAll('.rise, .lift, .stair.climb');
  function showAll() { targets.forEach(function (el) { el.classList.add('is-in'); }); }
  if (!hasIO || still) showAll();
  else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.04 });
    targets.forEach(function (el) { io.observe(el); });
  }
  window.addEventListener('beforeprint', showAll);
  // 주소의 # 자리로 바로 왔을 때도 그 자리가 비어 보이지 않게
  if (location.hash) { var h = document.getElementById(location.hash.slice(1)); if (h) h.querySelectorAll('.rise, .lift, .stair.climb').forEach(function (el) { el.classList.add('is-in'); }); }

  // 머리줄이 지금 지나는 장의 색을 입는다
  var bar = document.querySelector('.bar');
  var fields = document.querySelectorAll('[data-bar]');
  if (bar && hasIO) {
    var fo = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) bar.style.setProperty('--bar', e.target.getAttribute('data-bar')); });
    }, { rootMargin: '-40px 0px -92% 0px', threshold: 0 });
    fields.forEach(function (f) { fo.observe(f); });
  }

  // 영상: 보일 때만 돈다. 움직임 줄이기면 멈춘 채 조작 단추를 보인다
  document.querySelectorAll('video[data-loop]').forEach(function (v) {
    if (still || !hasIO) { v.controls = true; return; }
    v.muted = true;
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function () { v.controls = true; }); }
        else v.pause();
      });
    }, { threshold: 0.3 }).observe(v);
  });
})();
