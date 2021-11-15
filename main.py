import random
import pygame
import os
# initiating pygame variables 
x = pygame.init()

# music 
pygame.mixer.init()

# game area 
screen_len = 500
screen_width = 700
gamewindow = pygame.display.set_mode((screen_width,screen_len))
pygame.display.set_caption("Sekhars snake game")
pygame.display.update()

# bgm image 
bgm = pygame.image.load("snake.png")
bgm = pygame.transform.scale(bgm, (screen_width, screen_len)).convert_alpha()

# MASTER LOOP 
# -----------------------------

def game_loop():
    # variables 
    exit_game = False
    game_over = False
    score = 0
    slen = 10
    swidth = 10
    posx = 40
    posy = 40
    fps = 30
    velx = 0
    init_velx = 10
    vely = 0 
    init_vely = 10 
    food_x = random.randint(2,screen_width-12)
    food_y = random.randint(40,screen_len-12)
    snake_list = []
    snake_len = 1

    # store high scores 
    if not os.path.exists("high_scores.txt"):
        with open("high_scores.txt", "r") as f:
            f.write(0)

    # read score file 
    with open("high_scores.txt", "r") as f:
        hscore = f.read()
        print(hscore)

    # clock for fps
    clk = pygame.time.Clock()

    # colors 
    white = (255,255,255)
    red = (255,0,0)
    black = (0,0,0)
    vio = (40, 10, 79)

    # score UI 
    font = pygame.font.SysFont(None, 52)
    def show_text(text,  color, x, y):
        screen_txt = font.render(text, True, color)
        gamewindow.blit(screen_txt, [x,y])

    def plot_snake(gamewindow , color, slist, s_size):
        for x,y in slist:
            pygame.draw.rect(gamewindow, color, [x,y,s_size,s_size])

    def wel_screen():
        exit_wel = False
        while not exit_wel:
            gamewindow.fill(white)
            show_text("Press space to play", black, 200,200)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_wel = True
                    global exit_game 
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.load("Music_bgm.mp3")
                        exit_wel = True
                        pygame.mixer.music.play()
            pygame.display.update()
            clk.tick(60)
    
    wel_screen()

    # infinite loop 
    while not exit_game:

        # Game over 
        if game_over:
            with open("high_scores.txt", "w") as f:
                f.write(str(hscore))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()
                        
            gamewindow.fill(red)
            show_text("Game Over", white, 240,200)
            show_text("High score: "+ hscore, white, 240,250)

        else:
            if score > int(hscore):
                hscore = str(score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velx = init_velx
                        vely = 0
                    if event.key == pygame.K_LEFT:
                        velx = -init_velx
                        vely = 0
                    if event.key == pygame.K_UP:
                        velx = 0
                        vely = -init_vely
                    if event.key == pygame.K_DOWN:
                        velx = 0
                        vely = init_vely
                    if event.key == pygame.K_q:
                        score += 10
                        snake_len += 1

            posx += velx
            posy += vely 

            if abs(posx-food_x) < 10 and abs(posy-food_y) < 10:
                score += 10
                snake_len += 1
                food_x = random.randint(2,screen_width-12)
                food_y = random.randint(40,screen_len-12)

            # gamewindow.fill(white)
            gamewindow.blit(bgm,(0,0))
            show_text("score: "+str(score), vio, 5 ,5 )
            show_text("highest score: "+str(hscore), vio, 250 ,5 )
            pygame.draw.rect(gamewindow,black,[posx,posy,slen, swidth])
            pygame.draw.rect(gamewindow, red ,[food_x,food_y,slen,swidth])

            # portions apart from head 
            shead = []
            shead.append(posx)
            shead.append(posy)
            snake_list.append(shead)
            if len(snake_list)>snake_len:
                del snake_list[0]
                
            # -- crash with itself --  
            if shead in snake_list[:-1]:
                game_over = True

            # game over 
            if posx>screen_width-10 or posx<0 or posy>screen_len-10 or posy<38:
                game_over = True

            plot_snake(gamewindow, black, snake_list, slen)
        
        # fixed for any condition 
        pygame.display.update()
        clk.tick(fps)

# ------------------------------

game_loop()

# exit 
pygame.quit()
quit()

