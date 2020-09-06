import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait


def log(file, data):
    success_time = datetime.now()
    file.write(str(success_time) + '\n')
    file.write(data + '\n')


def log_data(driver, file):
    """
    1. 填报日期
    2. 姓名
    3. 学工号
    4. 地址 *
    5. 范围 *
    6. 是否在校
    7. 是否外出
    8. 是否隔离
    9. 其他情况  （不填）
    """
    key_arr = ['填报日期', '姓名', '学工号', '地址', '温度范围', '是否在校', '是否外出', '是否隔离']
    document = driver
    value_arr = []
    input_list = document.find_elements_by_tag_name('input')
    for dom_input in input_list:
        value = dom_input.get_attribute('value')
        value_arr.append(value)

    span_list = document.find_elements_by_css_selector('.active+span')
    for dom_span in span_list:
        value = dom_span.text
        value_arr.append(value)

    # 拼接JSON
    result_map = {}
    for i in range(8):
        result_map[key_arr[i]] = value_arr[i]
    print(result_map)

    # 将cookies保存为json格式

    log(file, '4. 当前填报信息为\n' + json.dumps(result_map, ensure_ascii=False) + '\r\n')
    # driver.quit()


def auto_submit(username, password):
    filename = 'report/' + username + '.log'
    file = open(filename, 'a', encoding='utf-8')

    print('0. 执行脚本')
    log(file, '0. 执行脚本')
    # 将chromedriver放到python脚本的文件夹下面，比如（`Anaconda3\Scripts`）
    # 就可以不用每次手动指定目录了
    # driver = webdriver.Chrome('d:/software/dev/chromedriver.exe')
    options = webdriver.ChromeOptions()
    # 无头无法获取地址
    # for debug
    options.add_argument('--headless')  # 确保无头，对于无界面系统
    options.add_argument('--disable-gpu')  # 无需要gpu加速
    options.add_argument('--no-sandbox')  # 无沙箱
    # options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)  # 添加软链接后是不需要写路径的
    driver.get('https://app.buaa.edu.cn/site/ncov/xisudailyup')
    document = driver
    driver.execute_cdp_cmd(
        "Browser.grantPermissions",
        {
            "origin": "https://app.buaa.edu.cn/",
            "permissions": ["geolocation"]
        },
    )
    driver.execute_cdp_cmd(
        "Emulation.setGeolocationOverride",
        {
            "latitude": 40.154693,
            "longitude": 116.276079,
            "accuracy": 1
        })
    js = 'window.location.reload()'
    driver.execute_script(js)
    WebDriverWait(driver, 10).until(lambda d: d.find_element_by_class_name('btn'))
    print('1. 进入登录页面')
    log(file, '1. 进入登录页面')

    dom_username = document.find_elements_by_tag_name('input')[0]
    dom_password = document.find_elements_by_tag_name('input')[1]
    dom_login_btn = document.find_element_by_class_name('btn')
    # stale element reference: element is not attached to the page document
    dom_username.send_keys(username)
    dom_password.send_keys(password)
    dom_login_btn.click()
    time.sleep(1.5)
    try:
        document.find_element_by_class_name('wapat-title')
        print('【用户名或密码错误】')
        log(file, '【用户名或密码错误】')
        return driver.quit()
    except NoSuchElementException:

        # 是否已经填报过？
        driver.implicitly_wait(10)
        time.sleep(1)
        print('2. 进入填报页面')
        log(file, '2. 进入填报页面')
        dom_submit_btn = document.find_element_by_css_selector('.footers a')
        tip = dom_submit_btn.text
        need_commit = tip.find('提交信息') > -1

        if need_commit:
            time.sleep(1)
            dom_btn_tw = document.find_element_by_css_selector('[name=tw] div div span')
            dom_btn_pos = document.find_element_by_css_selector('[name=area] input')
            dom_submit_btn = document.find_element_by_css_selector('.footers a')

            dom_btn_tw.click()
            dom_btn_pos.click()
            time.sleep(2)
            # check
            try:
                dom_submit_btn.click()
                time.sleep(1)
                dom_confirm = document.find_element_by_css_selector('.wapcf-btn-ok')
                dom_confirm.click()
                print('3. 提交成功')
                log(file, '3. 提交成功')
                log_data(driver, file)
            except Exception as ex:
                print('4. 提交失败')
                log(file, '3. 提交失败')
                log(file, str(ex))
        else:
            print('3. 不需要提交 ：' + tip)
            log(file, '3. 不需要提交 ：' + tip)
            log_data(driver, file)
        file.close()
        driver.quit()


if __name__ == '__main__':
    with open('./users.secret.json', 'r', encoding='UTF-8') as f:
        userlist = json.load(f)
    for item in userlist:
        print(item)
        auto_submit(item['username'], item['password'])
