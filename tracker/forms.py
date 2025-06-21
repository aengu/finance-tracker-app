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