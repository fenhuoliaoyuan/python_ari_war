from plane_sprites import *

class PlanGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("游戏初始化")
        # 1.创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)  # 矩形对象的size属性就是元组
        # 2.创建游戏的时钟
        self.clock = pygame.time.Clock()
        # 3.调用私方法，精灵和精灵组的创建
        self._create_sprites()
        # 4.设置定时器事件-创建敌机 1s
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)  # ms
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)  # ms

    def _create_sprites(self):
        bg1 = Background()
        bg2 = Background(is_alt=True)
        # bg2.rect.y = -bg2.rect.height
        # self.back_group = pygame.sprite.Group(bg1)
        self.back_group = pygame.sprite.Group(bg1, bg2)
        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()
        # 创建英雄的精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        print("游戏开始")
        while True:
            # 1.可以指定循环体内部的代码执行的频率
            self.clock.tick(FRAMe_PER_SEC)
            # 2.事件监听
            self._event_handler()
            # 3.碰撞检测
            self._check_collide()
            # 4.更新/绘制精灵组
            self._update_sprites()
            # 5.更新显示
            pygame.display.update()

    def _event_handler(self):
        for event in pygame.event.get():
            # 判断事件类型是否是退出事件
            if event.type == pygame.QUIT:
                PlanGame._game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                print("敌机出场")
                # 创建敌机精灵
                enemy = Enemy()
                self.enemy_group.add(enemy)
            # elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            #     print("向右移动")
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
        # 使用键盘提供的方法获取键盘按键
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值1
        if keys_pressed[pygame.K_RIGHT]:
            # print("向右移动....")
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def _check_collide(self):
        # 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        # 敌机撞毁英雄
        enemys_list = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemys_list) > 0:
            # 让英雄牺牲
            self.hero.kill()
            # 结束游戏
            PlanGame._game_over()

    def _update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def _game_over():
        print("游戏结束")
        pygame.quit()
        exit()


if __name__ == '__main__':
    # 创建游戏对象
    game = PlanGame()
    # 启动游戏
    game.start_game()
