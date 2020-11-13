import pygame
from Gun import Gun
from Constants import *
pygame.init()

class FiveSeven(Gun):

    LENGTH = 1.3                    # Multiplied by radius
    AMMO_CLIP = 20
    AMMO_RESERVE = 120
    SHOT_CD_FRAMES = 5
    SHOT_CD_RELOAD_FRAMES = 58
    SHOOT_SOUND_MAXTIME = 750
    SHOOT_SOUND = './Sounds/FiveSevenShot.mp3'    # https://www.fesliyanstudios.com/royalty-free-sound-effects-download/desert-eagle-.50-ae-gun-295
    CLICK_SOUND = './Sounds/M1911click.mp3'         # https://www.fesliyanstudios.com/royalty-free-sound-effects-download/p226-9mm-pistol-gun-296
    RELOAD_SOUND = './Sounds/M1911reload.wav'       # https://opengameart.org/content/handgun-reload-sound-effect

    def __init__(self):
        self.ammoClip = self.AMMO_CLIP
        self.ammoReserve = self.AMMO_RESERVE
        self.shotCdFrames = 0
        self.reloadCdFrames = 0

    def drawGunBody(self, win, x, y, r, theta):
        pygame.draw.line(win, (16, 16, 16), self.getDrawStartPos(x, y, r, theta), self.getDrawEndPos(x, y, r, theta, self.LENGTH * r), width=5)
        pygame.draw.line(win, (0, 64, 0), self.getDrawEndPos(x, y, r, theta, 0.8 * self.LENGTH * r), self.getDrawEndPos(x, y, r, theta, self.LENGTH * r), width=5)

    @staticmethod
    def getName():
        return "Five-Seven"
