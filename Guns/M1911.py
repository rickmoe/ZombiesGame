import pygame
from Gun import Gun
from Constants import *
pygame.init()

class M1911(Gun):

    LENGTH = 1.2                    # Multiplied by radius
    AMMO_CLIP = 8
    AMMO_RESERVE = 80
    SHOT_CD_FRAMES = 6
    SHOT_CD_RELOAD_FRAMES = 58
    SPEED_MULT = 0.975
    SHOOT_SOUND = './Sounds/M1911shot.mp3'      # https://www.fesliyanstudios.com/royalty-free-sound-effects-download/p226-9mm-pistol-gun-296
    CLICK_SOUND = './Sounds/M1911click.mp3'     # https://www.fesliyanstudios.com/royalty-free-sound-effects-download/p226-9mm-pistol-gun-296
    RELOAD_SOUND = './Sounds/M1911reload.wav'   # https://opengameart.org/content/handgun-reload-sound-effect

    def __init__(self):
        self.ammoClip = self.AMMO_CLIP
        self.ammoReserve = self.AMMO_RESERVE
        self.shotCdFrames = 0
        self.reloadCdFrames = 0

    def drawGunBody(self, win, x, y, r, theta):
        pygame.draw.line(win, (64, 64, 64), self.getDrawStartPos(x, y, r, theta), self.getDrawEndPos(x, y, r, theta, self.LENGTH * r), width=4)

    @staticmethod
    def getName():
        return "M1911"
