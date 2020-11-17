from Zombie import Zombie

class ZombieManager:

    zombies = []

    def spawn(self, x, y, health, speed):
        self.zombies.append(Zombie(x, y, health, speed))

    def tick(self, win, playerX, playerY, playerGun, shotVect):
        for zombie in self.zombies:
            zombie.updatePos(playerX, playerY)
            zombie.checkShot(shotVect, playerGun)
            zombie.draw(win, playerX, playerY)
            if not zombie.checkAlive():
                self.zombies.remove(zombie)
