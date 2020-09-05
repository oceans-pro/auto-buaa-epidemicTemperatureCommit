## 说明
- 本脚本的动机是在**忘记**打卡的时候，系统自动帮忙打卡，减少提醒人员（reminder）的工作量。
- 尽量使用手工打卡，定时任务设置在ddl的前一个小时。
- 代码中的定位为**北京昌平区**，如果为学院路校区请记得修改经纬度 
- 百度地图拾取坐标系统连接为： http://api.map.baidu.com/lbsapi/getpoint/index.html

## 使用方法

### 一、安装chrome及其驱动
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

### 二、安装python3
```shell script
yum -y install epel-release # 清华镜像
yum repolist
yum -y install python36
pip3 install selenium
```
### 三、配置用户名和密码
在main.py同级新建`user.secret.json`文件，填入学号和密码（如下所示，可填入多个）。
```json
[
  {
    "username": "sy1906888",
    "password": "mima"
  },
  {
    "username": "xxx",
    "password": "xxx"
  }
]
```

### 四、做成定时服务
windows：对于win10，可使用`任务计划程序`，每天定时执行（需要保持电脑开机..），具体步骤可以百度。

linux：可参考我的配置步骤

将放在 main.py放到 ~/reminder-helper 目录下
```shell script
# 列出全部的定时任务
crontab -l 
# 编辑定时任务
contab -e 
```

```shell script
# 每天下午5点打卡
0 0 17 * * ? python3 ~/reminder-helper/main.py
```