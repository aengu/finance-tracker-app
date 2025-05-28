### pytest 중 테스트케이스의 쿼리 count 하기
1. test_view 테스트 중 이런 코드가 있었다.
    ```python
    @pytest.mark.django_db
    def test_transaction_type_filter1(user_transactions, client):
        user = user_transactions[0].user
        client.force_login(user)

        # income check
        GET_params = {'transaction_type': 'income'}
        response = client.get(reverse('transaction_list'), GET_params)

        qs = response.context['filter'].qs
        for tr in qs:
            assert tr.type == 'income'
    ```
2. 테스트를 하는 view 함수의 코드는 이랬다.
    ```python
        def transaction_list(request):
        transaction_filter = TransactionFilter(
            request.GET,
            queryset=Transaction.objects.filter(user=request.user).select_related('category')
        )
        total_income = transaction_filter.qs.get_total_income()
        total_expenses = transaction_filter.qs.get_total_expenses()
        context = {
            'filter' : transaction_filter,
            'total_income' : total_income,
            'total_expenses': total_expenses,
            'net_income':total_income - total_expenses
            }

        # htmx 요청이 있는 경우, 템플릿의 일부분만 반환 
        if request.htmx:
            return render(request, 'tracker/particials/transaction-container.html', context)
        
        return render(request, 'tracker/transaction-list.html', context)
    ```
3. 그래서 view 함수에서만 보면 qs는 filter().select_related()으로 return하기 때문에 django의 lazy loading 특성상 쿼리가 실행되지 않은 상태이고, 이 상태로 pytest에서 for문으로 쿼리셋을 순회하면 n+1 problem이 될 거라고 생각했다. 그래서 실제로 쿼리 실행 수를 세는 데코레이터를 만들어 확인해봤다.
    ```python
    def query_debugger(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not settings.DEBUG:
                # DEBUG=False이면 동작하지 않도록 안전 장치
                return func(*args, **kwargs)
            reset_queries()
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()

            total_time = end - start
            num_queries = len(connection.queries)

            print(f"\n🔍 Function: {func.__name__}")
            print(f"🕒 Time: {total_time:.4f}s")
            print(f"📦 Query Count: {num_queries}")

            for i, query in enumerate(connection.queries, start=1):
                print(f"  {i}. {query['sql']} ({query['time']}s)")

            return result
        return wrapper
    ```

4. 이러고 pytest를 실행했는데 time은 잘 떴지만 query count가 항상 0으로 나왔다.
    - 알고보니 django에서는 성능저하이슈로 settings.py에 debug=True여도 테스트환경에선 기본적으로 False로 설정한다.
    - https://docs.djangoproject.com/en/5.2/topics/testing/overview/#other-test-conditions
    - 그래서 임의로 conftest 파일에 명시를 해줘야 한다.
    ```python
    @pytest.fixture(autouse=True)
    def enable_debug_setting():
        settings.DEBUG = True
    ```

5. 드디어 query count를 확인했는데 6개였다. 즉 response.qs이 이미 실행된 상태였던 것이다. 알고보니 view함수에
    ```python
    # views.py
    total_income = transaction_filter.qs.get_total_income()
    total_expenses = transaction_filter.qs.get_total_expenses()

    # managers.py
    def get_total_expenses(self):
        return self.get_expense().aggregate(
            total=models.Sum('amount')
        )['total'] or 0
    
    def get_total_income(self):
        return self.get_income().aggregate(
            total=models.Sum('amount')
        )['total'] or 0
    ```
    수입/지출의 합을 계산하는 aggregate는 lazy loading하지 않고 바로 실행되기 때문에 qs이 테스트함수에서 이미 실행된 상태였던 것이다.

6. 그러면 view함수에서 aggregate를 하지 않는다면 qs가 테스트함수의 for문 전에는 실행되지 않는 상태겠지?라고 생각하여 확인해보았다.
    ```python
    total_income = 0
    total_expenses = 0
    ```

7. 이렇게 해도 qs count가 변함이 없었다! 즉 view함수에서 .filter().select_related()만 return 했는데도 쿼리를 실행했다는 것이었다. (+ qs._result_cache가 None이 아니고 Transaction의 queryset이었다.)

8. 내가 놓친게 있었는데 view함수는 reder함수의 반환값인 httpResponse를 return을 한다.
    ```python
    #views.py
    return render(request, 'tracker/transaction-list.html', context)
    ```

    그리고 렌더링하는 템플릿에는 qs를 순회한다.
    ```html
    <tbody>
            {% for transaction in filter.qs %}
                <tr>
                    <td>{{transaction.date}}</td>
                    <td>{{transaction.category}}</td>
                    <td>{{transaction.type}}</td>
                    <td>{{transaction.amount}}</td>
                </tr>
            {% endfor %}
        </tbody>
    ```
    django의 템플릿 엔진이 qs를 순회하기 위해 쿼리셋을 실행하기 때문에 return render시점에서 쿼리셋이 실행되는 것이었다. 궁금증 해결!!!


