"""
Player entity class
"""


import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 75))
        self.image.fill((153, 151, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (100, 400)
        self.speed = 0.0
        self.isJumping = False
        self.isCrouching = False
        self.hoverCount = 0
        self.isOnFloor = False
        self.isDownJump = False
        self.isDownCrouch = False
        self.buttonsJump = (pygame.K_UP, pygame.K_SPACE,)
        self.buttonsCrouch = (pygame.K_DOWN,)
        self.gameSpeed = 1


    def crouch(self):
        if not self.isCrouching:
            self.isCrouching = True
            self.rect = self.rect.inflate(0, -25)
            # self.image.set_clip((50, 50))


    def standup(self):
        if self.isCrouching:
            self.isCrouching = False
            self.rect = self.rect.inflate(0, 25)

    def updateSpeed(self, newGameSpeed):
        self.gameSpeed = newGameSpeed

    def control(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.buttonsCrouch:
                self.isDownCrouch = True
            elif event.key in self.buttonsJump:
                self.isDownJump = True

        elif event.type == pygame.KEYUP:
            if event.key in self.buttonsCrouch:
                self.isDownCrouch = False
            elif event.key in self.buttonsJump:
                self.isDownJump = False


    def update(self):
        if not self.speed: self.rect.y += 1

        if not self.isDownJump:
            self.hoverCount = 0

        if self.isOnFloor:
            self.speed = 0

            if self.isDownJump:
                self.isJumping = True

                if self.isCrouching:
                    self.standup()

            elif self.isDownCrouch:
                if not self.isCrouching:
                    self.crouch()

            elif self.isCrouching:
                    self.standup()

        if self.isJumping:
#            maxHoverCount = 30
            if self.gameSpeed <= 2:     maxHoverCount = 30
            elif self.gameSpeed <= 4:   maxHoverCount = 23
            elif self.gameSpeed <= 8:   maxHoverCount = 16
            elif self.gameSpeed <= 16:  maxHoverCount = 9
            elif self.gameSpeed <= 32:  maxHoverCount = 5
            elif self.gameSpeed <= 64:  maxHoverCount = 2
            else:                       maxHoverCount = 1

            if self.isDownJump and self.hoverCount < maxHoverCount:
                self.speed -= self.gameSpeed/8 * ((math.cos(2*math.pi*self.hoverCount/(2*maxHoverCount))+1)/2.5+0.2)
                self.hoverCount += 1
            else:
                self.isJumping = False
        else:
            self.speed += 0.07 * self.gameSpeed

        self.rect.y += self.speed
