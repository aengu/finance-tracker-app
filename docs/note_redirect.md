### redirect 메서드
- https://docs.djangoproject.com/en/5.1/topics/http/shortcuts/#django.shortcuts.redirect
- 자꾸 헷갈려서 그냥 정리...
- 인자에 따라 적절한 URL로 HttpRedirectResponse를 반환하는 메서드

### redirect의 인자
1. 모델 인스턴스: 해당 모델의 get_absolute_url() 메서드가 호출됨
    ```python
    obj = Transaction.objests.first()
    redirect(obj)
    ```
    - 모델에 get_absolute_url()이 정의되어 있다면 호출해서 URL 사용
    - 정의 안 되어 있으면 reverse()시도 -> 그래서 get_absolute_url이 정의 안되어 있는 상황에서 인자로 모델 객체를 넣으면 NoReverseMatch 에러가 뜨는 것이다!
2. 뷰 이름(view name) (필요한 경우 인자들과 함께): reverse() 함수가 사용되어 URL을 역으로 찾아냄
3. 절대/상대 URL 문자열: 전달된 URL이 그대로 리디렉션 대상이 됨

### ✅ `render()` vs `redirect()` 차이점

| 항목 | `render()` | `redirect()` |
|------|------------|--------------|
| **역할** | 템플릿을 렌더링해서 HTML 응답 반환 | 다른 URL로 **리디렉션** (브라우저가 새 요청 보내게 함) |
| **HTTP 상태 코드** | `200 OK` | 기본 `302 Found` (또는 `301 Moved Permanently`) |
| **클라이언트 동작** | 현재 URL에서 그대로 결과 보여줌 | 클라이언트가 지정된 URL로 **다시 요청** |
| **서버 동작** | 현재 뷰 내부에서 템플릿 렌더링 | 응답에 `Location` 헤더 포함 → 브라우저가 다른 URL로 이동 |
| **사용 예시** | 폼 제출 실패 시 에러 메시지 보여줄 때 등 | 폼 제출 성공 후 목록 페이지로 이동할 때 등 |

```python
def my_view(request):
form = MyForm(request.POST or None)
if form.is_valid():
    form.save()
    return redirect('success_page')
return render(request, 'my_template.html', {'form': form})
```

### get_absolute_url 쓰는 법
- https://docs.djangoproject.com/en/5.1/ref/models/instances/#django.db.models.Model.get_absolute_url
```python
# 보통 이런 식으로 쓴다
def get_absolute_url(self):
        return '/' + self.slug

def get_absolute_url(self):
    from django.urls import reverse
    return reverse("people-detail", kwargs={"pk": self.pk})

```

### link/ redirect poisoning?
- 검증되지 않은 사용자 입력값을 이용해 URL을 직접 구성하는 것은 피해야 함
```python
# self.name이 /example.com이라면

# "//example.com/"이 됨. 원래 의도는 "/%2Fexample.com/"이렇게 /가 인코딩 되어 escape상태로 해야한다
def get_absolute_url(self):
    return "/%s/" % self.name
```
- 왜?: 사용자 입력을 검증없이 사용할 경우, 악의적으로 name = '//evil.com'으로 설정해서 해당 url로 리디렉션이 됨, 그러면 의도치 않은 악성 사이트로 접속되어 공격 노출 될 수 있음
```python
# 이렇게 해주면 안전하다고 한다,,
from urllib.parse import quote

def get_absolute_url(self):
    safe_name = quote(self.name, safe='')
    return f"/{safe_name}/"
```