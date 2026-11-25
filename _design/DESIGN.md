---
version: alpha
name: gamercross.github.io v3
description: 이재엽(gamercross) 포트폴리오. 작품이 주인공인 색 장, 틀 없는 큰 그림, 일하는 법 · 2027의 단계표. 원천은 assets/v3.css.
colors:
  ground: "#DDE6EA"
  lit: "#F2F5F6"
  step: "#D3DEE3"
  ink: "#17233F"
  ink-2: "#33405C"
  ink-soft: "#C9D3E6"
  hero: "#D6E3E7"
  archi: "#D3E3DA"
  floe: "#ECE5C9"
  dotci: "#D2DDEC"
  mini: "#EBD7DB"
  rise-0: "#D0DAE1"
  rise-1: "#BAC7D3"
  rise-2: "#A2B3C4"
  rise-3: "#8FA2B7"
  frame: "#26314A"
typography:
  s-small:
    fontFamily: Wanted Sans Variable
    fontSize: clamp(0.9375rem, 0.9rem + 0.15vw, 1.0625rem)
  s-body:
    fontFamily: Wanted Sans Variable
    fontSize: clamp(1.0625rem, 1rem + 0.25vw, 1.25rem)
    lineHeight: 1.55
  s-lead:
    fontFamily: Wanted Sans Variable
    fontSize: clamp(1.25rem, 1.05rem + 0.75vw, 1.875rem)
  s-head:
    fontFamily: Wanted Sans Variable
    fontSize: clamp(2.5rem, 1.4rem + 4.4vw, 6rem)
    fontWeight: 850
    letterSpacing: -0.04em
  s-sig:
    fontFamily: Wanted Sans Variable
    fontSize: clamp(3.4rem, 1.6rem + 7.4vw, 9.5rem)
    fontWeight: 850
    letterSpacing: -0.045em
spacing:
  m: clamp(16px, 2.2vw, 40px)
  g: clamp(10px, 1.2vw, 20px)
---

## Overview

이재엽(gamercross)이 끝낸 작품을 크게 보여 주는 포트폴리오다. 장마다 한 색 면에 작품 하나를 기기 틀 없이 크게 놓고, 글은 세 줄 안으로 둔다. 진지하고 차분한 결: 채도를 낮춘 파스텔 바탕에 남색 글씨, 무게는 글자 위계와 여백으로 준다.

## Colors

- 바탕은 `ground`, 가장 밝은 면은 `lit`이다. 순백 바탕은 쓰지 않는다.
- 글씨는 `ink`, 둘째 글씨는 `ink-2`. 남색 면 위 둘째 글씨만 `ink-soft`를 쓴다.
- 작품 장의 색 면은 작품마다 하나(`archi` · `floe` · `dotci` · `mini`), 첫 화면 · 2027 · 연락은 `hero`.
- 단계표는 `rise-0` → `rise-3`로 짙어지며 오르고, 꼭대기 한 칸은 `ink` 면에 `lit` 글씨다. `rise-3` 위의 작은 글씨는 `ink`로 쓴다(대비 4.5:1).
- `frame`(남색)은 코드 칸 · DOTCI 폰의 가는 테에만. 검정 면은 쓰지 않는다.

## Typography

- 글꼴은 Wanted Sans 한 벌. 크기는 YAML의 다섯(`s-small` · `s-body` · `s-lead` · `s-head` · `s-sig`)만 쓴다.
- 첫 화면 h1은 이름(`s-lead`)과 "MAKE, FIX, GO HIGH."(`s-sig`)를 함께 담는다.
- 주인 말 인용은 원문 그대로, 따옴표를 붙여 `s-body`로.
- 문서 이름(업무 매뉴얼 v2 등)은 쉬운 말 제목 아래 `s-small`로 작게 둔다.

## Layout

- 12칸 격자, 바깥 여백은 `spacing.m`, 칸 사이는 `spacing.g`.
- 작품 장은 글 4칸 + 그림 7칸, 장마다 좌우를 바꾼다. 1100px 아래에서는 글 → 그림 차례로 한 줄.
- 640px 아래에서 단계표는 두 칸씩 쌓는다(높이 차이는 없앤다).

## Shapes

- 면 · 막대 · 단추는 모서리가 반듯한 사각형이다. 둥근 모서리는 그림(`.cover` · `.pane`)과 DOTCI 폰에만.
- 계단 모양으로 깎은 모서리 · 도트 무늬는 쓰지 않는다. 사이트 자체의 마스코트 · 캐릭터 그림도 쓰지 않는다(작품 속 그림은 작품으로 싣는다).

## Components

- 단추(`.btn`): `ink` 면, `lit` 글씨, 높이 52px 이상. 한 구역에 하나.
- 그림(11/25 주인 "그림"): 노트북 · 브라우저 띠 · 두꺼운 폰은 쓰지 않는다. 첫 장 표지는 모두 `.cover` 16:10, 너비마다 핵심을 잘라(`<picture>`) 보이는 크기에서 글이 11px 안팎으로 읽히게. DOTCI만 가는 테 폰 한 대(`.handset`), 제조사 표시 없음.
- 단계표(`.stair.up` · `.stair.down`): '일하는 법' · '2027' 구역에서만 쓴다.

## Do's and Don'ts

- 하지 않는다: 그림자 · 그라디언트 · 1px 테두리 카드 · 칩 줄 · 글리프 장식 · 도트 글꼴 · 캐릭터 그림. 글꼴은 Wanted Sans 밖으로 늘리지 않는다.
- 하지 않는다: 뛰거나 흔들리는 움직임. 움직임은 들어올 때 한 번(투명도 · 위치), 움직임 줄이기 설정이면 없다.
- 하지 않는다: 다른 사람의 실명 · 학번 · 학점 · 날짜별 개인 일정 · 만드는 중인 것의 링크.
