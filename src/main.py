#  coding=utf-8
'''
main
@author: Shuaichi Li
@email: shuaichi@mail.dlut.edu.cn
@date: 2020/12/01 15:46
'''

#  import
import time
import datetime
from selenium import webdriver
import smtplib
from email.mime.text import MIMEText
import traceback


class Reserve(object):
    def __init__(self, user_id, password, wanted_seats, email, library_name, reading_room):
        self.user_id = user_id
        self.password = password
        self.wanted_seats = wanted_seats
        self.email = email
        self.library_map = {'伯川': '17', '令希': '32'}
        self.library_readingroom_map = {'17': {301: '168', 312: '170', 401: '195',\
                                               404: '197', 409: '196', 501: '198',\
                                               504: '199', 507: '200'},\
                                        '32': {301: '207', 302: '208', 401: '205',\
                                               402: '206', 501: '203', 502: '204',\
                                               601: '201', 602: '202', 202: '242'}
                                        }
        self.library_name = library_name
        self.reading_room = reading_room
        self.library_id = self.library_map.get(library_name)
        self.reading_room_id = self.library_readingroom_map.get(self.library_id).get(reading_room)

    def send_email(self, seat_id=None, successful=True):

        # 设置服务器所需信息
        # 163邮箱服务器地址
        mail_host = 'smtp.163.com'
        # 163用户名
        mail_user = 'xxxx@163.com'
        # 密码(部分邮箱为授权码)
        mail_pass = '****'
        # 邮件发送方邮箱地址
        sender = 'xxxx@163.com'
        # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        receivers = self.email

        # 设置email信息
        # 邮件内容设置
        if successful:
            context = '座位预定成功，座位位于' + self.library_name + '图书馆' + str(self.reading_room) + '阅览室的' + str(seat_id)
        else:
            context = '座位预定失败，今天你不能去图书馆自习了'
        message = MIMEText(context, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = '图书馆座位预定'
        # 发送方信息
        message['From'] = sender
        # 接受方信息
        message['To'] = receivers[0]

        # 登录并发送邮件
        try:
            smtpObj = smtplib.SMTP()
            # 连接到服务器
            smtpObj.connect(mail_host, 25)
            # 登录到服务器
            smtpObj.login(mail_user, mail_pass)
            # 发送
            smtpObj.sendmail(
                sender, receivers, message.as_string())
            # 退出
            smtpObj.quit()
            print('success')
        except smtplib.SMTPException as e:
            print('error', e)  # 打印错误

    def reserve(self, browser):

        '''登录'''
        browser.get(
            "https://sso.dlut.edu.cn/cas/login?service=http://seat.lib.dlut.edu.cn/yanxiujian/client/login.php?redirect=index.php")
        input_userid = browser.find_element_by_id('un')
        input_userid.send_keys(self.user_id)
        input_password = browser.find_element_by_id('pd')
        input_password.send_keys(self.password)
        login_button = browser.find_element_by_class_name('login_box_landing_btn')
        login_button.click()

        '''根据想要去的房间号，选取第二天的座位'''
        time_today = (datetime.datetime.now() + datetime.timedelta(days=1)).timetuple()
        today = str(time_today.tm_year) + '/' + str(time_today.tm_mon) + '/' + str(time_today.tm_mday)
        url = 'http://seat.lib.dlut.edu.cn/yanxiujian/client/orderSeat.php?method=addSeat&room_id=' + self.reading_room_id +'&areaid=' + self.library_id + '&curdate=' + today
        browser.get(url)
        today_button = browser.find_element_by_id('todayBtn')
        today_button.click()
        tomorrow_button = browser.find_element_by_id('nextDayBtn')
        tomorrow_button.click()
        time.sleep(1)

        # 直接选择座位
        flag = False
        for seat_id in self.wanted_seats:
            seat = browser.find_element_by_xpath("//table/tbody//tr//td/div[@class='seat-normal']/i[contains(text()," + str(seat_id) + ")]")
            seat.click()
            confirm_button = browser.find_element_by_id('btn_submit_addorder')
            time.sleep(0.5)
            try:
                confirm_button.click()
                print('seat has been reserved successfully!')
                flag = True
                self.send_email(seat_id, successful=True)
                break
            except Exception as e:
                traceback.extract_stack()
                print(e)
                continue

        if not flag:
            self.send_email(successful=False)

        '''注销操作并关闭窗口'''
        browser.get("http://seat.lib.dlut.edu.cn/yanxiujian/client/loginOut.php")
        time.sleep(2)


if __name__ == '__main__':

    browser = webdriver.Chrome(executable_path='../driver/chromedriver.exe')
    browser.maximize_window()

    # 用户名密码配置信息, 可选多人
    user_id = 'xxxx'
    password = '****'
    email = 'xxxx@163.com'
    user_id_n = 'xxxx'
    password_n = '****'
    email_n = 'xxxx@163.com'

    # 输入需要的图书馆和座位候选座位
    wanted_seats = [001, 002, 003, 004] # 请输入完整的3位座位号（如不足请用0补足）
    library_name = '伯川' # 请输入伯川或令希
    reading_room = 301 # 请预先在系统上确定要指定的阅览室

    user1 = Reserve(user_id_n, password_n, wanted_seats, email_n, library_name, reading_room)
    # user2 = Reserve(user_id, password, wanted_seats, email, library_name, reading_room)

    user1.reserve(browser)
    # user2.reserve(browser)

    browser.close()
