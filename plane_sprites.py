import random

import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 720)
# 刷新的帧率
FRAMe_PER_SEC = 60
# 定义定时器事件常量 敌机
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 定义发射子弹事件常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=1):
        # 调用父类的初始化方法
        super().__init__()
        # 定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 在屏幕的垂直方向上移动
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):
        super().__init__("./images/background.png")
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        super().update()
        # 判断是否移出屏幕，将图像设置到屏幕上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self):
        super().__init__("./images/enemy1.png")
        # 指定敌机的初始随机速度
        self.speed = random.randint(1, 3)
        # 指定敌机的初始随机位置
        self.rect.bottom = 0  # y = bottom-height
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            # print("飞出屏幕，需要从精灵组删除...")
            # kill方法可以将精灵从所以精灵组中移出，在内存中删除
            self.kill()

    def __del__(self):
        # print("敌机挂了%s"%self.rect)
        pass


class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self):
        # 调用父类方法，设置图片和speed
        super().__init__("./images/me1.png", 0)
        # 设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        # 英雄在水平方向移动
        self.rect.x += self.speed
        # 控制英雄不能离开屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        print("发射子弹...")
        for i in (0,1,2):
            # 创建子弹精灵
            bullet = Bullet()
            # 设置精灵的位置
            bullet.rect.bottom = self.rect.y - 20*i
            bullet.rect.centerx = self.rect.centerx
            # 将精灵添加到精灵组
            self.bullets.add(bullet)


class Bullet(GameSprite):
    def __init__(self):
        # 调用父类初始方法，设置图片速度
        super().__init__("./images/bullet1.png", -2)

    def update(self):
        # 调用父类方法，让子弹垂直飞行
        super().update()
        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        print("子弹被销毁")
