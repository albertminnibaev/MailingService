from fastapi import status, HTTPException


ObjectDoesNotExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Объект не найден"
)
