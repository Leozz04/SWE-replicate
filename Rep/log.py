import logging
import pathlib

class Log:
    def __init__(self, file_name, logger_name=None, level=logging.INFO):
        self.file_name = file_name
        self.level = level
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(self.level)
        self.init_log()

    def init_log(self):
        handler = logging.FileHandler(self.file_name)
        handler.setLevel(self.level)
        formatter = logging.Formatter(
            "[%(asctime)s - %(filename)s - %(name)s - %(levelname)s]: %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.level)
        stream_handler.setFormatter(formatter)
        # 添加处理器
        self.logger.addHandler(stream_handler)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


log_path = pathlib.Path(__file__).parent.joinpath("Info.log")
log = Log(log_path)


if __name__ == "__main__":
    log.info("test log")
