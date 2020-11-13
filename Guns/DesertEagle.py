import pygame
from Gun import Gun
from Constants import *
pygame.init()

class DesertEagle(Gun):

    LENGTH = 1.5                    # Multiplied by radius
    AMMO_CLIP = 7
    AMMO_RESERVE = 56
    SHOT_CD_FRAMES = 10
    SHOT_CD_RELOAD_FRAMES = 58
    SHOOT_SOUND = './Sounds/DesertEagleShot.mp3'    # https://www.fesliyanstudios.com/royalty-free-sound-effects-download/desert-eagle-.50-ae-gun-295
    CLICK_SOUND = './Sounds/M1911click.mp3'         # https://www.fesliyanstudios.com/royalty-free-sound-effects-download/p226-9mm-pistol-gun-296
    RELOAD_SOUND = './Sounds/M1911reload.wav'       # https://opengameart.org/content/handgun-reload-sound-effect

    def __init__(self):
        self.ammoClip = self.AMMO_CLIP
        self.ammoReserve = self.AMMO_RESERVE
        self.shotCdFrames = 0
        self.reloadCdFrames = 0

    def drawGunBody(self, win, x, y, r, theta):
        pygame.draw.line(win, (192, 192, 192), self.getDrawStartPos(x, y, r, theta), self.getDrawEndPos(x, y, r, theta, self.LENGTH * r), width=5)
        pygame.draw.line(win, (32, 32, 32), self.getDrawEndPos(x, y, r, theta, 0.7 * self.LENGTH * r), self.getDrawEndPos(x, y, r, theta, self.LENGTH * r), width=5)

    @staticmethod
    def getName():
        return "Desert Eagle"
