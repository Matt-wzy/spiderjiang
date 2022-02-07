
import sqlite3
import random

src = 'abcdefghijklmnopqrstuvwxyz'

def get_str(x,y):
    str_sum = random.randint(x,y)
    astr = ''
    for i in range(str_sum):
        astr += random.choice(src)
    return astr

# 输出指定记录
def output():
    cur.execute('select * from mytab')
    for sid,name,ps in cur:
        print(sid,' ',name,' ',ps)

# 输出全部记录
def output_all():
    cur.execute('select * from mytab')
    for item in cur.fetchall():
        print(item)

#
def get_data_list(n):
    res = []
    for i in range(n):
        res.append((get_str(2,4),get_str(8,12)))
    return res


if __name__ == '__main__':
    print('建立连接...')
    con = sqlite3.connect(':memory:')
    print('建立游标...')
    cur = con.cursor()
    print('建立一张表mytab...')
    #cur.execute('drop table mytab')
    cur.execute('create table mytab(id integer primary key autoincrement not null,name text,passwd text)')
    print('插入一条记录...')
    cur.execute('insert into mytab (name,passwd) values(?,?)',(get_str(2,4),get_str(8,12),))
    print('显示所有记录....')
    output()
    print('批量插入多条记录...')
    cur.executemany('insert into mytab (name,passwd)values(?,?)',get_data_list(3))
    print('显示所有记录...')
    output()
    print('批量插入多条记录...')
    cur.executemany('insert into mytab(name,passwd) values(?,?) ',get_data_list(3))
    print('显示所有记录...')
    output_all()
    print('更新一条记录....')
    cur.execute('update mytab set name =? where id=?',('aaa',1))
    print('显示所有记录...')
    output()
    print('删除一条记录')
    cur.execute('delete from mytab where id=?',(3,))
    print('显示所有记录')
    output()
    cur.close()
    con.close()
