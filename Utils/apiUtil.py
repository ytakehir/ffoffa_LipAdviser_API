from ..Utils import responseBean
from ..Utils import settings as set

class ApiService:
  def createImage(self, result, imageResult):
    imageList = []
    imagePath = ''

    if imageResult:
        for imgRe in imageResult:
            imagePath = f"{set.IMAGE_PATH}{imgRe.get('BRAND_NAME')}/product/{imgRe.get('PATH')}"
            imageList.append(responseBean.BaseImage(
                alt = result.get('BRAND_NAME'),
                path = imagePath
            ))
    else:
        imageList.append(responseBean.BaseImage(
                alt = result.get('BRAND_NAME'),
                path = imagePath
        ))

    return imageList

  def createTag(self, tagResult):
    tagList = []
    for tagRe in tagResult:
          tagList.append(responseBean.BaseTag(
            tagId = tagRe.get('ID'),
            tagName = tagRe.get('TAG_NAME'),
            tagGenre = tagRe.get('TAG_GENRE'),
          ))

    return tagList
