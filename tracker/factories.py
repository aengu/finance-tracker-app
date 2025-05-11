from datetime import datetime
import factory
from .models import User, Transaction, Category

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Sequence(lambda n: 'user%d' % n)

class CatetoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name',)

    name = factory.Iterator(
        ["청구서", "식비", "옷", "급여", "주거비", "의료비", "항공비", "주유비", "교통비", "기타"]
    )

class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction
    
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CatetoryFactory)
    amount = 5
    date = factory.Faker(
        'date_between',
        start_date = datetime(year=2022, month=1, day=1).date(),
        end_date=datetime.now().date()
    )
    type = factory.Iterator(
        [x[0] for x in Transaction.TRANSACTION_TYPE_CHOICE] # 랜덤순회가 아닌, 반복순회로 변경 [income, expense]라서 income -> expense -> income ..순으로 생성됨
    )