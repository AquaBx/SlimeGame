def gravite(self,obj):
    y_vect = 5 * GameConfig.BLOCK_SIZE
    gravite = v2(0, y_vect)
    obj.acceleration.y = gravite[1] # + resistance[1]
    obj.vitesse.y += self.player.acceleration.y*GameState.dt
    obj.position.y += self.player.vitesse.y*GameState.dt