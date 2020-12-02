# coding=utf-8
'''
main
@author: Shuaichi Li
@email: shuaichi@mail.dlut.edu.cn
@date: 2020/12/01 15:46
'''

# import
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

user_id = '学号'
password = '校园门户密码'

browser = webdriver.Chrome(executable_path='chromedriver的路径')
browser.maximize_window()

'''登录'''
browser.get("https://sso.dlut.edu.cn/cas/login?service=http://seat.lib.dlut.edu.cn/yanxiujian/client/login.php?redirect=index.php")
input_userid = browser.find_element_by_id('un')
input_userid.send_keys(user_id)
input_password = browser.find_element_by_id('pd')
input_password.send_keys(password)
login_button = browser.find_element_by_class_name('login_box_landing_btn')
login_button.click()

'''更改想要去的房间号，选取第二天的座位图'''
browser.get('http://seat.lib.dlut.edu.cn/yanxiujian/client/orderSeat.php?room_id=199')
today_button = browser.find_element_by_id('todayBtn')
today_button.click()
tomorrow_button = browser.find_element_by_id('nextDayBtn')
tomorrow_button.click()
time.sleep(1)

'''想要中间的座位，页面向下滚动'''
# browser.execute_script('window.scrollTo(0, 400)')
for _ in range(15):
    ActionChains(browser).key_down(Keys.DOWN).perform() #滚到屏幕中央
time.sleep(0.5)

'''从左边开始点击，如果被占，点击没有反应，继续向右点击，在弹出窗口中确认'''
ActionChains(browser).move_by_offset(235, 175).click().perform()
for _ in range(16):
    ActionChains(browser).move_by_offset(45, 0).click().perform()
    time.sleep(0.2)
    confirm_button = browser.find_element_by_id('btn_submit_addorder')
    # cancel_button = browser.find_element_by_id('btn_reset')
    try:
        time.sleep(0.5)
        confirm_button.click()
        # cancel_button.click()
        break
    except:
        continue
time.sleep(2)

'''注销操作并关闭窗口'''
browser.get("http://seat.lib.dlut.edu.cn/yanxiujian/client/loginOut.php")
time.sleep(2)
browser.close()
