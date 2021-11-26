# https://juejin.cn/post/6993558914725838856
# https://zhuanlan.zhihu.com/p/66341662

import collections


def f1():
    return [{'mv_user_name': '其他', 'col1': 'test01', 'col2': 'test02'}, {'mv_user_name': '海马汽车', 'col1': 'test01'}], ['mv_user_name', 'col1', 'col2']


def f2():
    return f1()


a, b = f2()

L = [1, 2, 3]
# print(', '.join(L))  # TypeError: sequence item 0: expected str instance, int found
print(" ".join(str(x) for x in L))
s1 = '%s, ' * (len(b) - 1) + '%s'
print(s1)

print(a)
print(b)
print(', '.join(b))
print(a + b)
print(b + a)
s2 = ', '.join(b)
print(f'insert into ({s2}) VALUES ({s1})')

columns = ', '.join(['date', 'dimension'] + b)
print(columns)

a = 'I'
a += ' am xyg'
print(a)

schemas = ['mv_user_id', 'mv_user_name']
list_columns = ['date', 'dimension'] + schemas
print(list_columns)
columns = ', '.join(list_columns)
values = '%s, ' * (len(list_columns) - 1) + '%s'
db = 'mba'
table = 'tb1'
ins_sql = f'insert into `{db}`.`{table}` ({columns}) VALUES ({values})'
print(ins_sql)

list_dict_data = [{'mv_user_id': 0, 'mv_user_name': '其他'}, {'mv_user_id': 1, 'mv_user_name': '海马汽车'}, {'mv_user_id': 2, 'mv_user_name': '一号店'},
                  {'mv_user_id': 3, 'mv_user_name': 'MediaV'}, {'mv_user_id': 4, 'mv_user_name': '珍爱网'}]
ins_sql_data = []
for dict_line in list_dict_data:
    print(dict_line)
    line = []
    for item in list_columns:
        if item == 'date':
            line.append('2021-11-01')
        elif item == 'dimension':
            line.append('dv')
        else:
            line.append(dict_line[item])
        print(line)

    ins_sql_data.append(tuple(line))
print(ins_sql_data)
