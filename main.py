import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_RADIUS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    fps_clock = pygame.time.Clock()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    dt = 0

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        dt = fps_clock.tick(60) / 1000
        screen.fill("black")
        
        updatable.update(dt)
        for sprite in asteroids:
            if player.collides_with(sprite):
                log_event("player_hit")
                print("Game over!")
                sys.exit(0)
            for shot in shots:
                if shot.collides_with(sprite):
                    log_event("asteroid_shot")
                    sprite.kill()
                    shot.kill()    
        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip()
    

if __name__ == "__main__":
    main()