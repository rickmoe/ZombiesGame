import pygame
from Gun import Gun
from Constants import *
pygame.init()

class M1911(Gun):

    LENGTH = 1.2                    # Multiplied by radius
    DRAW_DIST_FROM_CENTER = 0.9     # Percentage of the body before the gun is drawn
    AMMO_CLIP = 800
    AMMO_RESERVE = 800
    SHOT_CD_FRAMES = 5
    SHOT_CD_RELOAD_FRAMES = 85
    SHOOT_SOUND = './Sounds/M1911shot.mp3'      # https://www.fesliyanstudios.com/royalty-free-sound-effects-download/p226-9mm-pistol-gun-296
    CLICK_SOUND = './Sounds/M1911click.mp3'     # https://www.fesliyanstudios.com/royalty-free-sound-effects-download/p226-9mm-pistol-gun-296
    RELOAD_SOUND = './Sounds/M1911reload.wav'   # https://opengameart.org/content/gun-reload-sounds

    def __init__(self):
        self.ammoClip = self.AMMO_CLIP
        self.ammoReserve = self.AMMO_RESERVE
        self.shotCdFrames = 0
        self.reloadCdFrames = 0

    def draw(self, win, x, y, r, theta):
        self.drawGUI(win, self.getAmmoClip(), self.getAmmoReserve())
        r *= self.DRAW_DIST_FROM_CENTER
        pygame.draw.line(win, (64, 64, 64), self.getDrawStartPos(x, y, r, theta), self.getDrawEndPos(x , y , r, theta, self.LENGTH * r), width=4)

    @staticmethod
    def getName():
        return "M1911"
