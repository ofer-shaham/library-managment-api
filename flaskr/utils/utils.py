from datetime import datetime


def convertDateStrToDateObj(engine, dateObject):
    """sqlite does not support date type, so we need to convert date string to date object"""
    if engine.name == 'sqlite':
        if isinstance(dateObject, str):
            return datetime.strptime(
                dateObject, '%Y-%m-%d').date()

    return dateObject


def convertTimeToEpocSeconds(str, format):
    epoch = int(datetime.strptime(
        str, format).timestamp())

    return epoch
