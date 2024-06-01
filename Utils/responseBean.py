from typing import Optional
from pydantic import BaseModel, Field

# レスポンス バリデーション
class ErrorInfo(BaseModel):
    errorId: Optional[dict]
    errorMessage: Optional[list[str]]

class LipColorInfo(BaseModel):
    lipId: int
    colorCode: str
    productName: str
    colorNumber: str
    colorName: str

class LipColorInfoList(BaseModel):
    lipColorInfoList: list[LipColorInfo]

class BaseLipInfo(BaseModel):
    lipId: int
    brandName: str
    productName: str
    colorNumber: str
    colorName: str
    colorCode: str
    amount: int
    limitedProductFlag: str
    salesStopFlag: str
    officialURL: str
    amazonURL: str
    qooTenURL: str

class BrandNameInfo(BaseModel):
    brandName: str

class BrandNameInfoList(BaseModel):
    brandNameList: list[BrandNameInfo]

class SimilarLipInfo(BaseModel):
    similarPoint: float
    lipInfo: BaseLipInfo

class SearchInfo(BaseModel):
    brandName: str
    colorCode: str = Field(min_length = 3, max_length = 6, pattern = r"[A-Fa-f0-9]")

class SimilarLipInfoList(BaseModel):
    lipInfoList: list[SimilarLipInfo]