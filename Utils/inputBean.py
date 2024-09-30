from pydantic import BaseModel, Field

# リクエスト バリデーション
class AuthInput(BaseModel):
  accessId: str
  accessKey: str
class ColorCodeInput(BaseModel):
  colorCode: str = Field(min_length = 3, max_length = 6, pattern = r"[A-Fa-f0-9]")

class BrandNameInput(BaseModel):
  brandName: str

class LipIdInput(BaseModel):
  lipId: int

class ProductIdInput(BaseModel):
  productId: str = Field(min_length = 2, pattern = r"p[0-9]+")

class ImagePathInput(BaseModel):
  imagePath: str