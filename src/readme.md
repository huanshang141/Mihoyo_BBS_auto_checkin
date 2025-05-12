# 米游社自动签到
基于[AutoMihoyoBBS](https://github.com/Womsxd/MihoyoBBSTools)实现的轻量米游社自动签到脚本
## 特色
1. 支持（且目前仅支持）GitHub Actions
2. 仅保留各米家游戏的签到，去除了bbs相关的活动（~~因为不会写~~）
3. 支持推送服务（目前只有企业微信机器人）
4. 目前处于早期版本，代码架构一团糟，且有很多冗余代码，（会有人来帮我优化吗
## 使用方法
1. fork本项目
2. 修改`src\config.py`中的config字典，只需要修改`cn`中各游戏的`checkin`值
```python
config = {
    'enable': True, 'version': 14, "push": "",
    'account': {'cookie': '', 'stuid': '', 'stoken': '', 'mid': ''},
    'device': {'name': 'Xiaomi MI 6', 'model': 'Mi 6', 'id': '', 'fp': ''},
    'mihoyobbs': {
        'enable': True, 'checkin': True, 'checkin_list': [5, 2],
        'read': True, 'like': True, 'cancel_like': True, 'share': True
    },
    'games': {
        'cn': {
            'enable': True,
            'useragent': 'Mozilla/5.0 (Linux; Android 12; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Version/4.0 Chrome/103.0.5060.129 Mobile Safari/537.36',
            'retries': 3, # 重试次数
            'genshin': {'checkin': False, 'black_list': []}, # 不启用
            'honkai2': {'checkin': False, 'black_list': []},
            'honkai3rd': {'checkin': False, 'black_list': []},
            'tears_of_themis': {'checkin': False, 'black_list': []},
            'honkai_sr': {'checkin': True, 'black_list': []},# 启用
            'zzz': {'checkin': True, 'black_list': []}
        },
		#...
    },
	#...
}
```
3. 获取cookie，请参考[获取cookie](https://github.com/Womsxd/MihoyoBBSTools?tab=readme-ov-file#%E8%8E%B7%E5%8F%96%E7%B1%B3%E6%B8%B8%E7%A4%BE-cookie)
4. 添加secret，方法参考[添加secret](https://github.com/enpitsuLin/skland-daily-attendance?tab=readme-ov-file#%E6%B7%BB%E5%8A%A0-cookie-%E8%87%B3-secrets)，需要添加的secret名为`COOKIE`，支持使用`,`分割的多用户
5. 启动Actions，参考[启动Actions](https://github.com/enpitsuLin/skland-daily-attendance?tab=readme-ov-file#%E5%90%AF%E5%8A%A8-github-action)
## TODO
- [ ] 把TODO写了
## 鸣谢
[AutoMihoyoBBS](https://github.com/Womsxd/MihoyoBBSTools): 本项目核心代码均来自此
Github Copilot: 本项目其他代码均来自于此