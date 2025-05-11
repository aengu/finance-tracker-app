### factory boy 패키지
- https://factoryboy.readthedocs.io/en/stable/
- 테스트용 더미 데이터를 자동으로 만들어 주는 python 패키지
- django 모델 인스턴스나 다른 객체들을 간단한 코드로 만들 수 있다
- 보통 Pytest와 같이 사용하기 때문에 자동으로 db롤백 되어 테스트 동안 생성한 더미데이터를 수동으로 삭제할 필요는 없다
- 사용방법
    1. 보통 factories.py에 더미 데이터 생성할 모델의 Facory 클래스를 만들고
    2. factory 인스턴스의 batch로 데이터 생성
        ```python
        transaction_factory = TransactionFactory(amount=11.55) # 인수로 재정의 가능
        transaction_factory.create_batch(10)  # 10개 생성
        ```
