// 들어올 때 한 번 움직인다. 스크립트가 없으면 모든 내용이 그대로 보인다.
(function () {
  var root = document.documentElement;
  root.classList.add('js');
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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
