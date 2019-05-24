def yyyymmToMonthName(p_yyyymm):
    res = p_yyyymm[:4]
    mm = int(p_yyyymm[4:])
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    res = res + '-' + months[mm-1]
    return res
