# pygame_functions
# (formerly wghs)

# Documentation at www.github.com/stevepaget/pygame_functions
# Report bugs to pagetworld@gmail.com


import os
import sys

import pygame

bgcolor = pygame.Color("black")
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()
spriteGroup = pygame.sprite.OrderedUpdates()
textboxGroup = pygame.sprite.OrderedUpdates()
gameClock = pygame.time.Clock()
backgroundImage = None
musicPaused = False
hiddenSprites = pygame.sprite.OrderedUpdates()

keydict = {"space": pygame.K_SPACE, "esc": pygame.K_ESCAPE, "up": pygame.K_UP, "down": pygame.K_DOWN,
           "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "enter": pygame.K_RETURN,
           "a": pygame.K_a,
           "b": pygame.K_b,
           "c": pygame.K_c,
           "d": pygame.K_d,
           "e": pygame.K_e,
           "f": pygame.K_f,
           "g": pygame.K_g,
           "h": pygame.K_h,
           "i": pygame.K_i,
           "j": pygame.K_j,
           "k": pygame.K_k,
           "l": pygame.K_l,
           "m": pygame.K_m,
           "n": pygame.K_n,
           "o": pygame.K_o,
           "p": pygame.K_p,
           "q": pygame.K_q,
           "r": pygame.K_r,
           "s": pygame.K_s,
           "t": pygame.K_t,
           "u": pygame.K_u,
           "v": pygame.K_v,
           "w": pygame.K_w,
           "x": pygame.K_x,
           "y": pygame.K_y,
           "z": pygame.K_z,
           "1": pygame.K_1,
           "2": pygame.K_2,
           "3": pygame.K_3,
           "4": pygame.K_4,
           "5": pygame.K_5,
           "6": pygame.K_6,
           "7": pygame.K_7,
           "8": pygame.K_8,
           "9": pygame.K_9,
           "0": pygame.K_0}
screen = ""
bgSurface = ""


class newSprite(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(loadImage(filename))
        self.image = pygame.Surface.copy(self.images[0])
        self.currentImage = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1
        self.originalWidth = self.rect.width
        self.originalHeight = self.rect.height

    def addImage(self, filename):
        self.images.append(loadImage(filename))
        print(self.images)

    def move(self, xpos, ypos, centre=False):
        if centre:
            self.rect.center = [xpos, ypos]
        else:
            self.rect.topleft = [xpos, ypos]

    def changeImage(self, index):
        self.currentImage = index
        if self.angle == 0:
            self.image = self.images[index]
        else:
            self.image = pygame.transform.rotate(self.images[self.currentImage], -self.angle)
        oldcenter = self.rect.center
        self.rect = self.image.get_rect()
        self.originalWidth = self.rect.width
        self.originalHeight = self.rect.height
        self.rect.center = oldcenter
        self.mask = pygame.mask.from_surface(self.image)
        update_display()


class newTextBox(pygame.sprite.Sprite):
    def __init__(self, text, xpos, ypos, width, case, maxLength, fontSize):
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        self.width = width
        self.initialText = text
        self.case = case
        self.maxLength = maxLength
        self.boxSize = int(fontSize * 1.7)
        self.image = pygame.Surface((width, self.boxSize))
        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, width - 1, self.boxSize - 1], 2)
        self.rect = self.image.get_rect()
        self.fontFace = pygame.font.match_font("Arial")
        self.fontColour = pygame.Color("black")
        self.initialColour = (180, 180, 180)
        self.font = pygame.font.Font(self.fontFace, fontSize)
        self.rect.topleft = [xpos, ypos]
        newSurface = self.font.render(self.initialText, True, self.initialColour)
        self.image.blit(newSurface, [10, 5])

    def update(self, keyevent):
        key = keyevent.key
        str = keyevent.str
        if key > 31 and key < 127 and (
                self.maxLength == 0 or len(self.text) < self.maxLength):  # only printable characters
            if keyevent.mod == 1 and self.case == 1 and key >= 97 and key <= 122:
                # force lowercase letters
                key -= 32
                self.text += chr(key)
            else:
                # use the unicode char
                self.text += str
        elif key == 8:
            # backspace. repeat until clear
            keys = pygame.key.get_pressed()
            nexttime = pygame.time.get_ticks() + 200
            deleting = True
            while deleting:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_BACKSPACE]:
                    thistime = pygame.time.get_ticks()
                    if thistime > nexttime:
                        self.text = self.text[0:len(self.text) - 1]
                        self.image.fill((255, 255, 255))
                        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
                        newSurface = self.font.render(self.text, True, self.fontColour)
                        self.image.blit(newSurface, [10, 5])
                        update_display()
                        nexttime = thistime + 50
                        pygame.event.clear()
                else:
                    deleting = False

        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
        newSurface = self.font.render(self.text, True, self.fontColour)
        self.image.blit(newSurface, [10, 5])
        update_display()

    def move(self, xpos, ypos, centre=False):
        if centre:
            self.rect.topleft = [xpos, ypos]
        else:
            self.rect.center = [xpos, ypos]

    def clear(self):
        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
        newSurface = self.font.render(self.initialText, True, self.initialColour)
        self.image.blit(newSurface, [10, 5])
        update_display()


