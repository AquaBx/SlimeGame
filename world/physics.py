from pygame import Rect, Vector2 as v2
from pygame.mask import Mask

from config import GameConfig, GameState
from assets.scripts.gameobject_attributes import Damaged, Damager

from math import sqrt

def update_entity(world, obj) -> None:
    

    pos_avant = v2(obj.position)
    velo_avant = v2(obj.velocity)
    # keyboard inputs
    obj.update()

    ######### X AXIS

    obj.acceleration.x -= obj.velocity.x / (GameState.physicDT * (10 + 30 * obj.is_flying))
    obj.velocity.x += obj.acceleration.x * GameState.physicDT
    obj.position.x += obj.velocity.x * GameState.physicDT
    obj.acceleration.x = 0

    dir = obj.position - pos_avant

    blocks_collide = collide(world, obj) # on actualise les collisions pour avoir une meilleur gestion de l'axe x

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
    
    damage(obj, velo_avant, blocks_collide, 0)

    ######### Y AXIS

    # Gravity
    obj.acceleration.y += obj.mass * GameConfig.Gravity * GameConfig.BLOCK_SIZE

    obj.velocity.y += obj.acceleration.y * GameState.physicDT
    obj.position.y += obj.velocity.y * GameState.physicDT
    obj.acceleration.y = 0

    dir = obj.position - pos_avant

    # /!\ EDGE CASE TO PREVENT CRASHING 
    if not 0 <= obj.position_matrix_center.y <= 63:
        obj.position.y = pos_avant.y
        obj.velocity.y = 0.0


    blocks_collide = collide(world, obj)


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

    damage(obj, velo_avant, blocks_collide, 1)

def collide(world, obj):
    # we get all 9 blocs based on the centered position of the player (0)
    # | | | | | |
    # | |0|1|2| |
    # | |3|4|5| |
    # | |6|7|8| |
    # | | | | | |
    # for now there is a out of bound exception when we are not on the grid anymore
    jc = int( obj.position_matrix_center.x )
    ic = int( obj.position_matrix_center.y )
    blocks_arround = [
        {"ref":world.blocks[i,j] } for i in range(ic-1,ic+2) for j in range(jc-1,jc+2)
    ]

    for key in range(len(blocks_arround)):
        if blocks_arround[key]["ref"] == None:
            blocks_arround[key]["collide"] = False
            blocks_arround[key]["overlap_rect"] = None
        else:
            obj2 = blocks_arround[key]["ref"]
            offset: v2 = obj2.position - obj.position
            collide_mask: Mask = obj.mask.overlap_mask(obj2.mask, offset)
            collide_rect: list[Rect] = collide_mask.connected_component().get_bounding_rects()
            if collide_rect:
                blocks_arround[key]["collide"] = True
                blocks_arround[key]["overlap_rect"] = collide_rect[0]
            else:
                blocks_arround[key]["collide"] = False
                blocks_arround[key]["overlap_rect"] = None
            
    return blocks_arround

def damage(obj, velo_avant, blocks_collide, axis):
    #0 or +-1
    dir = abs(velo_avant[axis])/(velo_avant[axis] + (velo_avant[axis] == 0))

    # in addition of being a Damaged, obj has to have life, so has basically to be the Player for now 
    if isinstance(obj, Damaged):
        for key in range(len(blocks_collide)):
            if not isinstance(blocks_collide[key]["ref"], Damager): continue
            if blocks_collide[key]["collide"]:
                if(obj.hurt_time == 0):                   
                    obj.health -= blocks_collide[key]["ref"].damage
                    obj.hurt_time = blocks_collide[key]["ref"].hurt_time
                    
                obj.velocity[axis] = 0
                #if no movement when getting hit, bumb is vertical
                #bump in opposite movement direction
                obj.acceleration[axis] += sqrt(2 * GameConfig.Gravity * blocks_collide[key]["ref"].bump_factor * obj.mass) / GameState.physicDT * GameConfig.BLOCK_SIZE * -dir
                obj.is_flying = True

                break
    
