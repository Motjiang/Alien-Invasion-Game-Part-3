import sys
from zoneinfo import available_timezones

import pygame


from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """ Responds to keyboard events. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Updates position of bullets and remove old bullets"""
        # Update bullet positions
        self.bullets.update()

        """Get rif of bullets that have disappeared."""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_fleet(self)  :
       """Create the fleet of aliens."""
       #Create an alien and keep adding aliens until there is room.
       #Spacing between aliens is one alien width and one alien height

       alien=Alien(self)
       alien_width,alien_height=alien.rect.size
       available_space_x=self.settings.screen_width -(2 *alien_width)
       number_aliens_x=available_space_x // (2 * alien_width)

       #Calculate the number of rows of aliens that will fit on the screen
       ship_height=self.ship.rect.height
       available_space_y=(self.settings.screen_height - (2 * alien_height) - ship_height)
       number_rows=available_space_y //(2 * alien_height)

       #Create the full fleet of aliens
       for row_number in range (number_rows):
           for alien_number in range (number_aliens_x):
               self._create_alien(alien_number, row_number)


    def _create_alien(self,alien_number,row_number):
           alien=Alien(self)
           alien_width,alien_height=alien.rect.size
           alien.x=alien_width + 2 * alien_width * alien_number
           alien.rect.x=alien.x
           alien.rect.y =alien.rect.height + 2 * alien.rect.height * row_number
           self.aliens.add(alien)




    def _update_screen(self):
        """ Updates the game screen based on game settings. """
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

