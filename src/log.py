import logging
import logging.handlers
import os
from pathlib import Path

class LogMgr:
    """
    日志管理器类
    提供统一的日志配置和管理功能
    """
    
    def __init__(self):
        """
        初始化日志管理器
        """
        self._loggers = {}  # 缓存已创建的logger
        self._log_dir = Path(__file__).parent.parent / "logs"  # 日志目录
        self._log_dir.mkdir(exist_ok=True)  # 确保日志目录存在
        
    def get(self, level=logging.INFO, logger_name="LifeTool"):
        """
        获取配置好的logger实例
        
        @param level: 日志等级，默认为INFO
        @param logger_name: logger名称，默认为"LifeTool"
        @return: 配置好的logger实例
        """
        # 如果logger已存在，直接返回
        if logger_name in self._loggers:
            return self._loggers[logger_name]
        
        # 创建新的logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        
        # 清除已有的handlers，避免重复添加
        logger.handlers.clear()
        
        # 创建格式化器，包含详细的运行时信息
        formatter = logging.Formatter(
            fmt='[%(asctime)s][%(levelname)s][%(process)d][%(thread)d][%(name)s][%(filename)s][%(funcName)s][%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 1. 创建每天滚动的文件handler
        file_handler = self._create_rotating_file_handler(logger_name, formatter)
        logger.addHandler(file_handler)
        
        # 2. 创建控制台handler
        console_handler = self._create_console_handler(formatter)
        logger.addHandler(console_handler)
        
        # 缓存logger
        self._loggers[logger_name] = logger
        
        return logger
    
    def _create_rotating_file_handler(self, logger_name, formatter):
        """
        创建每天滚动的文件handler
        
        @param logger_name: logger名称
        @param formatter: 日志格式化器
        @return: 配置好的文件handler
        """
        # 日志文件路径
        log_file = self._log_dir / f"{logger_name}.log"
        
        # 创建TimedRotatingFileHandler，每天滚动
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=str(log_file),
            when='D',         # 每天滚动
            interval=1,       # 间隔1天
            backupCount=5,    # 保留5个备份文件
            encoding='utf-8', # 使用UTF-8编码
            delay=False,      # 立即创建文件
            utc=False         # 使用本地时间
        )
        
        # 设置日志文件的后缀格式
        file_handler.suffix = "%Y-%m-%d"
        
        # 设置格式化器
        file_handler.setFormatter(formatter)
        
        return file_handler
    
    def _create_console_handler(self, formatter):
        """
        创建控制台handler
        
        @param formatter: 日志格式化器
        @return: 配置好的控制台handler
        """
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        return console_handler
    

    
    def set_log_level(self, logger_name, level):
        """
        设置指定logger的日志等级
        
        @param logger_name: logger名称
        @param level: 新的日志等级
        """
        if logger_name in self._loggers:
            self._loggers[logger_name].setLevel(level)
    
    def get_log_dir(self):
        """
        获取日志目录路径
        
        @return: 日志目录的Path对象
        """
        return self._log_dir

# 创建全局日志管理器实例
log_mgr = LogMgr()

# 便捷函数
def get_logger(level=logging.INFO, logger_name="LifeTool"):
    """
    获取logger的便捷函数
    
    @param level: 日志等级
    @param logger_name: logger名称
    @return: 配置好的logger实例
    """
    return log_mgr.get(level, logger_name)

# 使用示例
if __name__ == "__main__":
    # 创建日志管理器
    mgr = LogMgr()
    
    # 获取logger
    logger = mgr.get(logging.DEBUG, "TestLogger")
    
    # 测试不同级别的日志
    logger.debug("这是一条调试信息")
    logger.info("这是一条信息")
    logger.warning("这是一条警告")
    logger.error("这是一条错误信息")
    logger.critical("这是一条严重错误信息")
    
    print(f"日志文件保存在: {mgr.get_log_dir()}")