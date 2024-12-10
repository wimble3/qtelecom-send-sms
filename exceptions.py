class QTException(Exception):
    pass


class QTLengthTooLongException(QTException):
    pass


class QTEmptySMSException(QTException):
    pass


class QTError(QTException):
    pass
