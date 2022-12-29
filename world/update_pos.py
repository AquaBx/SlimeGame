from pygame import Vector2 as v2
from config import GameConfig, GameState
from assets.scripts.gameobject import Dynamic

def update_pos(self, obj : Dynamic) -> None:
    
    pos_avant = v2(obj.position.x,obj.position.y)

    obj.acceleration.x = 0
    obj.acceleration.y = 0

    # keyboard inputs
    obj.update()

    obj.acceleration.x -= obj.vitesse.x / (GameState.dt * (10 + 30 * obj.is_flying))
    obj.vitesse.x += obj.acceleration.x * GameState.dt
    obj.position.x += obj.vitesse.x * GameState.dt

    dir = obj.position - pos_avant

    blocks_collide = self.collide(obj) # on actualise les collisions pour avoir une meilleur gestion de l'axe x

    if dir.x < 0 and ( blocks_collide[0]["collide"] or blocks_collide[3]["collide"] or blocks_collide[6]["collide"] ):

        correction = 0

        if blocks_collide[0]["collide"]:
            correction = max(correction,blocks_collide[0]["overlap_rect"].width)
        if blocks_collide[3]["collide"]:
            correction = max(correction,blocks_collide[3]["overlap_rect"].width)
        if blocks_collide[6]["collide"]:
            correction = max(correction,blocks_collide[6]["overlap_rect"].width)

        obj.position.x += 1 * correction
        obj.vitesse.x = 0

    elif dir.x > 0 and ( blocks_collide[2]["collide"] or blocks_collide[5]["collide"] or blocks_collide[8]["collide"] ):

        correction = 0

        if blocks_collide[2]["collide"]:
            correction = max(correction,blocks_collide[2]["overlap_rect"].width)
        if blocks_collide[5]["collide"]:
            correction = max(correction,blocks_collide[5]["overlap_rect"].width)
        if blocks_collide[8]["collide"]:
            correction = max(correction,blocks_collide[8]["overlap_rect"].width)

        obj.position.x += -1 * correction
        obj.vitesse.x = 0
    
    # Gravity
    obj.acceleration.y += 5 * 9.81 * GameConfig.BLOCK_SIZE

    obj.vitesse.y += obj.acceleration.y * GameState.dt
    obj.position.y += obj.vitesse.y * GameState.dt

    dir = obj.position - pos_avant

    # /!\ EDGE CASE TO PREVENT CRASHING 
    if not 0 <= obj.position_matrix_center.y <= 63:
        obj.position.y = pos_avant.y
        obj.vitesse.y = 0

    blocks_collide = self.collide(obj)


    if dir.y < 0 and ( blocks_collide[0]["collide"] or blocks_collide[1]["collide"] or blocks_collide[2]["collide"] ):

        correction = 0

        if blocks_collide[0]["collide"]:
            correction = max(correction,blocks_collide[0]["overlap_rect"].height)
        if blocks_collide[1]["collide"]:
            correction = max(correction,blocks_collide[1]["overlap_rect"].height)
        if blocks_collide[2]["collide"]:
            correction = max(correction,blocks_collide[2]["overlap_rect"].height)
        
        obj.position.y += 1 * correction
        obj.vitesse.y = 0

    if dir.y > 0 and ( blocks_collide[6]["collide"] or blocks_collide[7]["collide"] or blocks_collide[8]["collide"] ):
        
        obj.is_flying = False
        
        correction = 0

        if blocks_collide[6]["collide"]:
            correction = max(correction,blocks_collide[6]["overlap_rect"].height)
        if blocks_collide[7]["collide"]:
            correction = max(correction,blocks_collide[7]["overlap_rect"].height)
        if blocks_collide[8]["collide"]:
            correction = max(correction,blocks_collide[8]["overlap_rect"].height)
        
        obj.position.y += -1 * correction
        obj.vitesse.y = 0
    else: obj.is_flying = True

    obj.acceleration.x = 0
    obj.acceleration.y = 0