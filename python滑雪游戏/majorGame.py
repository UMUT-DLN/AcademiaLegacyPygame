import sys
import random
import pygame

from SkiGame.gameStartOver import gameover


class Skier(pygame.sprite.Sprite):
    def __init__(self, position):
        # 初始化
        pygame.sprite.Sprite.__init__(self)
        # 加载图片
        self.skiers = [pygame.image.load('resources/images/skier_forward.png'),
                       pygame.image.load('resources/images/skier_fall.png'),
                       pygame.image.load('resources/images/skier_left1.png'),
                       pygame.image.load('resources/images/skier_left2.png'),
                       pygame.image.load('resources/images/skier_right1.png'),
                       pygame.image.load('resources/images/skier_right2.png')]
        self.image = self.skiers[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y = position
        # 方向属性
        self.right = False
        self.left = False
        # 撞到属性
        self.collide = False
        # 速度属性
        self.speed = 5
        # 方向步数
        self.walkCount = 0

    def behavior(self):
        # 提取键盘上的跳跃按钮
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.x + 18 < 800:
            self.right = True
            self.left = False
            self.x += self.speed
        elif keys[pygame.K_LEFT] and self.x - 18 > 0:
            self.left = True
            self.right = False
            self.x -= self.speed
        else:
            self.right = False
            self.left = False

    def drawScreen(self, screen, Trees):
        self.rect.center = [self.x, self.y]
        if self.collide:
            screen.blit(self.skiers[1], self.rect)
        elif self.right:
            if self.walkCount < 20:
                self.walkCount += 1
                screen.blit(self.skiers[4], self.rect)
            else:
                screen.blit(self.skiers[5], self.rect)
        elif self.left:
            if self.walkCount < 20:
                self.walkCount += 1
                screen.blit(self.skiers[2], self.rect)
            else:
                screen.blit(self.skiers[3], self.rect)

        else:
            self.walkCount = 0
            screen.blit(self.skiers[0], self.rect)


class Tree(pygame.sprite.Sprite):
    def __init__(self, position):
        # 初始化
        pygame.sprite.Sprite.__init__(self)
        # 障碍物照片
        self.image = pygame.image.load('resources/images/tree.png')
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y = position
        # 移动速度
        self.speed = 5

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y
        if self.y + 10 < 0:
            self.kill()


class Banner(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/images/flag.png')
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y = position
        # 移动速度
        self.speed = 5

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y
        if self.y + 10 < 0:
            self.kill()


def main(username):
    pygame.init()
    size = width, height = (800, 533)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("滑雪游戏")
    # 字样
    font = pygame.font.SysFont('simhei', 25 ,True)
    # 帧率
    clock = pygame.time.Clock()
    # 音频
    pygame.mixer.init()
    pygame.mixer.music.load('resources/music/angelsbymyside.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    # 构造角色
    skier = Skier((340, 100))
    # 碰撞状态
    collide1 = False
    collide_wolk1 = 0
    # 精灵组
    Tree_sprite_group = pygame.sprite.Group()
    banner_sprite_group = pygame.sprite.Group()
    for _ in range(20):
        change = random.randint(0, 2)
        if change == 0:
            x = random.randint(0, 790)
            y = random.randint(533, 1200)
            Tree_sprite_group.add(Tree((x, y)))
        elif change == 1:
            x = random.randint(0, 790)
            y = random.randint(533, 1000)
            banner_sprite_group.add(Banner((x, y)))
    # 分数
    score = 0
    heightScore = 0
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # 更新精灵组
        if collide1:
            if collide_wolk1 < 50:
                collide_wolk1 += 1
            else:
                collide1 = False
                collide_wolk1 = 0
        if collide_wolk1 > 20 or collide1 == False:
            skier.collide = False
            skier.behavior()
            Tree_sprite_group.update()
            banner_sprite_group.update()
        Tree_sprite_group.draw(screen)
        banner_sprite_group.draw(screen)
        # 更新角色行为
        # skier.behavior()
        skier.drawScreen(screen, Tree_sprite_group)

        if len(Tree_sprite_group) < 10:
            x = random.randint(0, 790)
            y = 650
            Tree_sprite_group.add(Tree((x, y)))
        if len(banner_sprite_group) < 10:
            x = random.randint(0, 790)
            y = 650
            banner_sprite_group.add(Banner((x, y)))
        # 分数
        if score > heightScore:
            heightScore = score
        # 碰撞检测
        # 旗帜的碰撞
        if pygame.sprite.spritecollide(skier, banner_sprite_group, True):
            score += 5
        # 数目的碰撞
        if collide_wolk1 < 1:
            if pygame.sprite.spritecollide(skier, Tree_sprite_group, False):
                if score > 20:
                    score -= 20
                else:
                    score = 0
                    gameover(username, heightScore)
                skier.collide = True
                collide1 = True
        text = font.render(f'分数:{score}', True, (0, 0, 0))
        screen.blit(text, (20, 10))
        pygame.display.flip()  # 更新整个屏幕
        clock.tick(60)  # 控制
