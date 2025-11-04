import os
import pygame
import random
import sys
import pygame as pg

# 初期化
pygame.init()
WIDTH, HEIGHT = 800, 600
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.display.set_caption("射的ゲーム - ベース版")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)


# スコア
score = 0
mato_num = 10

class Mato:
    """
    的に関するクラス
    """
    img = pg.transform.scale(pg.image.load("fig/1.png").convert_alpha(), (100, 100))
    used_positions = set()

    def __init__(self, radius):
        """
        的を生成するための関数
        引数：的の半径
        visible:的に命中した際に表示を切り替えるためのもの
        """
        self.radius = radius
        self.cols = 8  # 横方向分割
        self.rows = 6  # 縦方向分割
        cell_w = WIDTH // self.cols
        cell_h = HEIGHT // self.rows

        # 使用可能な範囲
        available_positions = [
            (col, row)
            for col in range(self.cols)
            for row in range(1, self.rows)  # ← ここがポイント
            if (col, row) not in Mato.used_positions
        ]

        # もしすべて埋まっていたらリセット
        if not available_positions:
            Mato.used_positions.clear()
            available_positions = [
                (col, row)
                for col in range(self.cols)
                for row in range(1, self.rows)
            ]

        col, row = random.choice(available_positions)
        Mato.used_positions.add((col, row))

        self.x = col * cell_w + cell_w // 2
        self.y = row * cell_h + cell_h // 2

        self.last_update = pygame.time.get_ticks()
        self.visible = True

    def update(self):
        """
        一定時間経過したら新しい位置に移動するための関数
        """
        now = pygame.time.get_ticks()
        broke_time = now - self.last_update
        if  broke_time >= 3000:
            self.visible = True
            self.last_update = now

            cell_w = WIDTH // self.cols
            cell_h = HEIGHT // self.rows

            available_positions = [
                (col, row)
                for col in range(self.cols)
                for row in range(1, self.rows)
                if (col, row) not in Mato.used_positions
            ]

            if not available_positions:
                Mato.used_positions.clear()
                available_positions = [
                    (col, row)
                    for col in range(self.cols)
                    for row in range(1, self.rows)
                ]

            col, row = random.choice(available_positions)
            Mato.used_positions.add((col, row))

            self.x = col * cell_w + cell_w // 2
            self.y = row * cell_h + cell_h // 2

    def draw(self, surface):
        """
        的を描画する関数
        """
        if self.visible:
            mato_rect = Mato.img.get_rect(center=(self.x, self.y))
            surface.blit(Mato.img, mato_rect)


mato_list = [Mato(50) for _ in range(mato_num)]

running = True
while running:
    screen.fill((200, 220, 255))

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # クリックで命中判定
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for mato in mato_list:
                distance = ((mx - mato.x) ** 2 + (my - mato.y) ** 2) ** 0.5
                if distance <= mato.radius and mato.visible:
                    score += 1
                    mato.visible = False

    for mato in mato_list:
        mato.update()
        mato.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()