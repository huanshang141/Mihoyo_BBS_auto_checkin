import os
import logging
from logging.handlers import RotatingFileHandler

# 创建logs目录
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "logs")
os.makedirs(logs_dir, exist_ok=True)

# 日志文件路径
log_file = os.path.join(logs_dir, "auto_checkin.log")

# 配置日志
if False:
    os.path.exists(file_path)
    # 原有配置保持不变
    import logging.config
    logging.config.fileConfig(file_path, encoding='utf-8')
    log = logging.getLogger("AutoMihoyoBBS")
else:
    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d (%(funcName)s) - %(message)s')
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # 创建文件处理器 (限制文件大小为5MB，保留3个备份)
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # 创建logger
    logger = logging.getLogger("AutoMihoyoBBS")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    log = logger