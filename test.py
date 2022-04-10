
angle=0
angle_cible=90
pas = angle_cible/20

direction = 0
translate_max = 1

def draw():
    if(etat == rotate):
        self.transform = self.transform @ rotate((0, 0, 1), pas)
        angle += pas

        if angle >= angle_cible:
            etat = translate

    elif(etat == translate):
        self.transform = self.transform @ translate()

    self.models[anim_state].draw()

Animations à jouer :
    idle
    walking

Transformations à appliquer :
    rotate
    translate



Node(Spider_idle.fbx, Spider_walk.fbx)