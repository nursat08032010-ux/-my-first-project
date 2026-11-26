# import pygame
# import random
# import sys

# pygame.init()

# # 1. Константы окна
# WIDTH = 800
# HEIGHT = 600
# FPS = 60

# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Papers, Please Lite — Урок 1: Работа с курсором")
# clock = pygame.time.Clock()

# # Шрифты (arial корректно отображает кириллицу)
# font_title = pygame.font.SysFont("arial", 22, bold=True)
# font_card = pygame.font.SysFont("consolas", 22)
# font_btn = pygame.font.SysFont("arial", 24, bold=True)
# font_hud = pygame.font.SysFont("arial", 20, bold=True)

# # Цветовая палитра
# COLOR_BG = (28, 30, 36)
# COLOR_RULE_BG = (45, 48, 58)
# COLOR_CARD = (235, 230, 215)       # Цвет бумажного бланка
# COLOR_CARD_BORDER = (160, 150, 130)
# COLOR_INK = (30, 32, 38)           # Цвет текста на бланке

# COLOR_GREEN = (46, 160, 67)
# COLOR_GREEN_HOVER = (65, 195, 88)
# COLOR_RED = (205, 55, 55)
# COLOR_RED_HOVER = (235, 75, 75)
# COLOR_TEXT_LIGHT = (240, 245, 250)

# # Данные для генерации пропусков
# NAMES = ["Иванов А.С.", "Смирнова Е.В.", "Ким Д.Р.", "Ахметов Т.М.", "Волкова О.П.", "Соколов И.Н."]
# ROLES = ["ИНЖЕНЕР", "ОХРАНА", "ГОСТЬ", "КУРЬЕР"]
# YEARS = [2024, 2025, 2026, 2026]  # 2026 встречается чаще


# def generate_visitor():
#     """Создает словарь с данными нового посетителя."""
#     return {
#         "name": random.choice(NAMES),
#         "role": random.choice(ROLES),
#         "year": random.choice(YEARS),
#         "code": random.randint(100, 999),
#     }


# def is_visitor_valid(visitor):
#     """
#     ПРАВИЛО ДНЯ:
#     Пропускать только тех, у кого год пропуска == 2026 И код доступа >= 400.
#     """
#     return visitor["year"] == 2026 and visitor["code"] >= 400


# # Прямоугольники интерфейса (карта и две интерактивные кнопки-штампы)
# card_rect = pygame.Rect(210, 165, 380, 235)
# approve_btn = pygame.Rect(180, 445, 195, 65)
# deny_btn = pygame.Rect(425, 445, 195, 65)

# # Игровое состояние
# current_visitor = generate_visitor()
# score = 0
# mistakes = 0
# feedback_text = "Проверьте документ и нажмите штамп"
# feedback_color = (170, 175, 185)

# running = True
# while running:
#     # Получаем текущую позицию курсора для подсветки кнопок (hover)
#     mouse_pos = pygame.mouse.get_pos()

#     # --- ЭТАП 1: Обработка кликов мыши ---
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#         elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#             player_decision = None

#             # Проверяем, по какой кнопке кликнул игрок
#             if approve_btn.collidepoint(event.pos):
#                 player_decision = True
#             elif deny_btn.collidepoint(event.pos):
#                 player_decision = False

#             # Если игрок нажал одну из кнопок — сверяем решение с правилом
#             if player_decision is not None:
#                 actual_valid = is_visitor_valid(current_visitor)

#                 if player_decision == actual_valid:
#                     score += 1
#                     feedback_text = "ВЕРНО! Документ обработан правильно."
#                     feedback_color = COLOR_GREEN_HOVER
#                 else:
#                     mistakes += 1
#                     feedback_text = "ВЫГОВОР! Нарушена инструкция КПП."
#                     feedback_color = COLOR_RED_HOVER

#                 # Вызываем следующего посетителя
#                 current_visitor = generate_visitor()

#     # --- ЭТАП 2: Отрисовка интерфейса ---
#     screen.fill(COLOR_BG)

