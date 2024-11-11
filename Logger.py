from enum import Enum

class STATUS(Enum):
    INFO = 1
    DEBUG = 2
    ERROR = 3

class LogProcessor:
    def __init__(self, logProcessor) -> None:
        self.nextLogProcessor = logProcessor
    
    def log(self, LOGSTATUS: STATUS, message:str):
        if self.nextLogProcessor:
            self.nextLogProcessor.log(LOGSTATUS, message)


class InfoLogProcessor(LogProcessor):
    def __init__(self, logProcessor: LogProcessor) -> None:
        super().__init__(logProcessor)
    
    def log(self, LOGSTATUS: STATUS, message: str):
        if LOGSTATUS == STATUS.INFO:
            print(f"INFO LOGGER: {message}")
        else:
            super().log(LOGSTATUS, message)


class DebugLogProcessor(LogProcessor):
    def __init__(self, logProcessor: LogProcessor) -> None:
        super().__init__(logProcessor)
    
    def log(self, LOGSTATUS: STATUS, message: str):
        if LOGSTATUS == STATUS.DEBUG:
            print(f"DEBUG LOGGER: {message}")
        else:
            super().log(LOGSTATUS, message)

class ErrorLogProcessor(LogProcessor):
    def __init__(self, logProcessor: LogProcessor) -> None:
        super().__init__(logProcessor)
    
    def log(self, LOGSTATUS: STATUS, message: str):
        if LOGSTATUS == STATUS.ERROR:
            print(f"ERROR LOGGER: {message}")
        else:
            super().log(LOGSTATUS, message)

class Implementor:
    @staticmethod
    def run():
        logger = InfoLogProcessor(DebugLogProcessor(ErrorLogProcessor(None)))
        logger.log(STATUS.ERROR, "There is some error in the code")
        logger.log(STATUS.DEBUG, "Running debugger")
        logger.log(STATUS.INFO, "Here is some info about the process")

if __name__=="__main__":
    Implementor.run()