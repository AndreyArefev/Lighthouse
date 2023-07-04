from fastapi import HTTPException, status

ExceptionCategoryNotExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Категория отсутствует"
)

ExceptionUsernameAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь с таким ником уже зарегестрирован"
)

ExceptionEmailAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь с таким email уже зарегестрирован"
)

ExceptionCredentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )