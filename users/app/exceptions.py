from fastapi import HTTPException


EmailAlreadyTaken = HTTPException(
    status_code=400,
    detail="A user with this email already exists."
)

InvalidEmail = HTTPException(
    status_code=404,
    detail="No user with this email exists."
)

InvalidUserId = HTTPException(
    status_code=404,
    detail="No user with this id exists."
)

EmptyUpdatedData = HTTPException(
    status_code=422,
    detail='At least one field must be changed.'
)

CredentialsException = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )