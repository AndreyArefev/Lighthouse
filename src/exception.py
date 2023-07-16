from fastapi import HTTPException, status

ExCategoryNotExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Категория отсутствует"
)

ExUsernameAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь с таким ником уже зарегестрирован"
)

ExEmailAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь с таким email уже зарегестрирован"
)

ExInactiveUser = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Доступ запрещен")


ExNotAdmin = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Недостаточно прав. Доступ разрешен только адмиристраторам")


ExCredentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


ExIncorrectLoginOrPassword = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Логин или пароль неверны")

ExTokenExpired = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истек")

ExIncorrectTokenVerification = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Для верификации аккаунта используйте ссылку в входящем e-mail")