#     # 1. Верхняя панель со статистикой
#     score_surf = font_hud.render(f"Одобрено верно: {score}", True, COLOR_TEXT_LIGHT)
#     mistakes_surf = font_hud.render(f"Выговоры: {mistakes} / 3", True, COLOR_RED_HOVER if mistakes > 0 else COLOR_TEXT_LIGHT)
#     screen.blit(score_surf, (30, 20))
#     screen.blit(mistakes_surf, (WIDTH - mistakes_surf.get_width() - 30, 20))

#     # 2. Плашка с правилом дня
#     rule_rect = pygame.Rect(60, 65, WIDTH - 120, 65)
#     pygame.draw.rect(screen, COLOR_RULE_BG, rule_rect, border_radius=8)
#     pygame.draw.rect(screen, (90, 95, 110), rule_rect, width=2, border_radius=8)

#     rule_surf = font_title.render("ИНСТРУКЦИЯ: Пропускать только если ГОД = 2026 и КОД >= 400", True, (255, 220, 100))
#     screen.blit(rule_surf, rule_surf.get_rect(center=rule_rect.center))

#     # 3. Карточка документа посетителя
#     pygame.draw.rect(screen, COLOR_CARD, card_rect, border_radius=10)
#     pygame.draw.rect(screen, COLOR_CARD_BORDER, card_rect, width=4, border_radius=10)

#     # Заголовок карточки
#     doc_header = font_title.render("ПРОПУСК НА ТЕРРИТОРИЮ", True, COLOR_INK)
#     screen.blit(doc_header, (card_rect.x + 25, card_rect.y + 20))
#     pygame.draw.line(screen, COLOR_CARD_BORDER, (card_rect.x + 20, card_rect.y + 55), (card_rect.right - 20, card_rect.y + 55), 2)

#     # Поля документа
#     lines = [
#         f"ФИО:       {current_visitor['name']}",
#         f"ДОЛЖНОСТЬ: {current_visitor['role']}",
#         f"ГОД ВЫД.:  {current_visitor['year']}",
#         f"КОД ДОСТ.: {current_visitor['code']}",
#     ]
#     for i, text in enumerate(lines):
#         line_surf = font_card.render(text, True, COLOR_INK)
#         screen.blit(line_surf, (card_rect.x + 25, card_rect.y + 75 + i * 36))

#     # 4. Статус последнего решения
#     fb_surf = font_hud.render(feedback_text, True, feedback_color)
#     screen.blit(fb_surf, fb_surf.get_rect(center=(WIDTH // 2, 418)))

#     # 5. Интерактивные кнопки (меняют цвет при наведении курсора)
#     is_hover_approve = approve_btn.collidepoint(mouse_pos)
#     is_hover_deny = deny_btn.collidepoint(mouse_pos)

#     pygame.draw.rect(screen, COLOR_GREEN_HOVER if is_hover_approve else COLOR_GREEN, approve_btn, border_radius=10)
#     if is_hover_approve:
#         pygame.draw.rect(screen, COLOR_TEXT_LIGHT, approve_btn, width=3, border_radius=10)

#     pygame.draw.rect(screen, COLOR_RED_HOVER if is_hover_deny else COLOR_RED, deny_btn, border_radius=10)
#     if is_hover_deny:
#         pygame.draw.rect(screen, COLOR_TEXT_LIGHT, deny_btn, width=3, border_radius=10)

#     app_text = font_btn.render("ОДОБРИТЬ", True, COLOR_TEXT_LIGHT)
#     deny_text = font_btn.render("ОТКАЗАТЬ", True, COLOR_TEXT_LIGHT)
#     screen.blit(app_text, app_text.get_rect(center=approve_btn.center))
#     screen.blit(deny_text, deny_text.get_rect(center=deny_btn.center))

#     pygame.display.flip()
#     clock.tick(FPS)

# pygame.quit()
# sys.exit()

# import pygame
# import random
# import sys

# pygame.init()

# # 1. Константы окна
# WIDTH = 800
# HEIGHT = 600
# FPS = 60

# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Papers, Please Lite — Урок 1: Работа с курсором")
# clock = pygame.time.Clock()

# # Шрифты
# font_title = pygame.font.SysFont("arial", 22, bold=True)
# font_card = pygame.font.SysFont("consolas", 22)
# font_btn = pygame.font.SysFont("arial", 24, bold=True)
# font_hud = pygame.font.SysFont("arial", 20, bold=True)
# font_game_over = pygame.font.SysFont("arial", 38, bold=True)
# font_restart = pygame.font.SysFont("arial", 24)

