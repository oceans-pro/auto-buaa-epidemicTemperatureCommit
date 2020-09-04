
## 服务器部署

操作系统：`centos7` 

### 安装chrome及其驱动
```shell script
# 安装chrome最新版本
yum -y install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
# 查看当前chrome版本，去查找相对应的chromedriver版本，https://npm.taobao.org/mirrors/chromedriver/
# 使用sftp工具将其上传到服务器
# 建立软连接
ln -s /root/software/chromedriver /usr/bin/chromedriver
google-chrome --version
chmod 777 chromedriver # 开启执行权限
```

## 安装python3
```shell script
yum -y install epel-release # 清华镜像
yum repolist
yum -y install python36
pip3 install selenium
```
安装完成后，可保存以下py文件进行测试
```python
# -*- coding:utf-8 -*-
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 确保无头
options.add_argument('--disable-gpu')  # 无需要gpu加速
options.add_argument('--no-sandbox')  # 无沙箱
driver = webdriver.Chrome( options=options)  # 添加软链接后是不需要写路径的

driver.get("https://www.baidu.com")
print(driver.page_source)
driver.quit()
```