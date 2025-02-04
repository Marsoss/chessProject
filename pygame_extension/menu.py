import pygame
import sys
if __name__ != "__main__":
    from pygame_extension import button

class Menu:
    def __init__(self, screen, options, functions, back_function=None, title="Menu", font_size=40, button_size=(300, 60), gap=20):
        self.screen = screen
        self.options = options
        self.functions = functions
        self.back_function = back_function
        self.title = title
        self.font = pygame.font.Font(None, font_size)
        self.button_width, self.button_height = button_size
        self.gap = gap

        # Colors
        self.bg_color = (50, 50, 50)
        self.button_color = (100, 100, 200)
        self.button_hover_color = (150, 150, 250)
        self.text_color = (255, 255, 255)

        self.selected_index = 0
        self.buttons = []
        self.init_buttons()


    def init_buttons(self):
        screen_width, screen_height = self.screen.get_size()
        start_y = screen_height // 3
        for i, option in enumerate(self.options):
            x = (screen_width - self.button_width) // 2
            y = start_y + i * (self.button_height + self.gap)
            butn = button.Button(self.screen, x, y, self.button_width, self.button_height, option, self.font, self.button_color, self.button_hover_color, self.text_color, self.functions[i])
            self.buttons.append(butn)

    def draw(self):
        self.screen.fill(self.bg_color)
        mouse_pos = pygame.mouse.get_pos()
        for i, button in enumerate(self.buttons):
            button.draw(button.is_hovered(mouse_pos) or i == self.selected_index)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.buttons[self.selected_index].activate()
                elif event.key == pygame.K_BACKSPACE:
                    return "BACK"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, button in enumerate(self.buttons):
                    if button.is_hovered(pygame.mouse.get_pos()):
                        return button.activate()
        return None

    def run(self):
        while True:
            self.draw()
            result = self.handle_events()
            if result == "BACK" and self.back_function is not None:
                break
            pygame.display.flip()
        return self.back_function(self.screen)


def main_menu(screen):
    options = [
        "Joueur contre Joueur",
        "Joueur contre Ordinateur",
        "Ordinateur contre Ordinateur"
    ]

    functions = [
        cadence_menu,
        pve_game,
        ai_game
    ]
    menu = Menu(screen, options, functions, back_function=None, title="Menu Principal", button_size=(420,60))
    return menu.run()

def pve_game(screen):
    print("PvE game!")
    return main_menu(screen)
def ai_game(screen):
    print("AI game!")
    return main_menu(screen)

def cadence_menu(screen):
    options = [
        "Bullet",
        "Blitz",
        "Rapide",
        "Longue",
        "Personnaliser"
    ]
    functions = [
        bullet_game,
        blitz_game,
        rapid_game,
        long_game,
        custom_game
    ]
    menu = Menu(screen, options, functions, back_function=main_menu, title="Choix de la Cadence")
    return menu.run()

def bullet_game(screen):
    print("BULLET GAME!")
    return main_menu(screen)

def blitz_game(screen):
    print("BLITZ GAME!")
    return main_menu(screen)

def rapid_game(screen):
    print("RAPID GAME!")
    return main_menu(screen)

def long_game(screen):
    print("LONG GAME!")
    return main_menu(screen)

def custom_game(screen):
    print("CUSTOM GAME!")
    return main_menu(screen)

if __name__ == "__main__":
    import button
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menu du Jeu d'échecs")

    main_menu(screen)
        # Intégrer ici le lancement du mode sélectionné avec la cadence.
