// 작품 목록 — 한 줄이 작품 하나. 첫 장(/)의 "만든 것"과 디자인 쪽(/design/)이 이 목록을 거른다.
// 빼려면 그 줄을 지우고, 첫 장에서만 빼려면 home을 false로.
// design: false면 디자인 쪽 격자에서 뺀다(그 쪽 첫 그림과 같을 때). award는 작품 칸에 글자색으로 한 줄 더 적는다.
// kind: dev(개발) · graphic(그래픽) · video(영상). 그림 길은 사이트 뿌리(/)에서 본 길.
// 영상 제목은 해만 적고 회차는 적지 않는다(2026-11-26 주인 고름). 그래픽은 모두 경상롤드컵 제1회(2022).
window.WORKS = [
  { id: 'archi', kind: 'dev', home: true, title: 'archi-board', line: '코드와 문서를 읽어 아키텍처 보드 한 장을 그리는 Claude Code 스킬', meta: '혼자 · 공개 스킬 (MIT) · 엔진 1.6', href: '/work/archi-board/', img: '/assets/img/archi-back-960.webp', srcset: '/assets/img/archi-back-960.webp 960w, /assets/img/archi-back-1600.webp 1600w', w: 1600, h: 1000, alt: 'archi-board 예시 보드의 뒷면. 객체 지도와 순서도가 여러 창으로 이어져 있다' },
  { id: 'floe', anchor: 'floe', kind: 'dev', home: true, title: 'Floe', line: 'AI에게 코드를 맡기는 사람이 끝까지 만들게 돕는 데스크톱 앱', meta: '팀장 · 총괄 · AI 연동 (5인 팀)', award: '경진대회 본선 우수상', href: '/work/floe/', img: '/assets/img/floe-workspace-800.webp', srcset: '/assets/img/floe-workspace-800.webp 800w, /assets/img/floe-workspace-1600.webp 1600w', w: 1600, h: 955, alt: 'Floe 작업실 화면. 3단계 할 일 칸들과 플로로가 단계를 알려 주는 남색 판' },
  { id: 'dotci', anchor: 'dotci', kind: 'dev', home: true, title: 'DOTCI', line: '캠퍼스 장소에 도착하면 선배의 쪽지가 열리는 신입생용 웹', meta: 'UI 디자인 · 사용자 평가 · 발표 (3인 팀)', award: '경진대회 1위', href: '/work/dotci/', pair: [['/assets/img/dotci-map.webp', 'DOTCI 지도 화면. 캠퍼스 건물마다 쪽지 수가 붙은 점'], ['/assets/img/dotci-opened.webp', 'DOTCI에서 우송도서관 쪽지를 연 화면']], w: 540, h: 1169 },
  { id: 'mini', anchor: 'minimall', kind: 'dev', home: true, title: 'MiniMall', line: '요구 명세와 시험으로 끝을 재는 수업용 가상 쇼핑몰', meta: '발표 덱 · 대본, 사용자 쪽 점검 · 팀 시험 110개 통과', href: '/work/minimall/', img: '/assets/img/minimall-products-720.webp', srcset: '/assets/img/minimall-products-720.webp 720w, /assets/img/minimall-products-1440.webp 1440w', w: 1440, h: 900, alt: 'MiniMall 상품 목록. 검색 칸 아래 전체 상품 4' },
  { id: 'g-final', kind: 'graphic', home: true, title: '결승 포스터', line: 'THE GRAND FINAL', meta: '경상롤드컵 제1회 · 2022.12.07', img: '/assets/img/d-final-600.webp', big: '/assets/img/d-final-1200.webp', w: 600, h: 600, bw: 1200, bh: 1200, alt: '결승 포스터. 구겨진 검은 종이 위 위아래로 붉고 푸른 빛, 가운데 경상롤드컵 THE GRAND FINAL, 아래 GAME DAY 2022. 12. 07' },
  { id: 'g-offline', kind: 'graphic', home: true, design: false, title: '결승 화면 OFFLINE', line: 'VICTORY · MVP · WIN', meta: '경상롤드컵 제1회 · 2022.12.07', img: '/assets/img/d-offline-640.webp', big: '/assets/img/d-offline-1280.webp', w: 640, h: 360, bw: 1280, bh: 720, alt: '결승 날 방송 화면. 검은 종이 위에 흰 OFF와 테두리만 남은 LINE, 오른쪽에 노란 붓글씨 VICTORY · MVP · WIN' },
  { id: 'g-vs', kind: 'graphic', home: false, title: '방송 화면 1 VS 1', line: '대회 방송의 1 대 1 점수 화면', meta: '경상롤드컵 제1회 · 2022.10.22 – 23', img: '/assets/img/d-vs-640.webp', big: '/assets/img/d-vs-1280.webp', w: 640, h: 360, bw: 1280, bh: 720, alt: '대회 방송 화면. 푸른 성과 구름 위에 2022 경상롤드컵, 날짜, 가운데 1 VS 1 점수 띠' },
  { id: 'g-players', kind: 'graphic', home: false, title: '선수 소개 화면', line: '팀마다 선수 다섯을 자리와 함께 소개하는 방송 화면', meta: '경상롤드컵 제1회 · 2022', img: '/assets/img/d-players-640.webp', big: '/assets/img/d-players-1280.webp', w: 640, h: 360, bw: 1280, bh: 720, alt: '선수 소개 방송 화면. 밤하늘 위에 팀 이름 4 PLATINUM 1 SILBER, 금테 카드 다섯 아래에 TOP · JUG · MID · ADC · SUP. 선수 얼굴 · 이름 · 번호와 담당 선생님 이름은 모자이크로 가렸다' },
  { id: 'g-recruit', kind: 'graphic', home: false, title: '참가 모집 포스터', line: 'e-스포츠 대회 참가 모집', meta: '경상롤드컵 제1회 · 2022.10.22 – 23', img: '/assets/img/d-recruit-top.webp', big: '/assets/img/d-recruit-top.webp', w: 905, h: 640, alt: '참가 모집 포스터의 윗부분. 제1회 경상고등학교장배 e-스포츠 대회, 2022 경상롤드컵, 2022. 10. 22~23. 오전 9시, 총상금 100만원' },
  { id: 'v-school', kind: 'video', home: true, title: '2022 경상고등학교 홍보영상', yt: 'yNg7zA8J87Q', img: '/assets/img/v-school.webp', w: 960, h: 540 },
  { id: 'v-2022', kind: 'video', home: true, title: '2022 경상롤드컵 오프닝 영상', yt: '_aXdBsvoTng', img: '/assets/img/v-grand.webp', w: 960, h: 540 },
  { id: 'v-2021', kind: 'video', home: false, title: '2021 경상롤드컵 오프닝 영상', yt: 'EtVj5oIbZZI', img: '/assets/img/v-2021.webp', w: 480, h: 270 },
  { id: 'v-switch', kind: 'video', home: false, title: '중학생 대상 경상롤드컵 화면 전환 영상', yt: 'nos82iFOXSo', img: '/assets/img/v-fight.webp', w: 960, h: 540 },
  { id: 'v-2020', kind: 'video', home: false, title: '2020 경상롤드컵 오프닝 영상', yt: '6teR3wVCxOE', img: '/assets/img/v-2020.webp', w: 480, h: 270 },
  // 썸네일에 사람 얼굴이 또렷해 재생 표시 판으로 둔다
  { id: 'v-exam', kind: 'video', home: false, title: '수능응원 영상', yt: 'ze45Ppr12w0' },
  { id: 'v-grad', kind: 'video', home: false, title: '졸업영상', yt: 'Wp5Izk2OVQ8' },
];
window.KINDS = { dev: '개발', graphic: '그래픽', video: '영상' };
