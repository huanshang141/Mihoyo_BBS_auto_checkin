import os
import sys
import time
from typing import List, Tuple

from main import main
from src.utils.loghelper import log
import src.notify.wechat as WeChat

def get_cookies_from_env() -> Tuple[str, ...]:
    """从环境变量获取 cookie 字符串并转换为元组"""
    cookies_str = os.environ.get('COOKIE', '')
    if not cookies_str:
        log.error("未找到环境变量 COOKIE，请检查配置")
        sys.exit(1)
    
    # 以逗号分割 cookie 字符串，并去除每个 cookie 两端的空白
    cookies = tuple(cookie.strip() for cookie in cookies_str.split(',') if cookie.strip())
    
    if not cookies:
        log.error("解析后的 cookie 列表为空，请检查环境变量格式")
        sys.exit(1)
        
    log.info(f"成功获取到 {len(cookies)} 个账号的 cookie")
    return cookies

def main_multi() -> None:
    """处理多个账号的签到"""
    cookies = get_cookies_from_env()
    all_results = []
    
    for i, cookie in enumerate(cookies, 1):
        log.info(f"开始处理第 {i} 个账号")
        try:
            status_code, message = main(cookie=cookie)
            result = f"账号 {i} 结果: {'成功' if status_code == 0 else '失败'}\n{message}"
            all_results.append(result)
            log.info(f"第 {i} 个账号处理完成")
        except Exception as e:
            error_msg = f"账号 {i} 处理时发生错误: {str(e)}"
            log.error(error_msg)
            all_results.append(error_msg)
        
        # 账号之间添加随机延迟，避免请求过于频繁
        if i < len(cookies):
            delay = random.randint(5, 10)
            log.info(f"等待 {delay} 秒后处理下一个账号")
            time.sleep(delay)
    
    # 合并所有结果
    final_result = "\n\n".join(all_results)
    print(final_result)
    
    # 发送微信通知
    WeChat.send_wechat_notification(final_result)
    
    # 如果在 GitHub Actions 环境中，设置输出变量
    if os.getenv('GITHUB_ACTIONS') == 'true':
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"status=0\n")  # 总是返回成功状态码
            f.write(f"message=多账号处理完成\n")

if __name__ == "__main__":
    import random  # 导入随机模块用于延迟
    main_multi()
