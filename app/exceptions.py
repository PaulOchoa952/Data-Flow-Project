from fastapi import HTTPException, status

class APIException(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)

class RedisCacheException(APIException):
    def __init__(self, detail: str = "Redis cache error"): 
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) 