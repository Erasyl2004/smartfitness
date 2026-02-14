class UserAlreadyExistsException(Exception):
    def __init__(self, email: str):
        super().__init__(f'User with this email {email} already exists')