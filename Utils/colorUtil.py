import colorsys as cs

rangeValue = 10.0

def hexToRgb(hexCode):
    rgbCodeList = [int(hexCode[i:i+2], 16) for i in range(0, 6, 2)]
    rgbCode =(rgbCodeList[0], rgbCodeList[1], rgbCodeList[2])

    return rgbCode

def rgbToHex(rgbCode):
    hexCode = "{:02X}{:02X}{:02X}".format(*rgbCode)

    return hexCode

def rgbToHsv(rgbCode):
    hsvCode = cs.rgb_to_hsv(rgbCode[0], rgbCode[1], rgbCode[2])

    return hsvCode

def hsvToRgb(hsvCode):
    rgbCodeList = []
    rgbCode = cs.hsv_to_rgb(hsvCode[0], hsvCode[1], hsvCode[2])
    for i in range(3):
        rgbCodeList.append(int(rgbCode[i]))

    return rgbCodeList

def sameColor(searchColor, colorList):
    sameColorList = []
    if (searchColor in colorList):
        for cl in colorList:
            if (searchColor == cl):
                sameColorList.append(cl)

    return sameColorList

def searchSimilarValue(hexCode):
    rgbCode = hexToRgb(hexCode)
    hsvCode = rgbToHsv(rgbCode)
    vRange = hsvCode[2]

    downVRange = vRange - rangeValue
    if downVRange < 20:
        downVRange = 20
    downHsvCode = [hsvCode[0], hsvCode[1], downVRange]
    downRgbCode = hsvToRgb(downHsvCode)
    downVCode = rgbToHex(downRgbCode)

    upVRange = vRange + rangeValue
    if upVRange > 100:
        upVRange = 100
    upHsvCode = [hsvCode[0], hsvCode[1], upVRange]
    upRgbCode = hsvToRgb(upHsvCode)
    upVCode = rgbToHex(upRgbCode)

    return (downVCode, upVCode)

def searchSimilarSaturation(hexCode):
    rgbCode = hexToRgb(hexCode)
    hsvCode = rgbToHsv(rgbCode)
    sRange = hsvCode[2]

    downSRange = sRange - rangeValue
    if downSRange < 20:
        downSRange = 20
    downHsvCode = [hsvCode[0], downSRange, hsvCode[2]]
    downRgbCode = hsvToRgb(downHsvCode)
    downSCode = rgbToHex(downRgbCode)

    upSRange = sRange + rangeValue
    if upSRange > 100:
        upSRange = 100
    upHsvCode = [hsvCode[0], upSRange, hsvCode[2]]
    upRgbCode = hsvToRgb(upHsvCode)
    upSCode = rgbToHex(upRgbCode)

    return (downSCode, upSCode)