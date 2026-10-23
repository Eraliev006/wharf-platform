class InvalidToken(Exception):
    pass


class TokenExpired(InvalidToken):
    pass


class InvalidTokenType(InvalidToken):
    pass
