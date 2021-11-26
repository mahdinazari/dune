"""
Create A New Exception Example:
```
    class BarException(AppException):
        message = "This Is A Sample Error text"
        status_code = 423
        code = 1025
```

Usage of created exception in Views Example:
```
    from application import exc
    @app.route('/foo')
    def get_foo():
        raise exc.BarException
```
"""

class ApplicationException(Exception):
    status_code = 400
    message =  "Empty"
    payload = {}

    def __init__(self):
        Exception.__init__(self)

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class ForemDataNotValid(ApplicationException):
    status_code = 701
    message = '400 Form Data Not Valid'


class EmailNotValid(ApplicationException):
    status_code = 702
    message = '400 Email Not Valid'


class PasswordLengthNotValid(ApplicationException):
    status_code = 703
    message = '400 Password Length Not Valid'


class ValidationException(ApplicationException):
    status_code = 704
    message = '400 Validation Exception'


class DuplicateMemberFound(ApplicationException):
    status_code = 705
    message = "400 Duplicate Member Found"


class RegisterFailed(ApplicationException):
    status_code = 706
    message = "400 Register Failed"


class EmailNotInForm(ApplicationException):
    status_code = 706
    message = "400 Email Not In Form"


class PasswordNotInForm(ApplicationException):
    status_code = 706
    message = "400 Password Not In Form"


class MemberNotFound(ApplicationException):
    status_code = 706
    message = "400 Member Not Found"



class EmptyList(ApplicationException):
    status_code = 707
    message = "404 Empty List"

