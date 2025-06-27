import collections
import os
import yaml
from copy import deepcopy

from src.utils.loghelper import log
from src.utils import tools

# 这个字段现在还没找好塞什么地方好，就先塞config这里了
serverless = False
# 提示需要更新config版本
update_config_need = False
# 检测是否在GitHub Actions环境中运行
is_github_action = os.getenv("GITHUB_ACTIONS") == "true"

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
            'retries': 3,
            'genshin': {'checkin': True, 'black_list': []},
            'honkai2': {'checkin': False, 'black_list': []},
            'honkai3rd': {'checkin': False, 'black_list': []},
            'tears_of_themis': {'checkin': False, 'black_list': []},
            'honkai_sr': {'checkin': True, 'black_list': []},
            'zzz': {'checkin': True, 'black_list': []}
        },
        'os': {
            'enable': False, 'cookie': '', 'lang': 'zh-cn',
            'genshin': {'checkin': False, 'black_list': []},
            'honkai3rd': {'checkin': False, 'black_list': []},
            'tears_of_themis': {'checkin': False, 'black_list': []},
            'honkai_sr': {'checkin': False, 'black_list': []},
            'zzz': {'checkin': False, 'black_list': []}
        }
    },
    'cloud_games': {
        "cn": {
            "enable": False,
            "genshin": {'enable': False, 'token': ""},
            "zzz": {'enable': False, 'token': ""}
        },
        "os": {
            "enable": False, 'lang': 'zh-cn',
            "genshin": {'enable': False, 'token': ""}
        }
    },

    'competition': {
        'enable': False,
        'genius_invokation': {'enable': False, 'account': [], 'checkin': False, 'weekly': False}
    }
}
config_raw = deepcopy(config)

path = os.path.dirname(os.path.realpath(__file__)) + "/config"
if os.getenv("AutoMihoyoBBS_config_path") is not None:
    path = os.getenv("AutoMihoyoBBS_config_path")
config_prefix = os.getenv("AutoMihoyoBBS_config_prefix")
if config_prefix is None:
    config_prefix = ""
# config_Path = f"{path}/{config_prefix}config.yaml"
config_Path = "src/config/config.yaml"


def copy_config():
    return config_raw


def config_v10_update(data: dict):
    global update_config_need
    update_config_need = True
    data['version'] = 11
    data['account']['mid'] = ""
    genius = data['competition']['genius_invokation']
    new_keys = ['enable', 'account', 'checkin', 'weekly']
    data['competition']['genius_invokation'] = dict(collections.OrderedDict(
        (key, genius.get(key, False) if key != 'account' else []) for key in new_keys))
    log.info("config 已升级到：11")
    return data


def config_v11_update(data: dict):
    global update_config_need
    update_config_need = True
    data['version'] = 13
    new_config = {}
    for key in data:
        if key == "account":
            new_config["push"] = ""
        if key == "cloud_games":
            new_config['cloud_games'] = deepcopy(config_raw['cloud_games'])
            continue
        new_config[key] = deepcopy(data[key])
    new_config['cloud_games']['cn']['enable'] = data['cloud_games']['genshin']['enable']
    new_config['cloud_games']['cn']['genshin']['enable'] = data['cloud_games']['genshin']['enable']
    new_config['cloud_games']['cn']['genshin']['token'] = data['cloud_games']['genshin']['token']
    log.info("config 已升级到：13")
    return new_config


def config_v12_update(data: dict):
    global update_config_need
    update_config_need = True
    data['version'] = 13
    data['cloud_games']['cn']['zzz'] = {'enable': False, 'token': ""}
    log.info("config 已升级到: 13")
    return data


def config_v13_update(data: dict):
    global update_config_need
    update_config_need = True
    new_config = deepcopy(data)

    # 确保版本号更新为14
    new_config['version'] = 14
    new_config['device']['fp'] = config['device'].get('fp', '')

    log.info("config 已升级到：14")
    return new_config


