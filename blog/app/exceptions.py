from fastapi import HTTPException

PostNotFound = HTTPException(status_code=404, detail="Post not found.")

PostOrCommentNotFound = HTTPException(
    status_code=404, detail="Post or comment not found."
)


EmptyUpdateData = HTTPException(
    status_code=422, detail="At least one field must be changed."
)
