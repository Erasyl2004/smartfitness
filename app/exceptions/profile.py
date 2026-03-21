
class UserProfileAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__(f'User profile already exists')