def load_config(p_path: str =None,cookie: str=None):
    global config
    # 使用默认配置作为基础
    data = deepcopy(config_raw)
    
    # 如果不是在GitHub Actions中运行，尝试从文件加载配置
    if not is_github_action and not os.getenv("COOKIE"):
        if not p_path:
            p_path = config_Path
        try:
            with open(p_path, "r", encoding='utf-8') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
            # 版本更新检查
            if data['version'] != config_raw['version']:
                if data['version'] == 10:
                    data = config_v10_update(data)
                if data['version'] == 11:
                    data = config_v11_update(data)
                if data['version'] == 12:
                    data = config_v12_update(data)
                if data['version'] == 13:
                    data = config_v13_update(data)
                if not is_github_action:
                    save_config(p_config=data)
            log.info("从配置文件加载配置完成")
        except (FileNotFoundError, OSError):
            log.info("配置文件不存在或无法读取，使用默认配置")
    
    # 从环境变量加载COOKIE（优先级高于文件配置）
    if os.getenv("COOKIE"):
        log.info("从环境变量加载COOKIE")
        if cookie:
            cookie = deepcopy(cookie)
            data["account"]["cookie"] = cookie
        else:
            data["account"]["cookie"] = os.getenv("COOKIE")
    
    # 去除cookie最末尾的空格
    data["account"]["cookie"] = str(data["account"]["cookie"]).rstrip(' ')
    
    # 检查设备ID是否为空，如果为空则使用cookie生成
    if not data["device"]["id"] and data["account"]["cookie"]:
        log.info("设备ID为空，使用cookie生成设备ID")
        data["device"]["id"] = tools.get_device_id(data["account"]["cookie"])
    
    config = data
    log.info("Config 加载完毕")
    return data


def save_config(p_path=None, p_config=None):
    global serverless
    if serverless or is_github_action:
        if is_github_action:
            log.info("GitHub Actions环境中运行，不保存配置文件")
        else:
            log.info("云函数执行，无法保存")
        return None
        
    if not p_path:
        p_path = config_Path
    if not p_config:
        p_config = config
    with open(p_path, "w+") as f:
        try:
            f.seek(0)
            f.truncate()
            f.write(yaml.dump(p_config, Dumper=yaml.Dumper, sort_keys=False))
            f.flush()
        except OSError:
            serverless = True
            log.info("Cookie 保存失败")
        else:
            log.info("Config 保存完毕")


def clear_stoken():
    global config
    if serverless or is_github_action:
        log.info("在受限环境中运行，配置仅在内存中修改")
    else:
        config["account"]["mid"] = ""
        config["account"]["stuid"] = ""
        config["account"]["stoken"] = "StokenError"
        log.info("Stoken 已删除")
        save_config()


def clear_cookie():
    global config
    if serverless or is_github_action:
        log.info("在受限环境中运行，配置仅在内存中修改")
    else:
        config["account"]["cookie"] = "CookieError"
        log.info(f"Cookie 已删除")
        save_config()


def disable_games(region: str = "cn"):
    global config
    if serverless or is_github_action:
        log.info("在受限环境中运行，配置仅在内存中修改")
    else:
        config['games'][region]['enable'] = False
        log.info(f"游戏签到（{region}）已关闭")
        save_config()


def clear_cookie_cloudgame_genshin():
    global config
    if serverless or is_github_action:
        log.info("在受限环境中运行，配置仅在内存中修改")
    else:
        config['cloud_games']['cn']['genshin']["enable"] = False
        config['cloud_games']['cn']['genshin']['token'] = ""
        log.info("国服云原神 Cookie 删除完毕")
        save_config()


def clear_cookie_cloudgame_genshin_os():
    global config
    if serverless or is_github_action:
        log.info("在受限环境中运行，配置仅在内存中修改")
    else:
        config['cloud_games']['os']['genshin']["enable"] = False
        config['cloud_games']['os']['genshin']['token'] = ""
        log.info("国际服云原神 Cookie 删除完毕")
        save_config()


def clear_cookie_cloudgame_zzz():
    global config
    if serverless or is_github_action:
        log.info("在受限环境中运行，配置仅在内存中修改")
    else:
        config['cloud_games']['cn']['zzz']["enable"] = False
        config['cloud_games']['cn']['zzz']['token'] = ""
        log.info("国服云绝区零 Cookie 删除完毕")
        save_config()


if __name__ == "__main__":
    # 初始化配置文件
    # try:
    #     account_cookie = config['account']['cookie']
    #     config = load_config()
    #     config['account']['cookie'] = account_cookie
    # except OSError:
    #     pass
    # save_config()
    # update_config()
    pass
