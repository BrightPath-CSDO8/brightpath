class EmailAlreadyRegisteredError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class NotFoundError(Exception):
    pass


class DuplicateError(Exception):
    pass
