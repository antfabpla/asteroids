import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    pygame.font.init()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    clock = pygame.time.Clock()
    dt = 0
    score = 0

    ship = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    field = AsteroidField()
    score_count = pygame.font.Font(None, 36)

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        for obj in updatable:
            obj.update(dt)
        for ast in asteroids:
            ship_collision = ast.collides_with(ship)
            for shot in shots:
                shot_collision = ast.collides_with(shot)
                if shot_collision == True:
                    log_event("asteroid_shot")
                    score += 100
                    shot.kill()
                    ast.split()
            if ship_collision == True:
                log_event("player_hit")
                ship.respawn()
                if ship.lives <= 0:
                    print("Game over!")
                    print(f"Score: {score}")
                    sys.exit()
                
            else:
                continue

        for sprite in drawable:
            sprite.draw(screen)
        screen.blit(((pygame.font.Font(None, 36)).render(f"Score: {score}", False, (255,255,255), (0,0,0))), (0,0))
        screen.blit(((pygame.font.Font(None, 36)).render(f"Lives: {ship.lives}", False, (255,255,255), (0,0,0))), (0,35))
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
