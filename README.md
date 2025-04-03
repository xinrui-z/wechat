
## 不懂看这里，文件下载直接使用
```commandline
链接:https://pan.baidu.com/s/1H89Y6tuk7ugG-Lh6FKyUvw?pwd=pmf7
```


## 前置条件
注册一个微信公众号

https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login 

扫码登录成功后，就可以生成微信公众测试号的appID和appsecret
扫描测试号二维码后会生成微信号，那个账号需要接收就扫码

## 新增测试模板
模板标题: 自定义，例如: 宝宝，晚上好!  
模板内容参考:  
```
☀️今天是{{date.DATA}}
🌇城市：{{city.DATA}}
🌤️天气：{{weather.DATA}}
⛅最低气温： {{min_temperature.DATA}}
🌡️最高气温：{{max_temperature.DATA}}
🌈{{chp.DATA}}❤️
💏今天是我们恋爱的第{{love_day.DATA}}天
🍰距离小可爱的生日还有{{birthday.DATA}}天
🎉我们结婚{{marryday.DATA}}天啦
👧生理期{{period.DATA}}
📚{{note_en.DATA}}{{note_ch.DATA}}
```

```
☀️今天是{{date.DATA}}，我们认识的第{{love_day.DATA}}天

🍰距离你的的生日还有{{birthday.DATA}}天~

🌇城市：{{city.DATA}}
🌅日出时间：{{sunrise.DATA}}
🌄日落时间：{{sunset.DATA}}

🏝下面开始播报{{city.DATA}}今日的天气~
🌤️天气：{{weather.DATA}}
⛅最低气温： {{min_temperature.DATA}}℃
🌡️最高气温：{{max_temperature.DATA}}℃
🔥风向：{{wind_direction.DATA}}
🌿风力：{{wind_speed.DATA}}

ദ്ദി˶•̀֊<)✧ 缓慢又笨拙的路上，谢谢你陪我长大🥰~

```
## 安装python3 
官方网站: https://www.python.org/getit/

## 安装requests包
打开cmd，执行以下命令
```commandline
pip3 install requests
```

## 修改配置文件
`app_id`: 测试号信息里的appID 

`app_secret`: 测试信息里的appsecret

`template_id`: 模板消息接口里的模板ID

`user`: 测试号里的用户微信号

`province`: 所在省份

`city`: 所在城市

`birthday`: 生日

`love_date`: 在一起的日子

`marry_date`: 结婚日期

`last`: 最近一次生理期开始时间

`periodd_cycle`: 生理期周期

`period_days`: 生理期持续天数

## 运行程序
```commandline
python3 main.py
```
