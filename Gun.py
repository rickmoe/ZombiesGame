import math

class Gun:

    DRAW_DIST_FROM_CENTER = 0.9     # Percentage of the body before the gun is drawn

    def draw(self, win, x, y, r, theta):
        pass

    @staticmethod
    def getName():
        return "Gun"

    @staticmethod
    def getDrawStartPos(x, y, r, theta):
        circX, circY = getRectCordsOnCircleDeg(theta - 90, r)
        pos = (x + circX, y + circY)
        return pos

    @staticmethod
    def getDrawEndPos(x, y, r, theta, length):
        x, y = Gun.getDrawStartPos(x, y, r, theta)
        deltaX = length * math.cos(degreesToRadians(theta))
        deltaY = length * math.sin(degreesToRadians(theta))
        print(math.cos(degreesToRadians(theta)))
        x += deltaX
        y -= deltaY
        return x, y

def degreesToRadians(deg):
    return deg / 180 * math.pi

def radiansToDegrees(rad):
    return rad * 180 / math.pi

def getRectCordsOnCircleRad(rad, r):
    x, y = (r * math.cos(rad), r * math.sin(rad))
    return x, -y

def getRectCordsOnCircleDeg(deg, r):
    return getRectCordsOnCircleRad(degreesToRadians(deg), r)
