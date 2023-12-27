import pygame
import toolbox

class HUD():
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        self.state = 'mainmenu'

        self.hud_font = pygame.font.SysFont("microsoftyaheimicrosoftyaheiuibold", 15)

        self.score_text = self.hud_font.render("test text: ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 1234567890", True, (255, 255, 255))

        # Pinta: Move selected pixels move the white background away, Del the white background, move the background on top of the transparent background (even though the white backgroud is seemingly gone), use text to write on top of the white background selected deleted pixels
        # Load stuff for the main menu
        self.title_image = pygame.image.load("../assets/title.png")
        self.start_text = self.hud_font.render("Press any key to start", True, (255, 255, 255))

        # Load the images for the ammo tiles
        self.crate_icon = pygame.image.load("../assets/Crate.png")
        self.explosive_crate_icon = pygame.image.load("../assets/ExplosiveBarrel.png")
        self.split_shot_icon = pygame.image.load("../assets/iconSplitGreen.png")
        self.stream_shot_icon = pygame.image.load("../assets/iconStream.png")
        self.burst_shot_icon = pygame.image.load("../assets/iconBurst.png")
        self.normal_shot_icon = pygame.image.load("../assets/BalloonSmall2.png")

        # Make all the ammo tiles
        self.crate_ammo_tile = AmmoTile(self.screen, self.crate_icon, self.hud_font)
        self.explosive_crate_ammo_tile = AmmoTile(self.screen, self.explosive_crate_icon, self.hud_font)
        self.balloon_amoo_tile = AmmoTile(self.screen, self.normal_shot_icon, self.hud_font)

    def update(self):
        if self.state == 'ingame':
            # Draw the score text
            self.score_text = self.hud_font.render("Score: " + str(self.player.score), True, (255, 255, 255))
            self.screen.blit(self.score_text, (10, 10))

            # Draw the ammo tiles
            tile_x = 392
            self.crate_ammo_tile.update(tile_x, self.screen.get_height(), self.player.crate_ammo)
            tile_x += self.crate_ammo_tile.width
            self.explosive_crate_ammo_tile.update(tile_x, self.screen.get_height(), self.player.explosive_crate_ammo)
            tile_x += self.explosive_crate_ammo_tile.width
            # Figure out which icon to use for special ammo
            if self.player.shot_type == 'normal':
                self.balloon_amoo_tile.icon = self.normal_shot_icon
            elif self.player.shot_type == 'split':
                self.balloon_amoo_tile.icon = self.split_shot_icon
            elif self.player.shot_type == 'burst':
                self.balloon_amoo_tile.icon = self.burst_shot_icon
            elif self.player.shot_type == 'stream':
                self.balloon_amoo_tile.icon = self.stream_shot_icon
            
            self.balloon_amoo_tile.update(tile_x, self.screen.get_height(), self.player.special_ammo)

        elif self.state == 'mainmenu':
            title_x, title_y = toolbox.centeringCoords(self.title_image, self.screen)
            self.screen.blit(self.title_image, (title_x, title_y))
            text_x, text_y = toolbox.centeringCoords(self.start_text, self.screen)
            self.screen.blit(self.start_text, (text_x, text_y + 150))

class AmmoTile():
    def __init__(self, screen, icon, font):
        self.screen = screen
        self.icon = icon
        self.font = font
        self.bg_image = pygame.image.load("../assets/hudTile.png")
        self.width = self.bg_image.get_width()

    def update(self, x, y, ammo):
        # Draw tile background
        tile_rect = self.bg_image.get_rect()
        tile_rect.bottomleft = (x, y)
        self.screen.blit(self.bg_image, tile_rect)
        # Draw icon
        icon_rect = self.icon.get_rect()
        icon_rect.center = tile_rect.center
        self.screen.blit(self.icon, icon_rect)
        # Draw ammo number/amount
        ammo_text = self.font.render(str(ammo), True, (255, 255, 255))
        self.screen.blit(ammo_text, tile_rect.topleft)
