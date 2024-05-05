from typing import Optional
from pydantic import BaseModel, Field

# レスポンス バリデーション
class ErrorInfo(BaseModel):
    errorId: Optional[dict]
    errorMessage: Optional[list[str]]

class LipColorInfo(BaseModel):
    ripId: int
    colorCode: str
    productName: str
    colorNumber: str
    colorName: str

class LipColorInfoList(BaseModel):
    lipColorInfoList: list[LipColorInfo]

class BaseLipInfo(BaseModel):
    ripId: int
    brandName: str
    productName: str
    colorNumber: str
    colorName: str
    colorCode: str
    amount: int
    limitedProductFlag: str
    salesStopFlag: str
    cosmeURL: str

class SimilarLipInfo(BaseModel):
    similarPoint: str
    lipInfo: BaseLipInfo

class SearchInfo(BaseModel):
    brandName: str
    colorCode: str = Field(min_length = 3, max_length = 6, pattern = r"[A-Fa-f0-9]")

class SimilarLipInfoList(BaseModel):
    lipInfoList: list[SimilarLipInfo]