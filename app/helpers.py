from datetime import datetime


class LevelsStr:
    warn = 'WARN'.ljust(5, ' ')
    error = 'ERROR'.ljust(5, ' ')
    info = 'INFO'.ljust(5, ' ')
    debug = 'DEBUG'.ljust(5, ' ')


def logError(*args):
    print(datetime.now(), LevelsStr.info, *args)


def logInfo(*args):
    print(datetime.now(), LevelsStr.info, *args)


def logWarn(*args):
    print(datetime.now(), LevelsStr.info, *args)


def logDebug(*args):
    print(datetime.now(), LevelsStr.info, *args)
