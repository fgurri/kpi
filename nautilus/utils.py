import datetime
import dateutil.relativedelta

def yyyymmToMonthName(p_yyyymm):
    res = p_yyyymm[:4]
    mm = int(p_yyyymm[4:])
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    res = res + '-' + months[mm-1]
    return res


def yyyymm_add_months(p_yyyymm, p_inc):
    given_month = datetime.datetime.strptime(p_yyyymm+'01', '%Y%m%d')
    result_month = given_month + dateutil.relativedelta.relativedelta(months=p_inc)
    res = str(result_month.year) + str(result_month.month).zfill(2)
    return res
