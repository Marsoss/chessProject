import pygame

class Button:
    def __init__(self, screen, x, y, width, height, text, font, base_color, hover_color, text_color, action):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action

    def draw(self, is_hovered):
        color = self.hover_color if is_hovered else self.base_color
        pygame.draw.rect(self.screen, color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.screen.blit(text_surf, text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def activate(self):
        self.action(self.screen)

def activation(screen):
    print("Click!")

if __name__ == "__main__":
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Test button")
    BASE_COLOR = (200, 0, 0)
    HOVER_COLOR = (0, 200, 0)
    TEXT_COLOR = (255,255,255)
    b = Button(screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 100, 50, "PRESS", 
               pygame.font.Font(None, 40), BASE_COLOR, HOVER_COLOR, TEXT_COLOR, activation)
    while True:
        screen.fill(pygame.Color("black"))
        b.draw(b.is_hovered(pygame.mouse.get_pos()))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if b.is_hovered(pygame.mouse.get_pos()):
                    b.activate()
        pygame.display.flip()


