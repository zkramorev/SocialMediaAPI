from fastapi import HTTPException, status


class AppException(HTTPException):
    status_code = 500
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsException(AppException):
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"
        
class IncorrectEmailOrPasswordException(AppException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверная почта или пароль"
        
class TokenExpiredException(AppException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Срок действия токена истек"
        
class TokenAbsentException(AppException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"
        
class IncorrectTokenFormatException(AppException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный формат токена"
        
class UserIsNotPresentException(AppException):
    status_code=status.HTTP_401_UNAUTHORIZED

class CannotSendRequestToYourself(AppException):
    status_code=status.HTTP_405_METHOD_NOT_ALLOWED
    detail="Нельзя отправить заявку самому себе"

class UserNotFound(AppException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Пользователь не найден"


class CannotAddDataToDatabase(AppException):
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    detail="Не удалось добавить запись"

