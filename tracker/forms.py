from django import forms
from .models import Transaction, Category, User

class TransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.RadioSelect()
    )
    class Meta:
        model = Transaction
        fields = ('type', 'amount', 'date', 'category', )
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'})
        }
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('금액에 양수를 적어 주세요')
        return amount