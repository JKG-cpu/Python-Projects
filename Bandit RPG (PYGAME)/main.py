import pygame
from os.path import join

class Player:
    def __init__(self, power, hp, potions):
        self.screen = pygame.display.get_surface()
        self.head = join("img", "Knight")

        self.action = 0  # 0: Idle | 1: Attack | 2: Hurt | 3: Dead
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.clicked = False

        self.power = power
        self.max_hp = hp
        self.cur_hp = self.max_hp
        self.alive = True

        self.max_potions = potions
        self.cur_potions = self.max_potions
        self.potion_strength = 25

        self.animation_list = []
        self.load_all_images()

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_frect(center=(200, 260))

    def load_all_images(self):
        temp_list = []
        for i in range(8):
            img = pygame.image.load(join(self.head, "Idle", f"{i}.png")).convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        temp_list = []
        for i in range(8):
            img = pygame.image.load(join(self.head, "Attack", f"{i}.png")).convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

    def change_action(self, new_action):
        if new_action == 1 and not self.clicked:
            self.clicked = True
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def take_damage(self, amt):
        self.cur_hp -= amt
        if self.cur_hp < 0:
            self.cur_hp = 0

    def use_potion(self):
        self.cur_hp += self.potion_strength
        if self.cur_hp > self.max_hp:
            self.cur_hp = self.max_hp
        self.cur_potions -= 1

    def check_death(self):
        if self.cur_hp == 0:
            self.alive = False

    def update_animation(self):
        cd = 100
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > cd:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
                if self.action != 0:
                    self.action = 0
                    self.clicked = False

    def draw_player(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.update_animation()
        self.draw_player()

class Bandit:
    def __init__(self, x, y, hp, power, name, attack_delay=500):
        self.screen = pygame.display.get_surface()
        self.head = join("img", "Bandit")

        self.frame_index = 0
        self.action = 0   # 0: Idle | 1: Attack | 2: Dead | 3: Hurt
        self.update_time = pygame.time.get_ticks()
        self.hovering = False

        self.max_hp = hp
        self.cur_hp = self.max_hp
        self.alive = True
        self.power = power
        self.name = name

        # Attack delay logic
        self.attack_delay = attack_delay
        self.attack_start_time = None
        self.ready_to_attack = False
        self.attack_done = False
        self.damage_applied = False

        self.animation_list = []
        self.load_all_images()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_frect(center=(x, y))

    def load_all_images(self):
        # Idle
        temp_list = []
        for i in range(8):
            img = pygame.image.load(join(self.head, "Idle", f"{i}.png"))
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Attack
        temp_list = []
        for i in range(8):
            img = pygame.image.load(join(self.head, "Attack", f"{i}.png"))
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Death
        temp_list = []
        for i in range(10):
            img = pygame.image.load(join(self.head, "Death", f"{i}.png"))
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Hurt
        temp_list = []
        for i in range(3):
            img = pygame.image.load(join(self.head, "Hurt", f"{i}.png"))
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

    def outline_image(self, image, x, y):
        if self.alive:
            mask = pygame.mask.from_surface(image)
            outline_surface = mask.to_surface(setcolor=(255, 0, 0), unsetcolor=(0, 0, 0, 0))
            outline_surface.set_colorkey((0, 0, 0))
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx == 0 and dy == 0:
                        continue
                    self.screen.blit(outline_surface, (x + dx, y + dy))
            self.hovering = True

    def check_death(self):
        if self.cur_hp <= 0:
            self.alive = False
            self.action = 2

    def attacked(self, amt):
        self.cur_hp -= amt
        if self.cur_hp < 0:
            self.cur_hp = 0
            self.alive = False

    def start_attack(self):
        self.attack_start_time = pygame.time.get_ticks()
        self.ready_to_attack = False
        self.attack_done = False

    def update_animation(self):
        current_time = pygame.time.get_ticks()

        # DEAD: Play death animation slower and fully
        if not self.alive:
            if self.action != 2:
                self.action = 2
                self.frame_index = 0
                self.update_time = current_time

            self.image = self.animation_list[self.action][self.frame_index]

            if current_time - self.update_time > 150:
                self.update_time = current_time
                self.frame_index += 1
                if self.frame_index >= len(self.animation_list[self.action]):
                    self.frame_index = len(self.animation_list[self.action]) - 1  # Stay on last frame

            self.mask = pygame.mask.from_surface(self.image)
            return  # Skip rest of logic

        # Normal animation update (attack or idle)
        # Attack prep delay
        if self.attack_start_time is not None and self.action == 0 and not self.ready_to_attack:
            if current_time - self.attack_start_time < self.attack_delay:
                self.mask = pygame.mask.from_surface(self.image)
            else:
                self.ready_to_attack = True
                self.action = 1
                self.frame_index = 0
                self.update_time = current_time

        self.image = self.animation_list[self.action][self.frame_index]

        if current_time - self.update_time > 100:
            self.update_time = current_time
            self.frame_index += 1

            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 1:  # End of attack
                    self.attack_done = True
                    self.action = 0
                    self.frame_index = 0
                else:
                    self.frame_index = 0

        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, turn):
        mouse_pos = pygame.mouse.get_pos()
        rel_x = mouse_pos[0] - self.rect.x
        rel_y = mouse_pos[1] - self.rect.y

        if 0 <= rel_x < self.rect.width and 0 <= rel_y < self.rect.height:
            if self.mask.get_at((rel_x, rel_y)):
                if not turn:
                    self.outline_image(self.image, self.rect.x, self.rect.y)
            else:
                self.hovering = False

        self.screen.blit(self.image, self.rect)

    def update(self, turn=False):
        self.update_animation()
        self.draw(turn)
        self.check_death()

