from Zombie import Zombie

class ZombieManager:

    zombies = []
    round = 0
    ZOMBIE_HEALTH = [150 + i * 100 for i in range(10)]
    spawnpoints = [[-200, -100, 150, 1.0], [-200, 100, 150, 1.0], [200, -100, 150, 1.0], [200, 100, 150, 1.0]]
    ZOMBIES_PER_HORDE = 24
    zombiesToSpawn = 0

    def spawn(self, x, y, health, speed):
        self.zombies.append(Zombie(x, y, health, speed))

    def tick(self, win, playerX, playerY, playerGun, shotVect):
        for zombie in self.zombies:
            zombie.updatePos(playerX, playerY)
            zombie.checkShot(shotVect, playerGun)
            zombie.draw(win, playerX, playerY)
            if not zombie.checkAlive():
                self.zombies.remove(zombie)
        if not self.zombies:
            self.incRound()
        self.spawnZombiesAtSpawnpoints()

    def incRound(self):
        self.round += 1
        self.zombiesToSpawn = self.getZombiesInWave(self.round)

    def spawnZombiesAtSpawnpoints(self):
        for spawnpoint in self.spawnpoints:
            if self.zombiesToSpawn > 0 and not self.spawnpointNearbyZombie(spawnpoint):
                self.spawn(spawnpoint[0], spawnpoint[1], ZombieManager.getZombieHealth(self.round), 1.0)
                self.zombiesToSpawn -= 1

    def spawnpointNearbyZombie(self, spawnpoint):
        for zombie in self.zombies:
            if abs(zombie.x - spawnpoint[0]) < 50 and abs(zombie.y - spawnpoint[1]) < 50:
                return True
        return False

    def getRound(self):
        return self.round

    @staticmethod
    def getZombiesInWave(roundNum):
        return roundNum * 0.15 * ZombieManager.ZOMBIES_PER_HORDE

    @staticmethod
    def getZombieHealth(roundNum):
        if roundNum < 11:
            return ZombieManager.ZOMBIE_HEALTH[roundNum - 1]
        else:
            return ZombieManager.ZOMBIE_HEALTH[len(ZombieManager.ZOMBIE_HEALTH) - 1] * pow(1.1, roundNum - len(ZombieManager.ZOMBIE_HEALTH))