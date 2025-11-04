import os
import pygame
import random
import sys

# 初期化
pygame.init()
WIDTH, HEIGHT = 800, 600
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.display.set_caption("射的ゲーム - ベース版")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# 的の設定
target_radius = 30
target_x = random.randint(target_radius, WIDTH - target_radius)
target_y = random.randint(target_radius, HEIGHT - target_radius)

# スコア
score = 0


def display_score(screen:pygame.surface, font:pygame.font, current_score: int):
    if score >= 100:
        score_text = font.render(f"Score: {score}", True, (255, 215, 0))
    elif score >= 30:
        score_text = font.render(f"Score: {score}", True, (255, 255, 0))
    elif score >= 20:    
        score_text = font.render(f"Score: {score}", True, (255, 0, 0))
    elif score >= 10:
        score_text = font.render(f"Score: {score}", True, (0, 255, 0))
    else:
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

# メインループ
running = True
while running:
    screen.fill((200, 220, 255))  # 背景色（水色）

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # クリックで命中判定
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            distance = ((mx - target_x) ** 2 + (my - target_y) ** 2) ** 0.5
            if distance <= target_radius:
                score += 1
                # 的をランダムに再配置
                target_x = random.randint(target_radius, WIDTH - target_radius)
                target_y = random.randint(target_radius, HEIGHT - target_radius)

    # 的の描画
    pygame.draw.circle(screen, (255, 0, 0), (target_x, target_y), target_radius)
    pygame.draw.circle(screen, (255, 255, 255), (target_x, target_y), target_radius // 2)


    score_display = display_score(screen, font, score)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()