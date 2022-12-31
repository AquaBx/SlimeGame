from pygame import Vector2 as v2,Rect
from pygame.mask import Mask

def collide(self, obj):
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
        {"ref":self.blocks[i,j] } for i in range(ic-1,ic+2) for j in range(jc-1,jc+2)
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