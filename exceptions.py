class ValidationException(BaseException):

    def __init__(self, errors):
        self.errors = errors


class CrawlException(BaseException):

    def __init__(self, cause):
        self.cause = cause


class EmailException(BaseException):

    def __init__(self, cause):
        self.cause = cause
