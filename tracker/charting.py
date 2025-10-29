from django.db.models import Sum
import plotly.express as px

def plot_income_expenses_bar_chart(qs):
    x_vals = ['총수입', '총지출']

    total_income = qs.filter(type='income').aggregate(total=Sum('amount'))['total']
    total_expense = qs.filter(type='expense').aggregate(total=Sum('amount'))['total']
    fig = px.bar(x=x_vals, y=[total_income, total_expense], labels={'x':'','y':'금액(원)'})

    return fig

def plot_category_pie_chart(qs, title):
    query_list = qs.order_by('category').values_list('category__name').annotate(Sum('amount'))
    category_list = [c for c,_ in query_list]
    amount_list = [a for _,a in query_list]

    fig = px.pie(values=amount_list, names=category_list, title=title)

    return fig
    