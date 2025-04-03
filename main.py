from time import time, localtime
import cityinfo
import config
from requests import get, post,exceptions
from datetime import datetime, date, timedelta


def get_access_token():
    # appId
    app_id = config.app_id
    # appSecret
    app_secret = config.app_secret
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    access_token = get(post_url).json()['access_token']
    print(access_token)
    return access_token


def get_chp():
    get_url = "https://api.shadiao.pro/chp"
    headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    chp = get(get_url, headers=headers).json()['data']['text']
    return chp


def get_weather(province, city):
    # 城市id
    city_id = cityinfo.cityInfo[province][city]["AREAID"]
    # city_id = 101280101
    # 毫秒级时间戳
    t = (int(round(time() * 1000)))
    headers = {
      "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
    response = get(url, headers=headers)
    response.encoding = "utf-8"
    response_data = response.text.split(";")[0].split("=")[-1]
    response_json = eval(response_data)
   # print(response_json)
    print(response_json)
    weatherinfo = response_json["weatherinfo"]
    # 天气
    weather = weatherinfo["weather"]
    # 最高气温
    temp = weatherinfo["temp"]
    # 最低气温
    tempn = weatherinfo["tempn"]
    # 风力
    wind_direction = weatherinfo["wd"]
    wind_speed = weatherinfo["ws"]
    return weather, temp, tempn, wind_direction,wind_speed


def get_ciba():
    url = "http://open.iciba.com/dsapi/"
    headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    note_en = r.json()["content"]
    note_ch = r.json()["note"]
    fenxiang = r.json()["fenxiang_img"]
    return note_ch, note_en, fenxiang

def menstrual():
    cycle = config.periodd_cycle
    days = config.period_days
    result = ""
    layout = "%Y-%m-%d"
    now = datetime.now()
    curr_date = datetime(now.year, now.month, now.day, 0, 0, 0, 0)
    start_date = datetime.strptime(config.last, layout)
    duration = curr_date - start_date
    days_delta = int(duration.total_seconds() / 86400)
    zhen = days_delta // cycle

    # Calculate the last start time
    if zhen <= 1:
        last_start = start_date
    else:
        last_start = start_date + timedelta(days=zhen * cycle)

    days_from_last = int((curr_date - last_start).total_seconds() / 86400)
    next_start = last_start + timedelta(days=cycle)

    if days_from_last <= days:
        if days_from_last == days:
            result = "将在今天结束，下次开始日期为：{}".format(next_start.strftime(layout))
        else:
            result = "还剩{}天，将在{}结束".format(days - days_from_last, (last_start + timedelta(days=days)).strftime(layout))
    else:
        days_to_next_start = int((next_start - curr_date).total_seconds() / 86400)
        result = "下次开始日期为：{}，离今天还剩{}天".format(next_start.strftime(layout), days_to_next_start)

    return result


def calculate_period_cycle():
    history_period_start_date = datetime.strptime(config.last, "%Y-%m-%d").date() #date(2023, 5, 12)
    period_cycle = config.periodd_cycle
    period_days = config.period_days
    # 计算下一次开始时间
    next_period_start_date = history_period_start_date
    current_date = date.today()
    while next_period_start_date <= current_date:
        next_period_start_date += timedelta(days=period_cycle)
        next_period_end_date = next_period_start_date + timedelta(days=period_days)
    # 根据下一次开始的时间计算，上一次开始的时间
    last_period_start_date = next_period_start_date - timedelta(days=period_cycle)
    # 根据上一次开始时间计算上一次结束的时间
    last_period_end_date = last_period_start_date + timedelta(days=period_days)
    # 判断当前是否处在生理期中，并计算还剩几天结束
    if last_period_start_date <= current_date <= last_period_end_date:
        days_left_in_period = (last_period_end_date - current_date).days
        return "还剩" + str(days_left_in_period) + "天，将在" + last_period_end_date.strftime("%Y-%m-%d") + "结束"
    else:
        days_to_next_period_start = (next_period_start_date - current_date).days
        return "开始日期为：" + next_period_start_date.strftime("%Y-%m-%d") + "，离今天还剩" + str(days_to_next_period_start) + "天"

    # 计算日出日落


def get_sunrise_sunset(lat=23.37, lng=102.42):
    """
    获取指定经纬度的日出日落时间（自动转换为北京时间）
    参数：
        lat: 纬度（默认红河县纬度）
        lng: 经度（默认红河县经度）
    返回：
        包含北京时间的所有天文时间数据的字典
    """
    # 1. 调用API
    api_url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    try:
        response = get(api_url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()

        if data['status'] != 'OK':
            raise ValueError("API返回状态不正常")

        # 2. 转换UTC时间到北京时间（UTC+8）
        def convert_time(utc_time_str):
            utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S%z")
            beijing_time = utc_time + timedelta(hours=8)
            return beijing_time.strftime("%H:%M:%S")

        # 3. 处理所有时间字段
        result = {
            'sunrise': convert_time(data['results']['sunrise']),
            'sunset': convert_time(data['results']['sunset']),
            'solar_noon': convert_time(data['results']['solar_noon']),
            'day_length': data['results']['day_length'],
            'civil_twilight_begin': convert_time(data['results']['civil_twilight_begin']),
            'civil_twilight_end': convert_time(data['results']['civil_twilight_end']),
            'status': 'OK',
            'timezone': 'UTC+8 (北京时间)'
        }

        return result

    except exceptions.RequestException as e:
        return {'status': 'ERROR', 'message': f'网络请求失败: {str(e)}'}
    except Exception as e:
        return {'status': 'ERROR', 'message': f'处理数据时出错: {str(e)}'}

def send_message(to_user, access_token, city_name, weather, max_temperature, min_temperature,wind_direction,wind_speed,sunrise,sunset):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六","星期日"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    #print(today)
    #print(today.isoweekday())
    week = week_list[today.isoweekday()-1]
    #print(week)
    # 获取在一起的日子的日期格式
    love_year = int(config.love_date.split("-")[0])
    love_month = int(config.love_date.split("-")[1])
    love_day = int(config.love_date.split("-")[2])
    love_date = date(love_year, love_month, love_day)
    #计算结婚倒计时日期
    marry_year = int(config.marry_date.split("-")[0])
    marry_month = int(config.marry_date.split("-")[1])
    marry_day = int(config.marry_date.split("-")[2])
    marry_date = date(marry_year, marry_month, marry_day)
    marry_days = str(today.__sub__(marry_date)).split(" ")[0]
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取生日的月和日
    birthday_month = int(config.birthday.split("-")[1])
    birthday_day = int(config.birthday.split("-")[2])
    # 今年生日
    year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    #计算生理期
    period = menstrual()
    data = {
        "touser": to_user,
        "template_id": config.template_id,
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": "#00FFFF"
            },
            "city": {
                "value": city_name,
                "color": "#808A87"
            },
            "weather": {
                "value": weather,
                "color": "#ED9121"
            },
            "min_temperature": {
                "value": min_temperature,
                "color": "#00FF00"
            },
            "chp": {
              "value": chp,
              "color": "#7B68EE"
            },
            "max_temperature": {
              "value": max_temperature,
              "color": "#FF6100"
            },
            "wind_direction": {
                "value": wind_direction,
                "color": "#FF6100"
            },
            "wind_speed": {
                "value": wind_speed,
                "color": "#FF6100"
            },
            "sunrise": {
                "value": sunrise,
                "color": "#FF6100"
            },
            "sunset": {
                "value": sunset,
                "color": "#FF6100"
            },
            "love_day": {
              "value": love_days,
              "color": "#87CEEB"
            },
            "birthday": {
              "value": birth_day,
              "color": "#FF8000"
            },
	    "marryday": {
              "value": marry_days,
              "color": "#FF0000"
            },
            "period": {
              "value": period,
              "color": "#FF0000"
            },
            "note_en": {
                "value": note_en,
                "color": "#173177"
            },
            "note_ch": {
                "value": note_ch,
                "color": "#173177"
            }
        }
    }
    headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data)
    #print(response.text)


# 获取accessToken
accessToken = get_access_token()
#print(accessToken)
# 接收的用户
user1 = config.user1
user2 = config.user2
# 传入省份和市获取天气信息
province, city = config.province, config.city
weather, max_temperature, min_temperature, wind_direction, wind_speed = get_weather(province, city)
# 获取词霸每日金句
note_ch, note_en, fenxiang = get_ciba()

# 获取彩虹屁
chp = get_chp()

# 获取日出日落时间
sun_data = get_sunrise_sunset()
sunrise=sun_data['sunrise']
sunset=sun_data['sunset']

print(sunrise)
print(sunset)

# 公众号推送消息
# send_message(user1, accessToken, city, weather, max_temperature, min_temperature, wind_direction, wind_speed)
send_message(user2, accessToken, city, weather, max_temperature, min_temperature, wind_direction, wind_speed,sunrise,sunset)
