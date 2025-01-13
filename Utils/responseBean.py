from typing import Union, Optional
from pydantic import BaseModel, Field

# レスポンス バリデーション
class Error(BaseModel):
  errorId: Optional[dict]
  errorMessage: Optional[list[str]]

class ExecResult(Error):
  successFlag: str

class ColorCode(BaseModel):
  colorCode: str = Field(min_length = 3, max_length = 6, pattern = r"[A-Fa-f0-9]+")

class LipColor(BaseModel):
  lipId: int
  productId: str
  colorCode: str
  productName: str
  colorNumber: str
  colorName: str

class LipColorList(BaseModel):
  lipColorList: list[LipColor]

class BaseLip(BaseModel):
  lipId: int
  productId: str
  brandName: str
  productName: str
  colorNumber: str
  colorName: str
  colorCode: str
  amount: int
  limitedProductFlag: str
  salesStopFlag: str
  prFlag: str
  officialURL: str
  amazonURL: str
  qooTenURL: str

class BrandName(BaseModel):
  brandName: str

class BrandNameList(BaseModel):
  brandNameList: list[BrandName]

class SimilarLip(BaseLip):
  similarPoint: float

class Search(BaseModel):
  brandName: str
  colorCode: str = Field(min_length = 3, max_length = 6, pattern = r"[A-Fa-f0-9]+")

class SimilarLipList(BaseModel):
  lipList: list[SimilarLip]

class BaseTag(BaseModel):
  tagId: int
  tagName: str
  tagGenre: int

class TagList(BaseModel):
  tagList: list[BaseTag]

class BaseImage(BaseModel):
  alt: str
  path: str

class Product(BaseModel):
  imageList: list[BaseImage]
  lip: Union[SimilarLip, BaseLip]
  tagList: list[BaseTag]

class ProductList(BaseModel):
  productList: list[Product]

class ImageList(BaseModel):
  imageList: list[BaseImage]

class ProductId(BaseModel):
  productId: str


class ProductIdList(BaseModel):
  productIdList: list[ProductId]

class LipRanking(BaseModel):
  lipId: int
  count: int

class LipRankingList(BaseModel):
  lipRankingList: list[LipRanking]

class colorAI(BaseModel):
  colorCode: str
  base64: str