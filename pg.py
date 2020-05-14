import pygame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive
from skimage.transform import warp, ProjectiveTransform, resize

nom = input("Quel est le nom de la série d'images à traiter ? \t")
nombre = int(input("Quel est le nombre de photo dans la série ? \t"))

hauteur = float(input("Quelle est la hauteur du cylindre ? \t"))
circonference = float(input("Quelle est le diamètre du cylindre ? \t")) * np.pi
r1 = hauteur / (circonference / 4)

name = nom + "1.jpg"
image = plt.imread(name)
Y, X, c = image.shape
dst = np.array([[0,0],[X,0],[X,Y],[0,Y]])
ccst = 1000

# Initialize Pygame.
pygame.init()
screen=pygame.display.set_mode((ccst, int(ccst * Y / X)))

def new_image(name):
    background = pygame.Surface(screen.get_size())
    image = pygame.image.load(name)
    foo = pygame.transform.scale(image, screen.get_size())
    background.blit(foo, (0,0))
    background= background.convert()
    screen.blit(background, (0,0))

    return

new_image(name)

# Create Pygame clock object.
clock = pygame.time.Clock()

mainloop = True
FPS = 20
i = 1
Coords = []
coord = []

while mainloop:
    # Do not go faster than this framerate.
    milliseconds = clock.tick(FPS)

    for event in pygame.event.get():
        # User presses QUIT-button.
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            # User presses ESCAPE-Key
            if event.key == pygame.K_ESCAPE:
                mainloop = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            coord.append([x, y])
            if len(coord) == 4:

                coord = np.array(coord) * X / ccst
                print(coord)
                Coords.append(coord)
                # Redressement de l'image
                # tfp = ProjectiveTransform()
                # tfp.estimate(coord, dst)
                # pic = warp(plt.imread(name), inverse_map = tfp.inverse)
                # pic = resize(pic, (ccst, int(r1 * ccst)))
                # propre.append(pic)

                # Passage à l'image suivante
                i += 1
                coord = []
                name = nom + str(i) + ".jpg"
                if i > nombre:
                    mainloop = False
                    break
                new_image(name)


    # Print framerate and playtime in titlebar.
    text = "Pour mon Papa"
    pygame.display.set_caption(text)

    #Update Pygame display.
    pygame.display.flip()

# Finish Pygame.
pygame.quit()

# Utilisation des coordonnées récupérées
print("Correction des images en cours...")
propre = []
for k, c in zip(range(1, nombre+1), Coords):
    print("Image {:d} sur {:d}".format(k, nombre))
    tfp = ProjectiveTransform()
    tfp.estimate(c, dst)
    pic =  warp(plt.imread(nom + str(k) + ".jpg"), inverse_map = tfp.inverse)
    pic = resize(pic, (ccst, int(r1 * ccst)))
    propre.append(pic)
plt.imsave("champi.jpg", np.concatenate(propre))
print("Correction terminée")
