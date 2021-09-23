from baseapi import *
'''统计2021年批次的总数'''
total = 4 #当总数为4时，发送邮件告警。当前月份：5、7

def putin_info():
    driver.get('http://edu.hangzhou.gov.cn/')
    time.sleep(2)
    logging.info('页面加载完成')
    print('------------------------------------------------')
    driver.execute_script('window.stop()')#页面停止加载

def click_jiaoshipingpin():
    element=driver.find_element_by_xpath('/html/body/div[2]/div[10]/div[6]/div[2]/div[1]/a[2]')
    element.click()
    time.sleep(2)
    logging.info('进入教师评聘界面')
    print('------------------------------------------------')

def click_jiaoshizhaopin():
    element=driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div[1]/ul/li[1]/a')
    element.click()
    time.sleep(2)
    logging.info('进入教师招聘界面')
    print('------------------------------------------------')

def get_title(page,title_list):
    while True:
        try:
            '''寻找当前页面的title'''
            elements=driver.find_elements_by_partial_link_text('批次）')#模糊匹配
            for e in elements:
                title_list.append(e.get_attribute('title'))
            return title_list,page
        except:
            '''如果没找到title，则翻页，直至找到title'''
            element_click=driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div[2]/div[2]/ul/div/table/tbody/tr/td/table/tbody/tr/td[6]/a')
            element_click.click()
            page = page + 1
            time.sleep(2)
            print('寻找下一页')

def get_count():
    '''统计2021年批次的总数'''
    title_list = []
    count = 0
    page = 1 #当前页数
    #完成初始化
    title_list,page=get_title(page,title_list)#title总数
    count = len(title_list)
    print('当前页数为 {} ，共由 {} 个title'.format(page,count))
    print(title_list)
    print('------------------------------------------------')
    while '杭州市教育局所属事业单位公开招聘教职工公告（2021年5月批次）' not in title_list:
        '''由于列表中没找到目标title，需要翻页，继续查找'''
        element_click=driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div[2]/div[2]/ul/div/table/tbody/tr/td/table/tbody/tr/td[6]/a')
        element_click.click()
        page = page + 1
        time.sleep(2)
        #重复查找过程
        title_list,page=get_title(page,title_list)#title总数
        count = len(title_list)
        print('当前页数为 {} ，共由 {} 个title'.format(page,count))
        print(title_list)
    return count


def send_email():
    """
    如果count = total 发送邮件告警
    param:
        msg_from   发送方邮箱
        passwd     发送方密码
        msg_to     收件方邮箱
        subject    邮件主题
        content    邮件内容
        s          邮件服务器及端口号
    """
    msg_from='1141029485@qq.com'
    passwd='llvovkzqippvhegf'
    msg_to='1141029485@qq.com'
    subject='杭州教师招聘'
    content='最新批次已发布'

    msg=MIMEText(content)
    msg['Subject']=subject
    msg['From']=msg_from
    msg['To']=msg_to
    
    try:
        s=smtplib.SMTP_SSL("smtp.qq.com",465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        logging.info('邮件通知，发送成功')
    except smtplib.SMTPAuthenticationError as e:
        logging.info('邮件发送失败,未配置邮件客户端')
        logging.info(e)
    finally:
        s.quit()

def check_count():
    if count == total:
        #发送邮件
        send_email()
    else:
        pass

putin_info()
click_jiaoshipingpin()
click_jiaoshizhaopin()
count = get_count()
check_count()

