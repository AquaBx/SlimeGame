from pygame import Rect, Vector2 as v2
from pygame.mask import Mask
from typing import Any, Union
from math import sqrt

from config import GameConfig, GameState
from assets.scripts.environment import MapElement
from assets.scripts.enemy import Enemy
from assets.scripts.gameobject import GameObject
from assets.scripts.gameobject_attributes import Damagable, Damager, Dynamic
from sounds import Sounds

class BlockCollide:
    def __init__(self, ref: MapElement = None, collide: bool = False, overlap_rect: Rect = None):
        self.ref: MapElement = ref
        self.collide: bool = collide
        self.overlap_rect: Rect = overlap_rect

def update_entity(world, obj: Union[GameObject, Dynamic]) -> None:
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

    blocks_collide: list[BlockCollide] = collide(world, obj) # on actualise les collisions pour avoir une meilleur gestion de l'axe x

    if dir.x < 0.0 and (blocks_collide[0].collide or blocks_collide[3].collide or blocks_collide[6].collide):

        correction: float = 0.0

        if blocks_collide[0].collide:
            correction = max(correction,blocks_collide[0].overlap_rect.width)
        if blocks_collide[3].collide:
            correction = max(correction,blocks_collide[3].overlap_rect.width)
        if blocks_collide[6].collide:
            correction = max(correction,blocks_collide[6].overlap_rect.width)

        obj.position.x += 1.0 * correction
        obj.velocity.x = 0.0

    elif dir.x > 0.0 and (blocks_collide[2].collide or blocks_collide[5].collide or blocks_collide[8].collide):

        correction: float = 0.0

        if blocks_collide[2].collide:
            correction = max(correction,blocks_collide[2].overlap_rect.width)
        if blocks_collide[5].collide:
            correction = max(correction,blocks_collide[5].overlap_rect.width)
        if blocks_collide[8].collide:
            correction = max(correction,blocks_collide[8].overlap_rect.width)

        obj.position.x += -1 * correction
        obj.velocity.x = 0.0
    
    blocks_damage(obj, velo_avant, blocks_collide, 0)

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


    if dir.y < 0.0 and ( blocks_collide[0].collide or blocks_collide[1].collide or blocks_collide[2].collide ):

        correction: float = 0.0

        if blocks_collide[0].collide:
            correction = max(correction,blocks_collide[0].overlap_rect.height)
        if blocks_collide[1].collide:
            correction = max(correction,blocks_collide[1].overlap_rect.height)
        if blocks_collide[2].collide:
            correction = max(correction,blocks_collide[2].overlap_rect.height)

        obj.position.y += 1 * correction
        obj.velocity.y = 0.0

    if dir.y > 0.0 and ( blocks_collide[6].collide or blocks_collide[7].collide or blocks_collide[8].collide ):

        obj.is_flying = False

        correction: float = 0

        if blocks_collide[6].collide:
            correction = max(correction, blocks_collide[6].overlap_rect.height)
        if blocks_collide[7].collide:
            correction = max(correction, blocks_collide[7].overlap_rect.height)
        if blocks_collide[8].collide:
            correction = max(correction, blocks_collide[8].overlap_rect.height)
        obj.position.y = int(obj.position.y) + 1 - correction
        obj.velocity.y = 0.0

    else:
        obj.is_flying = True

    blocks_damage(obj, velo_avant, blocks_collide, 1)


    if isinstance(obj, Damagable):
        enemies_damage(obj, world.enemies)
    
def collide(world, obj: Union[GameObject, Dynamic]) -> list[BlockCollide]:
    # we get all 9 blocs based on the centered position of the player (0)
    # | | | | | |
    # | |0|1|2| |
    # | |3|4|5| |
    # | |6|7|8| |
    # | | | | | |
    # for now there is a out of bound exception when we are not on the grid anymore
    jc = int( obj.position_matrix_center.x )
    ic = int( obj.position_matrix_center.y )
    blocks_arround: list[BlockCollide] = [
        BlockCollide(ref=world.blocks[i,j]) for i in range(ic-1,ic+2) for j in range(jc-1,jc+2)
    ]

    for key in range(len(blocks_arround)):
        if blocks_arround[key].ref == None:
            blocks_arround[key].collide = False
            blocks_arround[key].overlap_rect = None
        else:
            block: MapElement = blocks_arround[key].ref
            offset: v2 = block.position - obj.position
            collide_mask: Mask = obj.mask.overlap_mask(block.mask, offset)
            collide_rect: list[Rect] = collide_mask.connected_component().get_bounding_rects()
            if collide_rect:
                blocks_arround[key].collide = True
                blocks_arround[key].overlap_rect = collide_rect[0]
            else:
                blocks_arround[key].collide = False
                blocks_arround[key].overlap_rect = None
            
    return blocks_arround

def bump(obj: Union[GameObject, Dynamic, Damagable], damager: Damager, dir: v2, axis: int) -> None:
    obj.velocity[axis] = 0
    #if no movement when getting hit, bumb is vertical
    #bump in opposite movement direction
    obj.acceleration[axis] += -1 * dir[axis] * sqrt(2 * GameConfig.Gravity * damager.bump_factor * obj.mass) / GameState.physicDT * GameConfig.BLOCK_SIZE / (1+(axis==1 and dir[axis] == -1))
    obj.is_flying = True

def deal_damage(obj: Union[GameObject, Dynamic, Damagable], damager: Damager, dir: v2, axis: int = -1) -> None:
    if obj.hurt_time < damager.hurt_time*0.8 and not Sounds.is_busy("damage"):
        Sounds.play_audio("damage")
    if(obj.hurt_time == 0):                   
        obj.health -= damager.damage
        obj.hurt_time = damager.hurt_time
    if axis == -1:
        bump(obj, damager, dir, 0)
        bump(obj, damager, dir, 1)
    else:
        bump(obj, damager, dir, axis)
                        
def blocks_damage(obj: Union[GameObject, Dynamic] , velo_avant: v2, blocks_collide: list[BlockCollide], axis: int):          
    # in addition of being a Damaged, obj has to have life, so has basically to be the Player for now 
    if not isinstance(obj, Damagable): return
    for key in range(len(blocks_collide)):
        block: MapElement = blocks_collide[key].ref
        if not isinstance(block, Damager): continue
        if blocks_collide[key].collide:
            dir = v2(0,0)
            if velo_avant.length() == 0 or (axis == 1 and dir[1] == 0 and not obj.is_flying):
                dir = v2(0,1)
            else: dir[axis] = abs(velo_avant[axis])/(velo_avant[axis] + (velo_avant[axis]==0))
            deal_damage(obj, block, dir, axis)
            break
    
def enemies_damage(obj: Union[GameObject, Dynamic, Damagable], enemies: list[Enemy]):
    for enemy in enemies:
        offset: v2 = enemy.position - obj.position
        collide: Mask = obj.mask.overlap(enemy.mask, offset)

        if collide is None: continue

        vel = obj.velocity
        dir = (0,0)
        if vel.length() == 0:
            dir = (0,1)
        else: dir = (abs(vel[0])/(vel[0] + (vel[0]==0)),
            abs(vel[1])/(vel[1] + (vel[1]==0)))
            
        deal_damage(obj, enemy, dir)

