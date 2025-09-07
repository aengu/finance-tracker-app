### htmx 속성들 몇 개 정리

1. htmx-indicator
- https://htmx.org/attributes/hx-indicator/
- https://daisyui.com/components/loading/
- htmx 요청이 진행되는 동안, hx-indicator selector로 지정한 요소에 htmx-request class가 추가된다.
- 추가로 요소에 htmx-indicator class를 설정하면 요청시간동안 나타났다가 끝나면 불투명해진다.(그래서 주로 스피너나 진행바에 많이 씀)
- 나처럼 까먹고 htmx-indicator를 설정 안해놓으면 요청이 끝나도 스피너가 사라지지 않는다... 일단 공식문서 정독을 생활화하자
```python
<div>
    <button hx-post="/example" hx-indicator="#spinner">
        Post It!
    </button>
    <img  id="spinner" class="htmx-indicator" src="/img/bars.svg"/>
</div>
```
```css
    .htmx-indicator{
        opacity:0;
        transition: opacity 500ms ease-in;
    }
    .htmx-request .htmx-indicator{
        opacity:1;
    }
    .htmx-request.htmx-indicator{
        opacity:1;
    }
```