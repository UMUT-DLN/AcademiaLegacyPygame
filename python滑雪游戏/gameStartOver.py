import pygame
import sys
import majorGame as dd
import dataManagement as aa
db = aa.dbMgr()


# 关闭页面
def gameover(username, score):
    pygame.init()
    size = width, height = (800, 533)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("滑雪游戏")
    # 背景
    backGroud1 = pygame.image.load("resources/images/ski1.jpg").convert()
    # 字样
    font = pygame.font.SysFont('simhei', 30, True)
    # 图片
    image = pygame.image.load('resources/images/restart.png')
    image_rect = image.get_rect()
    image_rect.center = (width/2, height/2)
    # 结束图图片
    image1 = pygame.image.load('resources/images/gameover.png')
    image1_rect = image1.get_rect()
    image1_rect.center = (width/2, height/2 - 50)
    image2 = pygame.image.load('resources/images/fanhui.png')
    image2_rect = image2.get_rect()
    image2_rect.center = (15, 15)
    # 最高分数
    highScore = db.selectHighScore(username)
    while True:
        screen.blit(backGroud1, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 检查是否点击按钮
            if event.type == pygame.MOUSEBUTTONDOWN:
                if image_rect.collidepoint(event.pos):
                    dd.main(username)
                    pygame.display.flip()
                if image2_rect.collidepoint(event.pos):
                    startGame(username)
                    pygame.display.flip()
        if score > highScore:
            highScore = score
            db.commitHighScore(username, score)
        text1 = font.render(f'本局分数：{score}', True, (0, 0, 0))
        text2 = font.render(f'最高分数：{highScore}', True, (0, 0, 0))
        screen.blit(text1, (width/2 - 75, height/2 - 100))
        screen.blit(text2, (width / 2 - 75, height / 2 - 140))
        screen.blit(image, image_rect)
        screen.blit(image1, image1_rect)
        screen.blit(image2, image2_rect)
        pygame.display.flip()


# 开始页面
def startGame(username):
    pygame.init()
    size = width, height = (800, 533)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("滑雪游戏")
    # 背景
    backGroud1 = pygame.image.load("resources/images/ski1.jpg").convert()
    # 字样
    font = pygame.font.SysFont('simhei', 25, True)
    # 图片
    image = pygame.image.load('resources/images/start .png')
    image_rect = image.get_rect()
    image_rect.center = (width/2, height/2)
    # 最高分数
    highScore = db.selectHighScore(username)
    while True:
        screen.blit(backGroud1, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if image_rect.collidepoint(event.pos):
                    dd.main(username)
                    pygame.display.flip()
        text1 = font.render(f'用户名：{username}', True, (0, 0, 0))
        text2 = font.render(f'最高分数：{highScore}', True, (0, 0, 0))
        screen.blit(text1, (10, 10))
        screen.blit(text2, (10, 40))
        screen.blit(image, image_rect)
        pygame.display.flip()



