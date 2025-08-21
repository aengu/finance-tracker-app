### django template에서 get 요청의 파라미터 유지하는 방법
- 이번에 새로 안 방법이 있어서 이참에 정리

1. {{request.GET.urlencode}}
    - request.GET은 get parameter를 querydict 형식으로 반환한다 (ex: QueryDict({'category':1}))
    - urlencode는 querydict의 내장 메서드인데, 템플릿엔진이 url로 읽을 수 있도록 인코딩 하여 반환한다
    - 근데 지금 상황에서 이렇게 하면, 무조건 get 파라미터 전부를 그대로 유지하기 때문에, &page=1&page=2이렇게 page 파라미터가 중복되는 경우가 발생할 수 있다.
    ```html
    hx-get="?{{request.GET.urlencode}}&page={{transactions.next_page_number}}"
    ```
2. custom template tags
    - https://docs.djangoproject.com/en/4.2/howto/custom-template-tags/
    - 그래서 1번의 단점을 해결할 방법 중 하나가 template tag를 직접 만드는 것이다.
    - 현재 요청의 get 파라미터를 그대로 유지하되 page 파라미터는 교체하는 템플릿 태그를 만들면 된다.
    ```python
    from django import template

    register = template.Library()

    @register.simple_tag
    def url_replace(request, field, value):
        dict_ = request.GET.copy()
        dict_[field] = value
        return f'{request.path}?{dict_.urlencode()}'
    ```
    ```html
    {% load custom_filter %}
    hx-get="{% url_replace request 'page' transactions.next_page_number %}"
    ```
3. htmx의 hx-include
    - https://htmx.org/attributes/hx-include/
    - 이번 프로젝트에서 htmx를 사용하면서 새로 배운 방법이다.
    - hx-include의 대상 form의 파라미터를 그대로 포함한다. 페이지는 직접 지정
    ```html
    hx-get="{% url 'transaction-list'%}?page={{transactions.next_page_number}}
    hx-include="#filter-form"
    ```