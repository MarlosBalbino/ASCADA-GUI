from datetime import datetime

level_str_sz = 6


class LevelsStr:
    warn = 'WARN:'.rjust(level_str_sz, ' ')
    error = 'ERROR:'.rjust(level_str_sz, ' ')
    info = 'INFO:'.rjust(level_str_sz, ' ')
    debug = 'DEBUG:'.rjust(level_str_sz, ' ')


def getTimeStamp(ms_divider=1e5):
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%m:%S.') + str(round(now.microsecond/ms_divider))


def logError(*args):
    print(getTimeStamp(), LevelsStr.error, *args)


def logInfo(*args):
    print(getTimeStamp(), LevelsStr.info, *args)


def logWarn(*args):
    print(getTimeStamp(), LevelsStr.warn, *args)


def logDebug(*args):
    print(getTimeStamp(), LevelsStr.debug, *args)
