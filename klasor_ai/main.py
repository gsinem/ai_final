import pygame
import sys
from game_logic import Move, GameResult, GameLogic
from ai_agent import AIAgent

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (800, 600)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 100, 255)
LIGHT_BLUE = (100, 200, 255)
FONT_SIZE = 32
TITLE_FONT_SIZE = 48
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20

# Set up the display
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Rock Paper Scissors AI")
clock = pygame.time.Clock()

# Initialize fonts
title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
font = pygame.font.Font(None, FONT_SIZE)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class Game:
    def __init__(self):
        self.ai_agent = AIAgent()
        self.player_score = 0
        self.ai_score = 0
        self.round_result = None
        self.player_move = None
        self.ai_move = None
        self.game_state = "playing"
        
        # Create buttons
        button_x = (WINDOW_SIZE[0] - (3 * BUTTON_WIDTH + 2 * BUTTON_MARGIN)) // 2
        button_y = WINDOW_SIZE[1] - BUTTON_HEIGHT - 50
        
        self.rock_button = Button(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Rock", BLUE, LIGHT_BLUE)
        self.paper_button = Button(button_x + BUTTON_WIDTH + BUTTON_MARGIN, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Paper", BLUE, LIGHT_BLUE)
        self.scissors_button = Button(button_x + 2 * (BUTTON_WIDTH + BUTTON_MARGIN), button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Scissors", BLUE, LIGHT_BLUE)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
            
        # Handle button clicks
        if self.rock_button.handle_event(event):
            self.play_round(Move.ROCK)
        elif self.paper_button.handle_event(event):
            self.play_round(Move.PAPER)
        elif self.scissors_button.handle_event(event):
            self.play_round(Move.SCISSORS)

    def play_round(self, player_move: Move):
        self.player_move = player_move
        self.ai_move = self.ai_agent.make_move()
        result = GameLogic.get_winner(player_move, self.ai_move)
        
        if result == GameResult.WIN:
            self.player_score += 1
        elif result == GameResult.LOSE:
            self.ai_score += 1
            
        self.round_result = result
        self.ai_agent.update_history(player_move, self.ai_move, result)

    def draw(self):
        screen.fill(WHITE)
        
        # Draw title
        title = title_font.render("Rock Paper Scissors AI", True, BLACK)
        screen.blit(title, (WINDOW_SIZE[0]//2 - title.get_width()//2, 50))
        
        # Draw scores
        score_text = font.render(f"Player: {self.player_score}  AI: {self.ai_score}", True, BLACK)
        screen.blit(score_text, (WINDOW_SIZE[0]//2 - score_text.get_width()//2, 150))
        
        # Draw moves
        if self.player_move and self.ai_move:
            moves_text = font.render(
                f"Player: {GameLogic.move_to_string(self.player_move)} vs AI: {GameLogic.move_to_string(self.ai_move)}",
                True, BLACK
            )
            screen.blit(moves_text, (WINDOW_SIZE[0]//2 - moves_text.get_width()//2, 250))
        
        # Draw result
        if self.round_result:
            result_text = font.render(
                f"Result: {self.round_result.name}",
                True, BLACK
            )
            screen.blit(result_text, (WINDOW_SIZE[0]//2 - result_text.get_width()//2, 350))
        
        # Draw quit instruction
        quit_text = font.render("Press 'Q' to Quit", True, GRAY)
        screen.blit(quit_text, (WINDOW_SIZE[0]//2 - quit_text.get_width()//2, 450))
        
        # Draw buttons
        self.rock_button.draw(screen)
        self.paper_button.draw(screen)
        self.scissors_button.draw(screen)
        
        pygame.display.flip()

def main():
    game = Game()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_input(event)
        
        game.draw()
        clock.tick(60)

if __name__ == "__main__":
    main() 