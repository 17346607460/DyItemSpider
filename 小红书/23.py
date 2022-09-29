
chrome = ChromeOption()
xhs = LittleRedBook()
# #
# 小红书后台cookie
xhs_cookie = chrome.xhs_login()
# # # # 贝德美.XHS.商品效果_日
xhs.commodity_as_a_whole_main('', '', xhs_cookie)
# # # # 贝德美.XHS.店铺整体_日
xhs.overall_store_day_main('', '', xhs_cookie)
chrome.__del__()
time.sleep(3)

chrome = ChromeOption()
# # 小红书蒲公英cookie
xhs_cookie = chrome.xhsjg_login()
# 贝德美.XHS.企业号_推广中心_计划报表
xhs.spotlight_platform_main('', '', xhs_cookie)
# 贝德美.XHS.企业号_推广中心_笔记报表
xhs.spotlight_platform_account_book_main('', '', xhs_cookie)
# # # # 贝德美.XHS.企业号_推广中心_单元报表
xhs.promotion_center_unit_report_main('', '', xhs_cookie)
# # # # # 贝德美.XHS.企业号_推广中心_创意报表
xhs.promotion_center_creative_report_main('', '', xhs_cookie)
# xhs.check_xhs_id('62ea4dd30000000012004b3a')