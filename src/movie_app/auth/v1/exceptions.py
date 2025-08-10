class UserNotFoundError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class UserInactiveError(Exception):
    pass

class RoleNotAssignedError(Exception):
    pass

class InvalidTokenError(Exception):
    pass
