import datetime
import dateutil.relativedelta

"""
    Format a string representing a month in '%Y%m' format to '%Y-%b'
    Doesn't use buildin format python functions because we have a custom string date format from database.
    If parameter doesn't fit expected format we return it without changes
    usage::

        >>> import utils
        >>> input_date = '201904'
        >>> output_date = u.yyyymmToMonthName(input_date)
        >>> # should return '2019-Apr'

    :param p_yyyymm: input string representing a year month date
    :rtype: string
"""
def yyyymmToMonthName(p_yyyymm):
    try:
        if len(p_yyyymm) != 6:
            # different lengths will end up in unexpected output
            return p_yyyymm
        res = p_yyyymm[:4]
        mm = int(p_yyyymm[4:])
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        res = res + '-' + months[mm-1]
        return res
    except:
        # anything that raises an exception is considered a bad input format
        return p_yyyymm


"""
    Add months to a string representing a date in format %Y%m
    If parameter doesn't fit expected format we return it without changes
    usage::

        >>> import utils
        >>> input_date = '201904'
        >>> output_date = u.yyyymm_add_months(input_date, +1)
        >>> # should return '201905'

    :param p_yyyymm: input string representing a year month date
    :param p_inc: input number of months to add/substract
    :rtype: string

"""
def yyyymm_add_months(p_yyyymm, p_inc):
    try:
        if len(p_yyyymm) != 6:
            # different lengths will end up in unexpected output
            return p_yyyymm
        given_month = datetime.datetime.strptime(p_yyyymm+'01', '%Y%m%d')
        result_month = given_month + dateutil.relativedelta.relativedelta(months=p_inc)
        res = str(result_month.year) + str(result_month.month).zfill(2)
        return res
    except:
        # anything that raises an exception is considered a bad input format
        return p_yyyymm
