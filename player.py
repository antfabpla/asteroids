import pygame
from circleshape import CircleShape
from shot import Shot
from constants import PLAYER_RADIUS, PLAYER_INITIAL_SPEED, PLAYER_ACCELERATION, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, LINE_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.shot_cooldown = 0
        self.respawn_cooldown = 0
        self.rotation = 180
        self.lives = 3
        self.speed = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
    
    def reset(self):
        self.position = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.speed = 0
        self.rotation = 180
    
    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * self.speed * dt
        self.position += rotated_with_speed_vector
    
    def accelerate(self, dt, acc=PLAYER_ACCELERATION):
        self.speed += acc * dt

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shot_cooldown -= dt
        if self.speed > 0:
            self.accelerate(-dt, PLAYER_ACCELERATION/2)
        if self.speed < 0:
            self.accelerate(dt, PLAYER_ACCELERATION/2)
        self.move(dt)
        if keys[pygame.K_w]:
            self.accelerate(dt)
        if keys[pygame.K_s]:
            self.accelerate(-dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        if self.shot_cooldown > 0:
            return
        else:
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        bullet = Shot(self.position.x, self.position.y)
        bullet.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def respawn(self):

        if self.lives <= 0:
            return
        self.lives -= 1
        self.reset()