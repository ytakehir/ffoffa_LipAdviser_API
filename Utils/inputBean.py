from pydantic import BaseModel, Field

# リクエスト バリデーション
class AuthInput(BaseModel):
    accessId: str
    accessKey: str
class ColorCodeSearchInput(BaseModel):
    colorCode: str = Field(min_length = 3, max_length = 6, pattern = r"[A-Fa-f0-9]")

class BrandNameSearchInput(BaseModel):
    brandName: str

class LipIdSearchInput(BaseModel):
    lipId: int

class ImageSearchInput(BaseModel):
    lipId: int

class LipHistoryInput(BaseModel):
    lipId: int

class ColorCodeHistoryInput(BaseModel):
    colorCode: str = Field(min_length = 3, max_length = 6, pattern = r"[A-Fa-f0-9]")