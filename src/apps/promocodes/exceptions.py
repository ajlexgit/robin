class PromoCodeError(Exception):
    """ Базовый класс исключений """
    pass


class PromoCodeValidationError(PromoCodeError):
    pass


class PromoCodeLimitReachedError(PromoCodeError):
    pass


class PromoCodeExpiredError(PromoCodeError):
    pass
