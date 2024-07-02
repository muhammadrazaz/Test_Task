from fastapi import HTTPException, status, UploadFile
def validate_image(file: UploadFile):
    valid_extensions = {"image/jpeg", "image/png"}
    content_type = file.content_type
    if content_type not in valid_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PNG and JPG are allowed.",
        )