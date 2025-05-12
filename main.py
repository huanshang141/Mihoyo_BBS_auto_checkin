import os
import time
import random
import json
import sys

import src.checkin.gamecheckin as gamecheckin
from src import config
from src.utils.error import *
from src.utils.loghelper import log
import src.notify.wechat as WeChat

def main():
    # 加载配置
    config.load_config()
    
    if not config.config["enable"]:
        log.warning("Config 未启用！")
        return 1, "Config 未启用！"
    
    # 检测账号信息是否完整
    if not config.config["account"]["cookie"]:
        log.error("账号信息不完整，请检查环境变量配置")
        return 1, "账号信息不完整，请检查环境变量配置"
    
    return_data = "\n"
    
    # 执行游戏签到
    if config.config['games']['cn']["enable"]:
        return_data += gamecheckin.run_task()
    
    return 0, return_data

if __name__ == "__main__":
    # try:
        status_code, message = main()
        print(message)
        WeChat.send_wechat_notification(message)
        
        # 如果在GitHub Actions环境中，设置输出变量
        if os.getenv('GITHUB_ACTIONS') == 'true':
            with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                f.write(f"status={status_code}\n")
                f.write(f"message={message}\n")
        
        sys.exit(status_code)
    # except CookieError:
    #     log.error("账号 Cookie 有问题！")
    #     print("账号 Cookie 出错！")
    #     sys.exit(1)
    # except StokenError:
    #     log.error("账号 Stoken 有问题！")
    #     print("账号 Stoken 出错！")
    #     sys.exit(1)
    # except Exception as e:
    #     log.error(f"发生未知错误: {str(e)}")
    #     print(f"发生未知错误: {str(e)}")
    #     sys.exit(1)