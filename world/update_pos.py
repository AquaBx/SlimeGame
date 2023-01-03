from pygame import Vector2 as v2
from config import GameConfig, GameState

def update_pos(self, obj) -> None:
    
    pos_avant = v2(obj.position.x,obj.position.y)

    # keyboard inputs
    obj.update()

    obj.acceleration.x -= obj.velocity.x / (GameState.PhysicDT * (10 + 30 * obj.is_flying))
    obj.velocity.x += obj.acceleration.x * GameState.PhysicDT
    obj.position.x += obj.velocity.x * GameState.PhysicDT

    dir = obj.position - pos_avant

    blocks_collide = self.collide(obj) # on actualise les collisions pour avoir une meilleur gestion de l'axe x

    if dir.x < 0.0 and (blocks_collide[0]["collide"] or blocks_collide[3]["collide"] or blocks_collide[6]["collide"]):

        correction: float = 0.0

        if blocks_collide[0]["collide"]:
            correction = max(correction,blocks_collide[0]["overlap_rect"].width)
        if blocks_collide[3]["collide"]:
            correction = max(correction,blocks_collide[3]["overlap_rect"].width)
        if blocks_collide[6]["collide"]:
            correction = max(correction,blocks_collide[6]["overlap_rect"].width)

        obj.position.x += 1.0 * correction
        obj.velocity.x = 0.0

    elif dir.x > 0.0 and (blocks_collide[2]["collide"] or blocks_collide[5]["collide"] or blocks_collide[8]["collide"]):

        correction: float = 0.0

        if blocks_collide[2]["collide"]:
            correction = max(correction,blocks_collide[2]["overlap_rect"].width)
        if blocks_collide[5]["collide"]:
            correction = max(correction,blocks_collide[5]["overlap_rect"].width)
        if blocks_collide[8]["collide"]:
            correction = max(correction,blocks_collide[8]["overlap_rect"].width)

        obj.position.x += -1 * correction
        obj.velocity.x = 0.0

    # Gravity
    obj.acceleration.y += obj.mass * GameConfig.Gravity * GameConfig.BLOCK_SIZE

    obj.velocity.y += obj.acceleration.y * GameState.PhysicDT
    obj.position.y += obj.velocity.y * GameState.PhysicDT

    dir = obj.position - pos_avant

    # /!\ EDGE CASE TO PREVENT CRASHING 
    if not 0 <= obj.position_matrix_center.y <= 63:
        obj.position.y = pos_avant.y
        obj.velocity.y = 0.0

    blocks_collide = self.collide(obj)


    if dir.y < 0.0 and ( blocks_collide[0]["collide"] or blocks_collide[1]["collide"] or blocks_collide[2]["collide"] ):

        correction: float = 0.0

        if blocks_collide[0]["collide"]:
            correction = max(correction,blocks_collide[0]["overlap_rect"].height)
        if blocks_collide[1]["collide"]:
            correction = max(correction,blocks_collide[1]["overlap_rect"].height)
        if blocks_collide[2]["collide"]:
            correction = max(correction,blocks_collide[2]["overlap_rect"].height)

        obj.position.y += 1 * correction
        obj.velocity.y = 0.0

    if dir.y > 0.0 and ( blocks_collide[6]["collide"] or blocks_collide[7]["collide"] or blocks_collide[8]["collide"] ):

        obj.is_flying = False

        correction: float = 0

        if blocks_collide[6]["collide"]:
            correction = max(correction, blocks_collide[6]["overlap_rect"].height)
        if blocks_collide[7]["collide"]:
            correction = max(correction, blocks_collide[7]["overlap_rect"].height)
        if blocks_collide[8]["collide"]:
            correction = max(correction, blocks_collide[8]["overlap_rect"].height)
        obj.position.y = int(obj.position.y) + 1 - correction
        obj.velocity.y = 0.0

    else:
        obj.is_flying = True

    obj.acceleration = v2(0.0)
