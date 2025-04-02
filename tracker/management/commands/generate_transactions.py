import random
from faker import Faker
from django.core.management.base import BaseCommand
from tracker.models import User, Transaction, Category

"""
black ./tracker/management/commands/* : 코드 예쁘게 정리해주는 포맷터라는데 왜 나는 안되지
"""
class Command(BaseCommand):
    help = "테스팅을 위한 트랜잭션을 생성합니다"

    def handle(self, *args, **options):
        categories = ["청구서", "식비", "옷", "급여", "주거비", "의료비", "항공비", "주유비", "교통비", "기타"]

        for category in categories:
            Category.objects.get_or_create(name=category)
        
        admin = User.objects.filter(username='haeran').first()

        if not admin:
            admin = User.objects.create_superuser(username='haeran', password='password123') 

        bulk_list = []
        fake = Faker()
        categories = Category.objects.all()
        types = [x[0] for x in Transaction.TRANSACTION_TYPE_CHOICE]
        for i in range(20):
            bulk_list.append(Transaction(
                user = admin,
                category = random.choice(categories),
                type = random.choice(types),
                amount = random.uniform(1,2500),
                date = fake.date_between(start_date='-1y', end_date='today')
            ))
        
        Transaction.objects.bulk_create(bulk_list)
        
