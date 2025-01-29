from fastapi import status, HTTPException


ObjectDoesNotExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Объект не найден"
)

UserAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует"
)

IncorrectEmailOrPassword = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверная почта или пароль"
)

TokenExpired = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен истек'
)

TokenNoFound = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен не найден'
)

NoJwtException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен не валидный!'
)

NoUserIdException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Не найден ID пользователя'
)

ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Недостаточно прав!'
)

IntegrityException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Возникла ошибка при выполнении запроса, '
           'пожалуйста обратитесь к администратору'
)

ProfileUserNotExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Профель пользователя не найден"
)
