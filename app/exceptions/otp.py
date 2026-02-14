class OtpNotFoundException(Exception):
    def __init__(self, verification_id: int):
        super().__init__(f'Verification with id {verification_id} not found')

class OtpResendTooSoonException(Exception):
    def __init__(self, retry_after: int):
        super().__init__(f'Otp resend is too soon. Try again in {retry_after} seconds.')

class OtpCodeIsNotValidException(Exception):
    def __init__(self, otp_code: str):
        super().__init__(f'Otp code {otp_code} is not valid')