class Main:
    def __init__(self):
        pygame.init()
        head = join("img")
        WIDTH, HEIGHT = 800, 550
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("RPG Game | Imgs from Coding with Russ")

        icon_img = pygame.image.load(join(head, "Icons", "sword.png")).convert_alpha()
        pygame.display.set_icon(icon_img)

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True

        pygame.mouse.set_visible(False)
        self.mouse_img = pygame.image.load(join(head, "Icons", "sword.png")).convert_alpha()

        self.bg = pygame.image.load(join(head, "Background", "background.png")).convert_alpha()
        self.bg_rect = self.bg.get_frect(topleft=(0, 0))
        self.panel = pygame.image.load(join(head, "Icons", "panel.png")).convert_alpha()
        self.panel_rect = self.panel.get_frect(topleft=(0, self.bg_rect.bottom))

        self.potion_image = pygame.image.load(join(head, "Icons", "potion.png"))
        self.potion_rect = self.potion_image.get_frect(topleft=(50, (self.bg_rect.bottom + self.panel_rect.height / 2) - (self.potion_image.height / 2)))

        self.victory_image = pygame.image.load(join(head, "Icons", "victory.png"))
        self.victory_rect = self.victory_image.get_frect(center=(WIDTH // 2, HEIGHT // 2))

        self.levels = {
            '1': {
                "Player": Player(50, 1000, 3),
                "Bandits": [
                    Bandit(525, 270, 50, 10, "Bandit 1", 500),
                    Bandit(650, 270, 25, 5, "Bandit 2", 1500)
                ]
            }
        }
        self.cur_level = '1'
        self.player = self.levels[self.cur_level]["Player"]
        self.bandits = self.levels[self.cur_level]["Bandits"]
        self.turn = 0
        self.bandit_attacking = False
        self.font = pygame.font.Font(None, 25)
        self.victory = False

    def run(self):
        fade = 0
        fade_speed = 5
        fading = False
        fade_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        fade_surface.fill((0, 0, 0))

        fade_complete_time = None
        fade_hold_time = 1000  # Hold black for 1 second

        victory_fade = 0  # Fade in victory image

        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            self.clock.tick(self.fps)
            self.screen.fill("Black")
            events = pygame.event.get()

            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False

            if not self.victory:
                for e in events:
                    if self.turn == 0 and e.type == pygame.MOUSEBUTTONDOWN:
                        for bandit in self.bandits:
                            if bandit.hovering:
                                self.player.change_action(1)
                                bandit.attacked(self.player.power)
                                self.turn = 1
                                self.bandit_attacking = False

                        if self.potion_rect.collidepoint(e.pos) and self.player.cur_potions and self.player.cur_hp < self.player.max_hp:
                            self.player.use_potion()
                            self.turn = 1

                self.screen.blit(self.bg, self.bg_rect)
                self.screen.blit(self.panel, self.panel_rect)
                self.screen.blit(self.potion_image, self.potion_rect)

                self.player.update()

                for bandit in self.bandits:
                    bandit.update(self.turn == 1)

                if self.turn == 1:
                    if not self.bandit_attacking:
                        self.bandit_attacking = True
                        for bandit in self.bandits:
                            if bandit.alive:
                                bandit.start_attack()
                    else:
                        for bandit in self.bandits:
                            if bandit.attack_done and not bandit.damage_applied:
                                self.player.take_damage(bandit.power)
                                bandit.damage_applied = True

                        if all(b.attack_done or not b.alive for b in self.bandits):
                            self.turn = 0
                            self.bandit_attacking = False
                            for b in self.bandits:
                                b.attack_done = False
                                b.damage_applied = False

                x, y = 30, 0
                for bandit in self.bandits:
                    txt = self.font.render(f"{bandit.name} HP: {bandit.cur_hp} | Alive: {bandit.alive}", True, "White")
                    y += 40
                    self.screen.blit(txt, (x, y))

                y += 40
                txt = self.font.render(f"Player HP: {self.player.cur_hp} | Alive: {self.player.alive}", True, "White")
                self.screen.blit(txt, (x, y))

                # Handle fading to black
                if all(not b.alive for b in self.bandits):
                    if not fading:
                        self.bandits_dead_time = pygame.time.get_ticks()
                        fading = True

                    if pygame.time.get_ticks() - self.bandits_dead_time > 2000:
                        if fade < 255:
                            fade += fade_speed
                            fade_surface.set_alpha(fade)
                            self.screen.blit(fade_surface, (0, 0))
                        else:
                            if fade_complete_time is None:
                                fade_complete_time = pygame.time.get_ticks()

                            self.screen.blit(fade_surface, (0, 0))  # Keep it black

                            if pygame.time.get_ticks() - fade_complete_time >= fade_hold_time:
                                self.victory = True
                                victory_fade = 0  # Start fade-in for victory
                else:
                    self.bandits_dead_time = None
                    fading = False
                    fade = 0
                    fade_complete_time = None

                pygame.display.update()

            else:
                # Fade in victory image over black background
                self.screen.fill("black")

                if victory_fade < 255:
                    temp = self.victory_image.copy()
                    temp.set_alpha(victory_fade)
                    self.screen.blit(temp, self.victory_rect)
                    victory_fade += 5
                else:
                    self.screen.blit(self.victory_image, self.victory_rect)

                pygame.display.update()
            
            self.screen.blit(self.mouse_img, self.mouse_img.get_frect(center=mouse_pos))
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    main = Main()
    main.run()

    def cc():
        from os import system, name
        system('cls' if name == 'nt' else 'clear')

    cc()