#
import pygame

GAME_SIZE = GAME_WIDTH, GAME_HEIGHT = 750, 750
TITLE = "Pygame game"

class Card:
    already_clicked = False
    already_hovered = False
    already_dragged = False

    def __init__(self, position):
        self.image = pygame.Surface((75, 100))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft=position)
        self.hovered = False
        self.clicked = False
        self.dragged = False
        self.drag_offset = pygame.Vector2()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos) and not Card.already_clicked:
                    self.clicked = True
                    Card.already_clicked = True
                    self.drag_offset = pygame.Vector2(event.pos) - self.rect.topleft
                else:
                    self.clicked = False
                    Card.already_clicked = False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.clicked = False
                self.dragged = False
                Card.already_clicked = False
                Card.already_dragged = False

        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        if self.rect.collidepoint(mouse_pos.xy) and not Card.already_hovered:
            self.hovered = True
            Card.already_hovered = True
            if self.clicked:
                self.dragged = True
                Card.already_dragged = True
        elif not Card.already_dragged:
            self.hovered = False
            Card.already_hovered = False

    def check_drag(self):
        if self.dragged:
            self.rect.topleft = pygame.Vector2(pygame.mouse.get_pos()) - self.drag_offset

    def check_hover(self):
        if self.hovered:
            # Add outline, animations, do special effects here
            self.image.fill('yellow')
        else:
            # Return to normal image
            self.image.fill('green')

    def update(self):
        self.check_drag()
        self.check_hover()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen.fill("black")
        self.clock = pygame.time.Clock()

        self.cards = [Card((100 + i * 10, 75)) for i in range(10)]

    def _handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        for card in self.cards:
            card.handle_events(events)

    def run(self):
        while True:
            self.clock.tick(60)
            self.screen.fill("black")

            self._handle_events()

            for card in self.cards:
                card.update()
                card.draw(self.screen)

            pygame.display.flip()

def main():
    pygame.init()
    screen_hide = {"size": GAME_SIZE, "flags": pygame.HIDDEN}
    screen_show = {"size": GAME_SIZE, "flags": pygame.SHOWN}
    screen = pygame.display.set_mode(**screen_hide)
    pygame.display.set_caption(TITLE)

    game = Game(screen)
    pygame.display.set_mode(**screen_show)
    game.run()

if __name__ == '__main__':
    main()
