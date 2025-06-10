from datetime import date, datetime
from django.shortcuts import render
from sales.models import *
from django.db.models import Sum

# function to combine store and online sales into a single dictionary
def get_order_data(store, online):
    """
    The function aggregates daily revenue from two datasets (store and online) into a 
    single dictionary. This is useful for combining sales data from different sources 
    (e.g., physical store sales and online sales) for further analysis or visualization.
    """
    day_and_amount = {}

    # Process store sales
    for sales in store:
        date = sales['date']  # 'date' is a datetime object
        day = date.day  # Extract the day of the month
        amount = float(round(sales['daily_revenue'], 2))
        day_and_amount[day] = day_and_amount.get(day, 0) + amount

    # Process SA orders
    for sales in online:
        date = sales['date']
        day = date.day  # Extract the day of the month
        amount = float(round(sales['daily_revenue'], 2))
        day_and_amount[day] = day_and_amount.get(day, 0) + amount

    return day_and_amount


# Create your models here.
def view_monthly_performance(request):
    # Get the selected month from the query parameters
    selected_month = request.GET.get('month', datetime.now().strftime('%Y-%m'))  # Default to the current month

    # Parse the selected month into year and month
    try:
        year, month = map(int, selected_month.split('-'))
    except ValueError:
        year, month = datetime.now().year, datetime.now().month

    # Aggregate daily revenue for the selected month
    store_sales = StorePurchase.objects.filter(date__year=year, date__month=month).values('date').annotate(
        daily_revenue=Sum('total')
    )
    online_sales = OnlinePurchase.objects.filter(date__year=year, date__month=month).values('date').annotate(
        daily_revenue=Sum('total')
    )

    # Get combined order data
    sales_data = get_order_data(store_sales, online_sales)

    # Prepare data for the chart
    labels = list(sales_data.keys())  # Days of the month
    chart_data = list(sales_data.values())  # Revenue for each day

    context = {
        'selected_month': selected_month,
        'labels': labels,
        'chart_data': chart_data,
    }
    return render(request, 'performance/month_data.html', context)
