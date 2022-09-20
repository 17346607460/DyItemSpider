from 小红书.Module import *


def start_task(table, user_tables, date):
    user_tables['shiguang658@ten-box.cn']['tables'].append(['贝德美.XHS.企业号_推广中心_计划报表', date]) if table == '贝德美.XHS.企业号_推广中心_计划报表' else 0
    user_tables['shiguang658@ten-box.cn']['tables'].append(['贝德美.XHS.企业号_推广中心_笔记报表', date]) if table == '贝德美.XHS.企业号_推广中心_笔记报表' else 0
    user_tables['2025005748@qq.com']['tables'].append(['贝德美.XHS.店铺整体_日', date]) if table == '贝德美.XHS.店铺整体_日' else 0
    user_tables['2025005748@qq.com']['tables'].append(['贝德美.XHS.商品效果_日', date]) if table == '贝德美.XHS.商品效果_日' else 0
    return user_tables
