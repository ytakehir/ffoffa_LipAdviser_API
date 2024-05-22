from cmath import sqrt
import math
import colorsys as cs
from flask import current_app
import sys
sys.path.append('C:\\Users\\takeg\\work\\ffoffa_LipAdviser_API\\')
# sys.path.append('/home/c1343520/program/lipAdviser/')
from Utils import settings as set

class ConvertColor:
    def hexToRgb(self, hexCode):
        rgbCodeList = [int(hexCode[i:i+2], 16) for i in range(0, 6, 2)]
        rgbCode =(rgbCodeList[0], rgbCodeList[1], rgbCodeList[2])

        return rgbCode

    def hexToRgbTuple(self, hexCode):
        rgbCodeList = [int(hexCode[i:i+2], 16) for i in range(0, 6, 2)]
        (r, g, b) =(rgbCodeList[0], rgbCodeList[1], rgbCodeList[2])

        return (r, g, b)

    def rgbToHex(self, rgbCode):
        hexCode = "{:02X}{:02X}{:02X}".format(*rgbCode)

        return hexCode

    def rgbToHsv(self, rgbCode):
        (r, g, b) = (rgbCode[0] / 255, rgbCode[1] / 255, rgbCode[2] / 255)
        (h, s, v) = cs.rgb_to_hsv(r, g, b)
        hsvCode = (int(h * 360), int(s * 100), int(v * 100))

        return hsvCode

    def hsvToRgb(self, hsvCode):
        (h, s, v) = (hsvCode[0] / 360, hsvCode[1] / 100, hsvCode[2] / 100)
        (r, g, b) = cs.hsv_to_rgb(h, s, v)
        rgbCode = (int(r * 255), int(g * 255), int(b * 255))

        return rgbCode

    def hexToHsv(self, hexCode):
        rgbCode = self.hexToRgb(hexCode)
        hsvCode = self.rgbToHsv(rgbCode)

        return hsvCode

    def hsvToHex(self, hsvCode):
        rgbCode = self.hsvToRgb(hsvCode)
        hexCode = self.rgbToHex(rgbCode)

        return hexCode

    def rgbToSrgb(self, r, g, b):
        br = r / 255
        bg = g / 255
        bb = b / 255

        sr = ((br + 0.055) / 1.055) ** 2.4 if br > 0.04045 else br / 12.92
        sg = ((bg + 0.055) / 1.055) ** 2.4 if bg > 0.04045 else bg / 12.92
        sb = ((bb + 0.055) / 1.055) ** 2.4 if bb > 0.04045 else bb / 12.92

        return (sr, sg, sb)

    def srgbToXyz(self, sr, sg, sb):
        # 白色点はD65
        x = (sr * 0.4124564) + (sg * 0.3575761) + (sb * 0.1804375)
        y = (sr * 0.2126729) + (sg * 0.7151522) + (sb * 0.072175)
        z = (sr * 0.0193339) + (sg * 0.119192) + (sb * 0.9503041)

        return (x * 100, y * 100, z * 100)

    def xyzToLab(self, x, y, z):
        LAB_FT = math.pow(6 / 29, 3)
        XN = 95.047
        YN = 100
        ZN = 108.883

        tx = x / XN
        ty = y / YN
        tz = z / ZN

        fx = tx ** (1 / 3) if (tx > LAB_FT) else (7.787 * tx) + (16 / 116)
        fy = ty ** (1 / 3) if (ty > LAB_FT) else (7.787 * ty) + (16 / 116)
        fz = tz ** (1 / 3) if (tz > LAB_FT) else (7.787 * tz) + (16 / 116)

        l = (116 * fy) - 16
        a = 500 * (fx - fy)
        b = 200 * (fy - fz)

        return (l, a, b)

    def rgbToLab(self, r, g, b):
        (lr, lg, lb) = self.rgbToSrgb(r, g, b)
        (x, y, z) = self.srgbToXyz(lr, lg, lb)
        (l, a, b) = self.xyzToLab(x, y, z)

        return (l, a, b)

    def hexToLab(self, hexCode):
        (r, g, b) = self.hexToRgbTuple(hexCode)
        (l, a, lb) = self.rgbToLab(r, g, b)

        return (l, a, lb)

