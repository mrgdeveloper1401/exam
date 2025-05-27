from django.core.validators import RegexValidator


class PhoneNumberValidator(RegexValidator):
    regex = r'^\d{9,15}'
    message = "you must valid phone"
    code = 'invalid_phone'
