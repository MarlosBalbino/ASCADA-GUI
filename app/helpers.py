from datetime import datetime

level_str_sz = 6


class LevelsStr:
    warn = 'WARN:'.rjust(level_str_sz, ' ')
    error = 'ERROR:'.rjust(level_str_sz, ' ')
    info = 'INFO:'.rjust(level_str_sz, ' ')
    debug = 'DEBUG:'.rjust(level_str_sz, ' ')


def logError(*args):
    print(datetime.now(), LevelsStr.info, *args)


def logInfo(*args):
    print(datetime.now(), LevelsStr.info, *args)


def logWarn(*args):
    print(datetime.now(), LevelsStr.info, *args)


def logDebug(*args):
    print(datetime.now(), LevelsStr.info, *args)
