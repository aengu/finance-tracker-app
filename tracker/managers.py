from django.db import models


class TransactionQuerySet(models.QuerySet):
    def get_expense(self):
        return self.filter(type='expense')
    
    def get_income(self):
        return self.filter(type='income')
    
    def get_total_expenses(self):
        return self.get_expense().aggregate(
            total=models.Sum('amount')
        )['total'] or 0
    
    def get_total_incomes(self):
        return self.get_income().aggregate(
            total=models.Sum('amount')
        )['total'] or 0

"""
NOTE. total 메서드에서 or 0 하는 이유?
get_[]메서드 반환: TransactionQuerySet
aggregate 반환: dict
만약 get_[]에 select된 row가 없는 경우 빈 쿼리셋이 되고
그 쿼리셋의 집계의 반환은 {'total':None} 이 되기 때문에
이 경우 0을 반환하게 하는 것
a = None or 0 하면 a = 0이 되니까
"""