class newLabel(pygame.sprite.Sprite):
    def __init__(self, text, fontSize, font, fontColour, xpos, ypos, background):
        pygame.sprite.Sprite.__init__(self)
        self.fontColour = pygame.Color(fontColour)
        self.fontFace = pygame.font.match_font(font)
        self.fontSize = fontSize
        self.background = background
        self.font = pygame.font.Font(self.fontFace, self.fontSize)
        newSurface = self.font.render(text, True, self.fontColour)
        self.rect = newSurface.get_rect()
        if self.background != "clear":
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill(pygame.Color(background))
            self.image.blit(newSurface, [0, 0])
        else:
            self.image = newSurface
        self.rect.center = [xpos, ypos]

    def update(self, newText, fontColour, background):
        if fontColour:
            self.fontColour = parse_colour(fontColour)
        if background:
            self.background = parse_colour(background)

        oldTopLeft = self.rect.topleft
        newSurface = self.font.render(newText, True, self.fontColour)
        self.rect = newSurface.get_rect()
        if self.background != "clear":
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill(self.background)
            self.image.blit(newSurface, [0, 0])
        else:
            self.image = newSurface
        self.rect.topleft = oldTopLeft
        update_display()


def loadImage(fileName, useColorKey=False):
    if os.path.isfile(fileName):
        image = pygame.image.load(fileName)
        image = image.convert_alpha()
        # Return the image
        return image
    else:
        raise Exception("Error loading image: " + fileName + " - Check filename and path?")


def screenSize(sizex, sizey, xpos=None, ypos=None, fullscreen=False):
    global bgcolor
    global screen
    global bgSurface
    if xpos != None and ypos != None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (xpos, ypos + 50)
    else:
        windowInfo = pygame.display.Info()
        monitorWidth = windowInfo.current_w
        monitorHeight = windowInfo.current_h
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % ((monitorWidth - sizex) // 2, (monitorHeight - sizey) // 2)
    if fullscreen:
        screen = pygame.display.set_mode((sizex, sizey), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((sizex, sizey), pygame.SRCALPHA)
    screen.fill(bgcolor)
    pygame.display.set_caption("Graphics Window")
    bgSurface = screen.copy()
    pygame.display.update()


def moveSprite(sprite, x, y, centre=True):
    sprite.move(x, y, centre)
    update_display()


def rotateSprite(sprite, angle):
    print("rotateSprite has been deprecated. Please use transformSprite")
    transformSprite(sprite, angle, 1)


def transformSprite(sprite, angle, scale):
    oldmiddle = sprite.rect.center
    sprite.angle = angle
    sprite.scale = scale
    sprite.image = pygame.transform.rotozoom(sprite.images[sprite.currentImage], -angle, scale)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = oldmiddle
    update_display()


def killSprite(sprite):
    sprite.kill()
    update_display()


def setBackgroundColour(colour):
    global bgcolor
    global bgSurface

    bgcolor = parse_colour(colour)
    screen.fill(bgcolor)
    pygame.display.update()
    bgSurface = screen.copy()


def setBackgroundImage(img):
    global bgSurface, backgroundImage
    surf = loadImage(img)
    backgroundImage = surf
    screen.blit(surf, [0, 0])
    bgSurface = screen.copy()
    update_display()


def hideSprite(sprite):
    hiddenSprites.add(sprite)
    spriteGroup.remove(sprite)
    update_display()


def hideAll():
    hiddenSprites.add(spriteGroup.sprites())
    spriteGroup.empty()
    update_display()


def unhideAll():
    spriteGroup.add(hiddenSprites.sprites())
    hiddenSprites.empty()
    update_display()


def showSprite(sprite):
    spriteGroup.add(sprite)
    update_display()


def makeSprite(filename):
    thisSprite = newSprite(filename)
    return thisSprite


def addSpriteImage(sprite, image):
    sprite.addImage(image)


def changeSpriteImage(sprite, index):
    sprite.changeImage(index)


def setSpriteImage(sprite, image):
    sprite.image = image


def nextSpriteImage(sprite):
    sprite.currentImage += 1
    if sprite.currentImage > len(sprite.images) - 1:
        sprite.currentImage = 0
    sprite.changeImage(sprite.currentImage)


def prevSpriteImage(sprite):
    sprite.currentImage -= 1
    if sprite.currentImage < 0:
        sprite.currentImage = len(sprite.images) - 1
    sprite.changeImage(sprite.currentImage)


def makeImage(filename):
    return loadImage(filename)


def touching(sprite1, sprite2):
    collided = pygame.sprite.collide_mask(sprite1, sprite2)
    return collided


def allTouching(spritename):
    if spriteGroup.has(spritename):
        collisions = pygame.sprite.spritecollide(spritename, spriteGroup, False, collided=pygame.sprite.collide_mask)
        collisions.remove(spritename)
        return collisions
    else:
        return []


def pause(milliseconds, allowEsc=True):
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    waittime = current_time + milliseconds
    while not (current_time > waittime or (keys[pygame.K_ESCAPE] and allowEsc)):
        pygame.event.clear()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_ESCAPE] and allowEsc):
            pygame.quit()
            sys.exit()
        current_time = pygame.time.get_ticks()


