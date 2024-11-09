class AuthUserError(Exception):
    pass

class AuthUsernameError(AuthUserError):
    pass

class AuthPasswordError(AuthUserError):
    pass
