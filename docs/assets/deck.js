// 강의 슬라이드 웹 버전 엔진: 화면 맞춤, 키보드·클릭 이동, 영상 자동 재생, 주소(#번호) 동기화
(() => {
  const stage = document.querySelector('.stage');
  const slides = [...document.querySelectorAll('.slide')];
  const count = document.querySelector('.count');
  const progress = document.querySelector('.progress');
  const notes = document.querySelector('.notes');
  let cur = 0;

  function fit() {
    const s = Math.min(innerWidth / 1920, innerHeight / 1080);
    stage.style.transform = `translate(-50%, -50%) scale(${s})`;
  }

  function show(i) {
    cur = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((el, k) => {
      el.classList.toggle('active', k === cur);
      el.querySelectorAll('video').forEach(v => {
        if (k === cur) { v.currentTime = 0; v.play().catch(() => {}); } else v.pause();
      });
    });
    count.textContent = `${cur + 1} / ${slides.length}`;
    progress.style.width = `${(cur + 1) / slides.length * 100}%`;
    const note = slides[cur].querySelector('aside.note');
    notes.textContent = note ? note.textContent.trim() : '(노트 없음)';
    history.replaceState(null, '', `#${cur + 1}`);
  }

  addEventListener('keydown', e => {
    if (['ArrowRight', 'PageDown', ' ', 'Enter'].includes(e.key)) { e.preventDefault(); show(cur + 1); }
    else if (['ArrowLeft', 'PageUp', 'Backspace'].includes(e.key)) { e.preventDefault(); show(cur - 1); }
    else if (e.key === 'Home') show(0);
    else if (e.key === 'End') show(slides.length - 1);
    else if (e.key === 'f' || e.key === 'F') toggleFull();
    else if (e.key === 'n' || e.key === 'N') notes.classList.toggle('show');
  });

  // 무대 클릭: 영상은 다시 재생, 버튼은 그대로, 나머지는 왼쪽 1/3 = 이전, 그 외 = 다음
  stage.addEventListener('click', e => {
    if (e.target.closest('button, a')) return;
    const v = e.target.closest('video');
    if (v) { v.currentTime = 0; v.play(); return; }
    const r = stage.getBoundingClientRect();
    show(e.clientX - r.left < r.width / 3 ? cur - 1 : cur + 1);
  });

  document.querySelectorAll('.reveal').forEach(b => b.addEventListener('click', () => {
    const a = b.nextElementSibling;
    a.classList.toggle('show');
    b.textContent = a.classList.contains('show') ? '정답 숨기기' : '정답 보기';
  }));

  function toggleFull() {
    if (document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen();
  }
  document.querySelector('[data-act=prev]').onclick = () => show(cur - 1);
  document.querySelector('[data-act=next]').onclick = () => show(cur + 1);
  document.querySelector('[data-act=full]').onclick = toggleFull;
  document.querySelector('[data-act=notes]').onclick = () => notes.classList.toggle('show');

  addEventListener('hashchange', () => { const n = parseInt(location.hash.slice(1)) - 1; if (n !== cur && n >= 0) show(n); });
  addEventListener('resize', fit);
  fit();
  show((parseInt(location.hash.slice(1)) || 1) - 1);
})();
