import sys
import pygame
import dataManagement as aa
import gameStartOver as dd
db = aa.dbMgr()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    font = pygame.font.SysFont('simhei', 15, True)
    input_box = pygame.Rect(100, 100, 200, 15)
    pygame.display.set_caption("滑雪游戏")
    # 加载图片
    image1 = pygame.image.load('resources/images/jinru.jpg')
    image1_rect = image1.get_rect()
    image1_rect.center = (85, 250)
    image2 = pygame.image.load('resources/images/zhuce.jpg')
    image2_rect = image2.get_rect()
    image2_rect.center = (310, 250)
    image3 = pygame.image.load('resources/images/denglu.jpg')
    image3_rect = image3.get_rect()
    image3_rect.center = (200, 50)
    # 输入文本框变量
    username_box = pygame.Rect(100, 100, 160, 25)
    password_box = pygame.Rect(100, 150, 160, 25)
    color_inactive = (0, 0, 0)
    color_active = (200, 200, 200)
    color = color_inactive
    active = None
    # 文本
    username_text = ''
    password_text = ''
    password_mask = ''
    # 状态
    a = False   # 账户或密码错误状态
    b = False   # 注册成功状态
    c = False   # 注册错误状态
    while True:
        screen.fill((250, 250, 250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 检查是否点击了输入框或按钮
            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_box.collidepoint(event.pos):
                    active = 'username'
                    a = b = c = False
                elif password_box.collidepoint(event.pos):
                    active = 'password'
                    a = b = c = False
                elif image1_rect.collidepoint(event.pos):
                    # 登录
                    # 账户和密码对了

                    if db.selectFromUsers(username_text, password_text):
                        dd.startGame(username_text)
                        pygame.display.flip()
                    # 错误
                    else:
                        username_text = ''
                        password_text = ''
                        password_mask = ''
                        a = True
                # 注册
                elif image2_rect.collidepoint(event.pos):
                    if db.regester(username_text, password_text):
                        b = True
                        username_text = ''
                        password_text = ''
                        password_mask = ''
                    else:
                        c = True
                        username_text = ''
                        password_text = ''
                        password_mask = ''
                else:
                    active = None
            # 输入用户名和密码
            if event.type == pygame.KEYDOWN:
                if active == 'username':
                    if event.key == pygame.K_RETURN:
                        active = 'password'
                    elif event.key == pygame.K_BACKSPACE:
                        username_text = username_text[:-1]
                    else:
                        username_text += event.unicode
                elif active == 'password':
                    if event.key == pygame.K_RETURN:
                        print(f'username:{username_text},password:{password_text}')
                    elif event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    else:
                        password_text += event.unicode
        password_mask = '*' * len(password_text)
        if a:
            text3 = font.render('账户或密码错误，请重新输入', True, (255, 0, 0))
            screen.blit(text3, (90, 180))
        if b:
            text4 = font.render('注册成功', True, (0, 255, 0))
            screen.blit(text4, (90, 180))
        if c:
            text4 = font.render('注册失败，请稍后重试', True, (255, 0, 0))
            screen.blit(text4, (90, 180))
        # 绘制输入
        text1 = font.render('账户', True, (0, 0, 0))
        text3 = font.render('账户', True, (0, 0, 0))
        text2 = font.render('密码', True, (0, 0, 0))
        screen.blit(text1, (60, 106))
        screen.blit(text2, (60, 156))
        txt_surface_username = font.render(username_text, True, color)
        txt_surface_password = font.render(password_mask, True, color)
        screen.blit(txt_surface_username, (username_box.x + 5, username_box.y + 5))
        screen.blit(txt_surface_password, (password_box.x + 5, password_box.y + 5))
        pygame.draw.rect(screen, color_active if active == 'username' else color_inactive, username_box, 2)
        pygame.draw.rect(screen, color_active if active == 'password' else color_inactive, password_box, 2)
        # 按钮
        screen.blit(image1, image1_rect)
        screen.blit(image2, image2_rect)
        screen.blit(image3, image3_rect)
        pygame.display.flip()