def drawRect(xpos, ypos, width, height, colour, linewidth=0):
    global bgSurface
    colour = parse_colour(colour)
    thisrect = pygame.draw.rect(screen, colour, [xpos, ypos, width, height], linewidth)
    bgrect = pygame.draw.rect(bgSurface, colour, [xpos, ypos, width, height], linewidth)
    pygame.display.update(thisrect)


def drawLine(x1, y1, x2, y2, colour, linewidth=1):
    global bgSurface
    colour = parse_colour(colour)
    thisrect = pygame.draw.line(screen, colour, (x1, y1), (x2, y2), linewidth)
    bgrect = pygame.draw.line(bgSurface, colour, (x1, y1), (x2, y2), linewidth)
    pygame.display.update(thisrect)


def drawPolygon(pointlist, colour, linewidth=0):
    global bgSurface
    colour = parse_colour(colour)
    thisrect = pygame.draw.polygon(screen, colour, pointlist, linewidth)
    bgrect = pygame.draw.polygon(bgSurface, colour, pointlist, linewidth)
    pygame.display.update(thisrect)


def drawEllipse(centreX, centreY, width, height, colour, linewidth=0):
    global bgSurface
    colour = parse_colour(colour)
    thisrect = pygame.Rect(centreX - width // 2, centreY - height // 2, width, height)
    pygame.draw.ellipse(screen, colour, thisrect, linewidth)
    # pygame.draw.ellipse(bgSurface, colour, thisrect, linewidth)
    pygame.display.update(thisrect)


def drawTriangle(x1, y1, x2, y2, x3, y3, colour, linewidth=0):
    global bgSurface
    colour = parse_colour(colour)
    thisrect = pygame.draw.polygon(screen, colour, [(x1, y1), (x2, y2), (x3, y3)], linewidth)
    bgrect = pygame.draw.polygon(bgSurface, colour, [(x1, y1), (x2, y2), (x3, y3)], linewidth)
    pygame.display.update(thisrect)


def clearShapes():
    global bgcolor
    global bgSurface, backgroundImage
    screen.fill(bgcolor)
    if backgroundImage:
        screen.blit(backgroundImage, [0, 0])
    bgSurface = screen.copy()
    update_display()


def updateShapes():
    pygame.display.update()


def end():
    pygame.quit()


def makeSound(filename):
    pygame.mixer.init()
    thissound = pygame.mixer.Sound(filename)

    return thissound


def playSound(sound, loops=0):
    sound.play(loops)


def stopSound(sound):
    sound.stop()


def playSoundAndWait(sound):
    sound.play()
    while pygame.mixer.get_busy():
        # pause
        pause(10)


def makeMusic(filename, volume):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.set_volume(volume)


def playMusic(loops=-1):
    global musicPaused
    if musicPaused:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.play(loops)
    musicPaused = False


def stopMusic():
    pygame.mixer.music.stop()


def pauseMusic():
    global musicPaused
    pygame.mixer.music.pause()
    musicPaused = True


def rewindMusic():
    pygame.mixer.music.rewind()


def endWait():
    print("Press ESC to quit")
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    waittime = 0
    while not keys[pygame.K_ESCAPE]:
        current_time = pygame.time.get_ticks()
        if current_time > waittime:
            pygame.event.clear()
            keys = pygame.key.get_pressed()
            waittime += 20
    pygame.quit()


def keyPressed(keyCheck=""):
    global keydict
    pygame.event.clear()
    keys = pygame.key.get_pressed()
    if sum(keys) > 0:
        if keyCheck == "" or keys[keydict[keyCheck.lower()]]:
            return True
    return False


def makeLabel(text, fontSize, xpos, ypos, fontColour='black', font='Arial', background="clear"):
    # make a text sprite
    thisText = newLabel(text, fontSize, font, fontColour, xpos, ypos, background)
    return thisText


def moveLabel(sprite, x, y, center=True):
    if center:
        sprite.rect.center = [x, y]
    else:
        sprite.rect.topleft = [x, y]
    update_display()


def changeLabel(textObject, newText, fontColour=None, background=None):
    textObject.update(newText, fontColour, background)
    # update_display()


def waitPress():
    pygame.event.clear()
    keypressed = False
    thisevent = pygame.event.wait()
    while thisevent.type != pygame.KEYDOWN:
        thisevent = pygame.event.wait()
    return thisevent.key


def makeTextBox(xpos, ypos, width, case=0, startingText="Please type here", maxLength=0, fontSize=22):
    thisTextBox = newTextBox(startingText, xpos, ypos, width, case, maxLength, fontSize)
    textboxGroup.add(thisTextBox)
    return thisTextBox


def textBoxInput(textbox):
    # starts grabbing key inputs, putting into textbox until enter pressed
    global keydict
    textbox.text = ""
    while True:
        update_display()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    textbox.clear()
                    return textbox.text
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    textbox.update(event)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def clock():
    current_time = pygame.time.get_ticks()
    return current_time


def tick(fps):
    gameClock.tick(fps)


def showLabel(label_name):
    textboxGroup.add(label_name)
    update_display()


def hideLabel(label_name):
    textboxGroup.remove(label_name)
    update_display()


def hide_all_labels():
    for label in textboxGroup:
        textboxGroup.remove(label)
    update_display()


def show_text_box(text_box_name):
    textboxGroup.add(text_box_name)
    update_display()


def hide_text_box(text_box_name):
    textboxGroup.remove(text_box_name)
    update_display()


def update_display():
    global bgSurface
    # spriteRects = spriteGroup.draw(screen)
    # textboxRects = textboxGroup.draw(screen)
    pygame.display.update()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    spriteGroup.clear(screen, bgSurface)
    textboxGroup.clear(screen, bgSurface)


def mouse_pressed():
    pygame.event.clear()
    mouseState = pygame.mouse.get_pressed()
    if mouseState[0]:
        return True
    else:
        return False


def sprite_clicked(sprite):
    mouseState = pygame.mouse.get_pressed()
    if not mouseState[0]:
        return False  # not pressed
    pos = pygame.mouse.get_pos()
    if sprite.rect.collidepoint(pos):
        return True
    else:
        return False


def parse_colour(colour):
    if type(colour) == str:
        # check to see if valid colour
        return pygame.Color(colour)
    else:
        colourRGB = pygame.Color("white")
        colourRGB.r = colour[0]
        colourRGB.g = colour[1]
        colourRGB.b = colour[2]
        return colourRGB


def mouse_x():
    x = pygame.mouse.get_pos()
    return x[0]


def mouse_y():
    y = pygame.mouse.get_pos()
    return y[1]


def animate_sprite_movement(end_x, end_y, move_sprite, speed=0.005):
    """
    Animate the movement on object from start_x, start_y to end_x, end_y
    :param end_x: The final x position. (int)
    :param end_y: The final y position. (int)
    :param move_sprite: The sprite to move. (Sprite)
    :param speed: The speed of the movement, a value between 0 and 1, 1 is instant, 0 won't move.
    """

    start_x, start_y = move_sprite.rect.center

    x_delta = end_x - start_x
    y_delta = end_y - start_y

    current_x = start_x
    current_y = start_y

    for i in range(int(1 / speed)):
        current_x = current_x + (x_delta * speed)
        current_y = current_y + (y_delta * speed)

        moveSprite(move_sprite, int(current_x), int(current_y))
        showSprite(move_sprite)

    # Fix inconsistent movement with the animation.
    moveSprite(move_sprite, end_x, end_y)


if __name__ == "__main__":
    print(""""pygame_functions is not designed to be run directly.
    See the wiki at https://github.com/StevePaget/Pygame_Functions/wiki/Getting-Started for 
    more information(this version has been updates by PoisonRain)""")