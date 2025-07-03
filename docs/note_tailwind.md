### tailwind css 자주 쓰는 속성 정리
| Tailwind 클래스       | CSS 속성 의미                                                             |
|-----------------------|---------------------------------------------------------------------------|
| `flex`                | `display: flex;` — 요소를 flex 컨테이너로 만듬                            |
| `justify-between`     | `justify-content: space-between;` — 좌우 요소를 양 끝으로 정렬                   |
| `items-center`        | `align-items: center;` — 세로 방향(교차축) 중앙 정렬                           |
| `gap-2`, `gap-4` 등   | `gap: 0.5rem`, `1rem` 등 — 자식 요소 간의 간격 설정 (기본 단위는 `rem`)         |
| `mt-4`, `mb-6` 등     | `margin-top: 1rem`, `margin-bottom: 1.5rem` 등 — 위/아래 바깥 여백 설정          |
| `text-white`          | `color: #ffffff;` — 텍스트 색상을 흰색으로 설정                                 |
| `prose`, `prose-2xl`  | 타이포그래피 스타일 적용 (Tailwind Typography 플러그인 필요)                   |
| `w-10`, `h-10` 등     | `width`, `height` 설정 (ex. `w-10` = `2.5rem`, `40px`)                          |
| `cursor-pointer`      | `cursor: pointer;` — 마우스 오버 시 클릭 가능한 커서로 변경                      |
