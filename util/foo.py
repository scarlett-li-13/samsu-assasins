from custom_errors import RegistrationError

def foo():
    raise RegistrationError("message")

try:
    foo()
except RegistrationError as e:
    print e.message
