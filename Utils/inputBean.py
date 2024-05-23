from pydantic import BaseModel, Field

# リクエスト バリデーション
class ColorCodeSearchInput(BaseModel):
    colorCode: str = Field(min_length = 3, max_length = 6, pattern = r"[A-Fa-f0-9]")

class BrandNameSearchInput(BaseModel):
    brandName: str

class LipIdSearchInput(BaseModel):
    lipId: int