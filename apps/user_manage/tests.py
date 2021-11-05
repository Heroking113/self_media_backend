s = '''bond_code
bond_abbr
purchase_date
purchase_code
purchase_limit
underly_code
underly_abbr
underly_price
conversion_price
conversion_value
cur_bond_price
conversion_preminum_rate
abos_erd
abos_aps
issurance_scale
ido_wln
win_rate
time_market'''
# s = s.replace(' ', '')
s = s.replace('\n', ',')
ls = s.split(',')
ls = ','.join(["'"+i+"'" for i in ls])
print(ls)