import demjson
from Setting import *
from TaskComparison import *

rc = RedisConnect()
ssrc = SqlServerReadConnect()


def scheduler(user_tables):
    '''
    分配抓取任务
    :return:
    '''
    rc.clear_db('sqlserverdb')
    ssrc.check_task()
    all_tables = rc.read_queue('sqlserverdb')
    for all_table in all_tables:
        value = demjson.decode(all_table.decode())
        table = value['table']
        date = value['date']
        status = value['status']
        printColor(f' 表名：{table} 数据库最新日期：{date} 抓取状态：{status}', '37')
        if status and date != get_before_day(get_today()):
            user_tables = start_task(table, user_tables, date)
    print(user_tables)
    show_tables = {'yes': [], 'no': []}
    for user_table in user_tables:
        if not user_tables[user_table]['tables']:
            continue
        if user_table == 'shiguang658@ten-box.cn':
            lr = LittleRedBook(user_table, user_tables[user_table]['password'])
            for tab in user_tables[user_table]['tables']:
                if tab[0] == '贝德美.XHS.企业号_推广中心_笔记报表':
                    try:
                        lr.spotlight_platform_account_book_main(get_after_day(tab[1]), get_before_day(get_today()))
                        show_tables['yes'].append('贝德美.XHS.企业号_推广中心_笔记报表')
                    except:
                        show_tables['no'].append('贝德美.XHS.企业号_推广中心_笔记报表')
                if tab[0] == '贝德美.XHS.企业号_推广中心_计划报表':
                    try:
                        lr.spotlight_platform_main(get_after_day(tab[1]), get_before_day(get_today()))
                        show_tables['yes'].append('贝德美.XHS.企业号_推广中心_计划报表')
                    except:
                        show_tables['no'].append('贝德美.XHS.企业号_推广中心_计划报表')
        if user_table == '2025005748@qq.com':
            lr = LittleRedBook(user_table, user_tables[user_table]['password'])
            for tab in user_tables[user_table]['tables']:
                if tab[0] == '贝德美.XHS.商品效果_日':
                    try:
                        lr.commodity_as_a_whole_main(get_after_day(tab[1]), get_before_day(get_today()))
                        show_tables['yes'].append('贝德美.XHS.商品效果_日')
                    except:
                        show_tables['no'].append('贝德美.XHS.商品效果_日')
                if tab[0] == '贝德美.XHS.店铺整体_日':
                    try:
                        lr.overall_store_day_main(get_after_day(tab[1]), get_before_day(get_today()))
                        show_tables['yes'].append('贝德美.XHS.店铺整体_日')
                    except:
                        show_tables['no'].append('贝德美.XHS.店铺整体_日')
    erro_dingding(f'成功：{len(show_tables["yes"])}个\n失败{len(show_tables["no"])}个 {show_tables["no"]}')


if __name__ == '__main__':
    user_tables = {
        'shiguang658@ten-box.cn': {'password': 'BDMbdm@456', 'tables': []},
        '2025005748@qq.com': {'password': 'Beidemei@2021', 'tables': []}
    }
    scheduler(user_tables)