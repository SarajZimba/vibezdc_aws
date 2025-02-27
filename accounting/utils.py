from pyBSDate import convert_AD_to_BS
from datetime import datetime

from organization.models import Organization

def get_fiscal_year():
    org = Organization.objects.first()
    return org.get_fiscal_year()


def calculate_depreciation(amount, percentage, bill_date):
    date_format = '%Y-%m-%d'
    ad_date = datetime.strptime(str(bill_date), date_format)
    year, month, day = ad_date.year, ad_date.month, ad_date.day
    bs_date = convert_AD_to_BS(year, month, day)
    nepali_month_int = bs_date[1]
    depreciation_amount = 0
    amount= float(amount)
    if nepali_month_int <= 3:
        depreciation_amount = (amount*(percentage/100))/3
    elif nepali_month_int <= 9:
        depreciation_amount = amount*(percentage/100)
    else:
        depreciation_amount = (amount*(percentage/100))*2/3
    return depreciation_amount, bs_date


class ProfitAndLossData():

    @staticmethod
    def get_data(revenues, expenses):
        revenue_list= []
        revenue_total = 0
        expense_list= []
        expense_total = 0

        for revenue in revenues:
            revenue_list.append({'title':revenue.ledger_name, 'amount': revenue.total_value})
            revenue_total += revenue.total_value

        for expense in expenses:
            expense_list.append({'title':expense.ledger_name, 'amount': expense.total_value})
            expense_total += expense.total_value

        return expense_list, expense_total, revenue_list, revenue_total