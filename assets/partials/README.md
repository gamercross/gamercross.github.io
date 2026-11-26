# 같이 쓰는 조각

포트폴리오와 커리어 로드맵이 같은 꼴로 보이게 하는 조각이다. 쪽마다 이 조각을 그대로 붙여 넣는다.

| 파일 | 무엇 | 붙이는 곳 |
|---|---|---|
| `../tokens.css` | 색 · 글꼴 · 글자 단계 · 간격 | `<head>`, Pretendard 다음 · `site.css` 앞 |
| `../site.css` | 위 메뉴 · 맺음 · 구역 꼴 | `<head>`, `tokens.css` 다음 |
| `../site.js` | 폰 메뉴 펼침 · 지금 쪽 표시 · 조용히 드러나기 | `<head>`에 `defer` |
| `header.html` | 위 메뉴 | `<body>` 맨 앞(건너뛰기 링크 다음) |
| `footer.html` | 맺음 | `</main>` 다음 |
| `../favicon.svg` | 작은 그림 | `<link rel="icon">` |

- 지금 쪽 표시: `<body data-page="roadmap">`처럼 적으면 메뉴의 같은 `data-nav` 칸에 `aria-current="page"`가 붙는다. 값은 work · design · how · roadmap · about · contact.
- 메뉴의 링크는 모두 사이트 뿌리(`/`)에서 시작하므로 어느 쪽에 붙여도 같은 곳으로 간다.
- 바깥 계정(GitHub · LinkedIn · Instagram · X) 주소는 `footer.html` 한 곳에 있다. 첫 장 연락 판도 같은 줄을 쓴다.