class ColorService:
    def sameColor(self, searchColor, colorList):
        sameColorList = []
        if (searchColor in colorList):
            for cl in colorList:
                if (searchColor == cl):
                    sameColorList.append(cl)

        return sameColorList

    def downValue(self, value):
        downValue = value - set.SEARCH_RANGE_VALUE
        if downValue < 20:
            downValue = 20

        return downValue

    def upValue(self, value):
        upValue = value + set.SEARCH_RANGE_VALUE
        if upValue > 100:
            upValue = 100

        return upValue

    def searchSimilarSaturation(self, hexCode):
        cc = ConvertColor()

        hsvCode = cc.hexToHsv(hexCode)

        downHsvCode = (hsvCode[0], self.downValue(hsvCode[1]), hsvCode[2])
        downSCode = cc.hsvToHex(downHsvCode)

        upHsvCode = (hsvCode[0], self.upValue(hsvCode[1]), hsvCode[2])
        upSCode = cc.hsvToHex(upHsvCode)

        return (downSCode, upSCode)

    def searchSimilarValue(self, hexCode):
        cc = ConvertColor()

        hsvCode = cc.hexToHsv(hexCode)

        downHsvCode = (hsvCode[0], hsvCode[1], self.downValue(hsvCode[2]))
        downVCode = cc.hsvToHex(downHsvCode)

        upHsvCode = (hsvCode[0], hsvCode[1], self.upValue(hsvCode[2]))
        upVCode = cc.hsvToHex(upHsvCode)

        return (downVCode, upVCode)

    def colorDistance(self, baseHexCode, checkHexCode):
        cc = ConvertColor()
        (br, bg, bb) = cc.hexToRgbTuple(baseHexCode)
        (cr, cg, cb) = cc.hexToRgbTuple(checkHexCode)

        r = br - cr
        g = bg - cg
        b = bb - cb
        distance = abs(sqrt(((r * r) * 0.3) + ((g * g) * 0.59) + ((b * b) * 0.11)))

        return distance

    def checkDistance(self, baseColor, checkColorList):
        similarDict = {}

        for cc in checkColorList:
            distance = self.colorDistance(baseColor, cc)
            # current_app.logger.debug(distance)
            if distance <= set.JUDGE_RANGE_VALUE:
                similarDict[cc] = self.howPoint(distance)

        sortedSimilarDict = sorted(similarDict.items(), key = lambda x: x[1])
        similarDict.clear()
        similarDict.update(sortedSimilarDict)

        return similarDict

    def colorDistanceLab(self, baseHexCode, checkHexCode):
        cc = ConvertColor()
        (bl, ba, bb) = cc.hexToLab(baseHexCode)
        (cl, ca, cb) = cc.hexToLab(checkHexCode)

        l = bl - cl
        a = ba - ca
        b = bb - cb
        distance = abs(sqrt((l * l)  + (a * a) + (b * b)))

        return distance

    def howPoint(self, distance):
        #10.0点満点
        point = (set.MAX_SIMILAR_POINT - distance)
        if isinstance(point, float) and point.is_integer():
            point = int(point)

        return (round(point, 1))

    def checkDistanceLab(self, baseColor, checkColorList):
        similarDict = {}

        for cc in checkColorList:
            distance = self.colorDistanceLab(baseColor, cc)
            # current_app.logger.debug(distance)
            if distance <= set.JUDGE_RANGE_VALUE:
                similarDict[cc] = self.howPoint(distance)

        sortedSimilarDict = sorted(similarDict.items(), key = lambda x: x[1])
        similarDict.clear()
        similarDict.update(sortedSimilarDict)

        return similarDict
