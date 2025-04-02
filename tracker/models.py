from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Categories" # 이거 안하면 admin에서 catetorys 이렇게 함
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    """ 금융거래 내역 """
    TRANSACTION_TYPE_CHOICE = (
        ('income', '수익'),
        ('expense', '지출')
    )
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICE, verbose_name="거래유형")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="거래자")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="금액")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="카테고리")
    date = models.DateField(verbose_name="거래일")

    def __str__(self):
        return f"{self.type} of {self.amount} on {self.date} by {self.user}"