# # Цветовая палитра
# COLOR_BG = (28, 30, 36)
# COLOR_RULE_BG = (45, 48, 58)
# COLOR_CARD = (235, 230, 215)
# COLOR_CARD_BORDER = (160, 150, 130)
# COLOR_INK = (30, 32, 38)

# COLOR_GREEN = (46, 160, 67)
# COLOR_GREEN_HOVER = (65, 195, 88)
# COLOR_RED = (205, 55, 55)
# COLOR_RED_HOVER = (235, 75, 75)
# COLOR_TEXT_LIGHT = (240, 245, 250)

# # Данные посетителей
# NAMES = ["Иванов А.С.", "Смирнова Е.В.", "Ким Д.Р.",
#          "Ахметов Т.М.", "Волкова О.П.", "Соколов И.Н."]
# ROLES = ["ИНЖЕНЕР", "ОХРАНА", "ГОСТЬ", "КУРЬЕР"]
# YEARS = [2024, 2025, 2026, 2026]


# def generate_visitor():
#     return {
#         "name": random.choice(NAMES),
#         "role": random.choice(ROLES),
#         "year": random.choice(YEARS),
#         "code": random.randint(100, 999),
#     }


# # Новое правило проверки
# def is_visitor_valid(visitor):
#     return (
#         visitor["role"] != "ГОСТЬ"
#         and visitor["year"] == 2026
#         and visitor["code"] >= 400
#     )


# # Прямоугольники интерфейса
# card_rect = pygame.Rect(210, 165, 380, 235)
# approve_btn = pygame.Rect(180, 445, 195, 65)
# deny_btn = pygame.Rect(425, 445, 195, 65)

# # Игровое состояние
# current_visitor = generate_visitor()
# score = 0
# mistakes = 0
# game_over = False

# feedback_text = "Проверьте документ и нажмите штамп"
# feedback_color = (170, 175, 185)

# running = True

# while running:
#     mouse_pos = pygame.mouse.get_pos()

#     # ЭТАП 1. Обработка событий
#     for event in pygame.event.get():

#         if event.type == pygame.QUIT:
#             running = False

#         # Перезапуск игры клавишей R
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_r and game_over:
#                 current_visitor = generate_visitor()
#                 score = 0
#                 mistakes = 0
#                 game_over = False
#                 feedback_text = "Проверьте документ и нажмите штамп"
#                 feedback_color = (170, 175, 185)

#         # Обработка кликов мыши
#         elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

#             if not game_over:
#                 player_decision = None

#                 if approve_btn.collidepoint(event.pos):
#                     player_decision = True
#                 elif deny_btn.collidepoint(event.pos):
#                     player_decision = False

#                 if player_decision is not None:
#                     actual_valid = is_visitor_valid(current_visitor)

#                     if player_decision == actual_valid:
#                         score += 1
#                         feedback_text = "ВЕРНО! Документ обработан правильно."
#                         feedback_color = COLOR_GREEN_HOVER
#                     else:
#                         mistakes += 1
#                         feedback_text = "ВЫГОВОР! Нарушена инструкция КПП."
#                         feedback_color = COLOR_RED_HOVER

#                     # Проверка трех выговоров
#                     if mistakes >= 3:
#                         game_over = True
#                     else:
#                         current_visitor = generate_visitor()

#     # ЭТАП 2. Отрисовка интерфейса
#     screen.fill(COLOR_BG)

#     # Статистика
#     score_surf = font_hud.render(
#         f"Одобрено верно: {score}", True, COLOR_TEXT_LIGHT
#     )
#     mistakes_surf = font_hud.render(
#         f"Выговоры: {mistakes} / 3", True,
#         COLOR_RED_HOVER if mistakes > 0 else COLOR_TEXT_LIGHT
#     )

#     screen.blit(score_surf, (30, 20))
#     screen.blit(
#         mistakes_surf,
#         (WIDTH - mistakes_surf.get_width() - 30, 20)
#     )

