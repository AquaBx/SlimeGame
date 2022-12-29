from assets.scripts.gameobject import GameObject, Dynamic, Player, EmptyElement

def is_flying(self,obj:GameObject) -> None:
    BL = obj.position_matrix_bottom_left
    BR = obj.position_matrix_bottom_right

    i1, j1 = int(BL.y), int(BL.x)
    i2, j2 = int(BR.y), int(BR.x)

    if BL.x == float(j1):
        #j1 += 1
        pass
    if BR.x == float(j2):
        j2 -= 1
        pass

    if self.blocks[i1,j1] == EmptyElement and self.blocks[i2,j2] == EmptyElement:
        return True,None
    elif self.blocks[i1,j1] == EmptyElement :
        return False,self.blocks[i2,j2].position.y
    return False,self.blocks[i1,j1].position.y