#     # Правило дня
#     rule_rect = pygame.Rect(60, 65, WIDTH - 120, 65)
#     pygame.draw.rect(screen, COLOR_RULE_BG, rule_rect, border_radius=8)
#     pygame.draw.rect(
#         screen, (90, 95, 110), rule_rect, width=2, border_radius=8
#     )

#     rule_surf = font_title.render(
#         "ГОД = 2026, КОД >= 400, ГОСТЬ = ЗАПРЕЩЕН",
#         True, (255, 220, 100)
#     )
#     screen.blit(rule_surf, rule_surf.get_rect(center=rule_rect.center))

#     # Карточка посетителя
#     pygame.draw.rect(screen, COLOR_CARD, card_rect, border_radius=10)
#     pygame.draw.rect(
#         screen, COLOR_CARD_BORDER, card_rect,
#         width=4, border_radius=10
#     )

#     doc_header = font_title.render(
#         "ПРОПУСК НА ТЕРРИТОРИЮ", True, COLOR_INK
#     )
#     screen.blit(doc_header, (card_rect.x + 25, card_rect.y + 20))

#     pygame.draw.line(
#         screen, COLOR_CARD_BORDER,
#         (card_rect.x + 20, card_rect.y + 55),
#         (card_rect.right - 20, card_rect.y + 55), 2
#     )

#     # Поля документа
#     lines = [
#         f"ФИО:       {current_visitor['name']}",
#         f"ДОЛЖНОСТЬ: {current_visitor['role']}",
#         f"ГОД ВЫД.:  {current_visitor['year']}",
#         f"КОД ДОСТ.: {current_visitor['code']}",
#     ]

#     for i, line in enumerate(lines):
#         line_surf = font_card.render(line, True, COLOR_INK)
#         screen.blit(
#             line_surf,
#             (card_rect.x + 25, card_rect.y + 75 + i * 36)
#         )

#     # Статус последнего решения
#     fb_surf = font_hud.render(feedback_text, True, feedback_color)
#     screen.blit(
#         fb_surf,
#         fb_surf.get_rect(center=(WIDTH // 2, 418))
#     )

#     # Кнопки
#     is_hover_approve = approve_btn.collidepoint(mouse_pos)
#     is_hover_deny = deny_btn.collidepoint(mouse_pos)

#     pygame.draw.rect(
#         screen,
#         COLOR_GREEN_HOVER if is_hover_approve else COLOR_GREEN,
#         approve_btn, border_radius=10
#     )

#     pygame.draw.rect(
#         screen,
#         COLOR_RED_HOVER if is_hover_deny else COLOR_RED,
#         deny_btn, border_radius=10
#     )

#     if is_hover_approve and not game_over:
#         pygame.draw.rect(
#             screen, COLOR_TEXT_LIGHT, approve_btn,
#             width=3, border_radius=10
#         )

#     if is_hover_deny and not game_over:
#         pygame.draw.rect(
#             screen, COLOR_TEXT_LIGHT, deny_btn,
#             width=3, border_radius=10
#         )

#     app_text = font_btn.render("ОДОБРИТЬ", True, COLOR_TEXT_LIGHT)
#     deny_text = font_btn.render("ОТКАЗАТЬ", True, COLOR_TEXT_LIGHT)

#     screen.blit(app_text, app_text.get_rect(center=approve_btn.center))
#     screen.blit(deny_text, deny_text.get_rect(center=deny_btn.center))

#     # ЭТАП 3. Экран увольнения
#     if game_over:
#         overlay = pygame.Surface((WIDTH, HEIGHT))
#         overlay.set_alpha(210)
#         overlay.fill((0, 0, 0))
#         screen.blit(overlay, (0, 0))

#         game_over_text = font_game_over.render(
#             "ВЫ УВОЛЕНЫ!", True, COLOR_RED_HOVER
#         )
#         restart_text = font_restart.render(
#             "Нажмите R для новой смены",
#             True, COLOR_TEXT_LIGHT
#         )

#         screen.blit(
#             game_over_text,
#             game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
#         )
#         screen.blit(
#             restart_text,
#             restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 35))
#         )

#     pygame.display.flip()
#     clock.tick(FPS)

# pygame.quit()
# sys.exit()

