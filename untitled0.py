################################### 게임의 기본 틀 출처 ###########################################
######                           [Python pygame Game] 4 Beats                                #####
######                               made by "PrintedLove"                                   #####    
######                           https://printed.tistory.com/                                #####
###### This game was created with reference to ParkJuneWoo(korca0220)'s [Finding-the-Rabbit] #####
##################################################################################################


import pandas as pd
import pygame as pg
import os, time, random
import tkinter.messagebox as messagebox

TITLE = "Moon Beats"       ### default setting
WIDTH = 640
HEIGHT = 480
FPS = 60
DEFAULT_FONT = "NotoSansCJKkr-Regular.otf"

WHITE = (238, 238, 238)     ### color setting
BLACK = (32, 36, 32)
RED = (246, 36, 74)
BLUE = (32, 105, 246)
ALPHA_MAX = 255
new_pref = []
num = 0
new_data = pd.DataFrame()
prefer_data = pd.DataFrame()

class Game:
    def __init__(self): ########################## Game Start
        pg.init()
        pg.mixer.init()     #sound mixer
        pg.display.set_caption(TITLE)       #title name
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))      #screen size
        self.screen_mode = 0    #screen mode (0: logo, 1: logo2, 2: main, 3: stage select, 4: play, 5: score)
        self.screen_value = [-ALPHA_MAX, 0, 0, 0]       #screen management value
        self.clock = pg.time.Clock()        #FPS timer
        self.start_tick = 0     #game timer
        self.running = True     #game initialize Boolean value
        self.language_mode = 1         #0: english, 1: korean, 2~: custom
        self.song_select = 1    #select song
        self.load_date()        #data loading
        self.new()
        pg.mixer.music.load(self.bg_main)       #bgm

    def load_date(self): ########################## Data Loading
        self.dir = os.path.dirname(__file__)
        
        ### font
        self.fnt_dir = os.path.join(self.dir, 'font')
        self.gameFont = os.path.join(self.fnt_dir, DEFAULT_FONT)
        self.csv_dir = os.path.join(self.dir, 'song')
        
        with open(os.path.join(self.fnt_dir, 'language.ini'), "r", encoding = 'UTF-8') as language_file:
            language_lists = language_file.read().split('\n')
            
        self.language_list = [n.split("_") for n in language_lists]

        #with open(os.path.join(self.csv_dir, 'moonbeat_music_preference.csv'), "r", encoding = 'UTF-8') as csv_file:
        #    csv_lists = csv_file.read().split(',')
            
        #self.csv_list = [n.split(",") for n in csv_lists]

        
        ### image
        self.img_dir = os.path.join(self.dir, 'image')
        pg.display.set_icon(pg.image.load(os.path.join(self.img_dir, 'icon.png')))      #set icon
        self.spr_printed = pg.image.load(os.path.join(self.img_dir, 'printed.png'))
        self.spr_logoback = pg.image.load(os.path.join(self.img_dir, 'logoback.png'))
        self.spr_logo = pg.image.load(os.path.join(self.img_dir, 'logo.png'))
        self.spr_circle = pg.image.load(os.path.join(self.img_dir, 'circle.png'))
        self.spr_shot = Spritesheet(os.path.join(self.img_dir, 'shot.png'))
        self.spr_selctback = pg.image.load(os.path.join(self.img_dir, 'selctback.png'))
        self.spr_playback = pg.image.load(os.path.join(self.img_dir, 'playback.png'))
        self.spr_resultback = pg.image.load(os.path.join(self.img_dir, 'resultback.png'))
        
        ### sound
        self.snd_dir = os.path.join(self.dir, 'sound')
        self.bg_main = os.path.join(self.snd_dir, 'bg_main.ogg')
        self.sound_click = pg.mixer.Sound(os.path.join(self.snd_dir, 'click.ogg'))
        self.sound_drum1 = pg.mixer.Sound(os.path.join(self.snd_dir, 'drum1.ogg'))
        self.sound_drum2 = pg.mixer.Sound(os.path.join(self.snd_dir, 'drum2.ogg'))
        self.sound_drum3 = pg.mixer.Sound(os.path.join(self.snd_dir, 'drum3.ogg'))
        self.sound_drum4 = pg.mixer.Sound(os.path.join(self.snd_dir, 'drum4.ogg'))

        ### song
        global song_lists
        self.sng_dir = os.path.join(self.dir, 'song')
        music_type = ["ogg", "mp3", "wav"]
        song_lists = [i for i in os.listdir(self.sng_dir) if i.split('.')[-1] in music_type]
        self.song_list = list()         # song name list
        self.song_path = list()         # song path list
        
        for song in song_lists:
            try:
                pg.mixer.music.load(os.path.join(self.sng_dir, song))
                self.song_list.append(song.split('.')[0])
                self.song_path.append(os.path.join(self.sng_dir, song))
            except:
                print("error: " + str(song) + "is unsupported format music file.")
        
        self.song_num = len(self.song_list)     # available song number
        self.song_dataPath = list()                 # song data file path list
        self.song_highScore = list()            # song highscore list
        self.song_perfectScore = list()            # song maxscore list
        
        for song in self.song_list:
            song_dataCoord = os.path.join(self.sng_dir, song + ".ini")

            try:
                with open(song_dataCoord, "r", encoding = 'UTF-8') as song_file:
                    song_scoreList = song_file.read().split('\n')[0]
                    
                self.song_highScore.append(int(song_scoreList.split(':')[1]))
                self.song_perfectScore.append(int(song_scoreList.split(':')[2]))
                self.song_dataPath.append(song_dataCoord) 
            except:
                print("error: " + str(song) + "'s song data file is damaged or does not exist.")
                self.song_highScore.append(-1)
                self.song_perfectScore.append(-1)
                self.song_dataPath.append(-1) 

    def new(self):      ########################## Game Initialize
        self.song_data = list()     #song data list
        self.song_dataLen = 0       #song data len
        self.song_dataIndex = 0     #song data index
        self.circle_dir = 1     #circle direction value (benchmark: white / down, right, up, left  == 1, 2, 3, 4)
        self.circle_rot = 0     #circle rotation value
        self.score = 0          #current game score
        self.all_sprites = pg.sprite.Group()        #sprite group
        self.shots = pg.sprite.Group()
        
    def run(self):      ########################## Game Loop
        self.playing = True
        
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            pg.display.flip()

        pg.mixer.music.fadeout(600)
    
    def update(self):   ########################## Game Loop - Update
        self.all_sprites.update()       #screen update
        self.game_tick = pg.time.get_ticks() - self.start_tick      #play time calculation
        
    def events(self):   ########################## Game Loop - Events
        mouse_coord = pg.mouse.get_pos()    #mouse coord value
        mouse_move = False      #mouse move Boolean value
        mouse_click = 0         #mouse click value (1: left, 2: scroll, 3: right, 4: scroll up, 5: scroll down)
        key_click = 0           #key value (275: right, 276: left, 273: up, 274: down, 13: enter)
        
        for event in pg.event.get():                        ### Event Check
            if event.type == pg.QUIT:       #exit
                if self.playing:
                    self.playing, self.running = False, False 
            elif event.type == pg.KEYDOWN:      #keyboard check
                key_click = event.key

                if self.screen_mode < 4:
                    self.sound_click.play()
            elif event.type == pg.MOUSEMOTION:
                if event.rel[0] != 0 or event.rel[1] != 0:    #mousemove
                    mouse_move = True
            elif event.type == pg.MOUSEBUTTONDOWN:      #mouse click
                mouse_click = event.button

                if self.screen_mode < 4:
                    self.sound_click.play()
        
        if self.screen_mode == 0:           ### Logo Screen1
            self.screen_value[0] += ALPHA_MAX / 51

            if self.screen_value[0] == ALPHA_MAX:
                self.screen_value[0] = 0
                self.screen_mode = 1
                pg.mixer.music.play(loops = -1)
        elif self.screen_mode == 1:             ### Logo Screen2          
            if self.screen_value[3] == 0:
                if self.screen_value[0] < ALPHA_MAX:
                    self.screen_value[0] += ALPHA_MAX / 51
                else:
                    if mouse_click == 1 or key_click != 0:
                        self.screen_value[3] = 1
            else:
                if self.screen_value[0] > 0:
                    self.screen_value[0] -= ALPHA_MAX / 15
                else:
                    self.screen_mode = 2
                    self.screen_value[1] = 2
                    self.screen_value[2] = 0
                    self.screen_value[3] = 0

            if self.screen_value[1] > -10:
                self.screen_value[1] -= 1
            else:
                if self.screen_value[2] == 0:
                    self.screen_value[1] = random.randrange(0, 10)
                    self.screen_value[2] = random.randrange(5, 30)
                else:
                    self.screen_value[2] -= 1       
        elif self.screen_mode == 2:                     ### Main Screen
            if self.screen_value[2] == 0:
                if self.screen_value[0] < ALPHA_MAX:
                    self.screen_value[0] += ALPHA_MAX / 15

                    if self.screen_value[3] > 0:
                        self.screen_value[3] -= ALPHA_MAX / 15
                else:
                    for i in range(4):
                        if mouse_move and 400 < mouse_coord[0] < 560 and 105 + i*70 < mouse_coord[1] < 155 + i*70:      #mouse cursor check
                            self.screen_value[1] = i + 1

                    if (key_click == 273 or mouse_click == 4) and self.screen_value[1] > 1:     #key up check
                        self.screen_value[1] -= 1
                    elif (key_click == 274 or mouse_click == 5) and self.screen_value[1] < 4:   #key down check
                        self.screen_value[1] += 1
                        
                    if (mouse_click == 1 or key_click == 13 or key_click == 275):      #click or key enter, key right check
                        if self.screen_value[1] == 1:       #START
                            self.screen_value[2] = 1
                        elif self.screen_value[1] == 2:     #HELP
                            self.screen_value[0] = ALPHA_MAX / 3
                            self.screen_value[2] = 2
                        elif self.screen_value[1] == 3:     #EXIT
                            self.screen_value[2] = 3
                        else:                               #Languague
                            self.language_mode = self.language_mode + 1 if self.language_mode < len(self.language_list) - 1 else 0
                            self.gameFont = os.path.join(self.fnt_dir, self.load_language(1))
            elif self.screen_value[2] == 1:
                if self.screen_value[0] > 0:
                    self.screen_value[0] -= ALPHA_MAX / 15
                else:
                    self.screen_mode = 3
                    self.screen_value[1] = 0
                    self.screen_value[2] = 0
                    
                    if self.song_highScore[self.song_select - 1] == -1:
                        pg.mixer.music.fadeout(600)
                    else:
                        pg.mixer.music.load(self.song_path[self.song_select - 1])
                        pg.mixer.music.play(loops = -1)
            elif self.screen_value[2] == 2:
                if mouse_click == 1 or key_click != 0:
                    self.screen_value[2] = 0
            elif self.screen_value[2] == 3:
                if self.screen_value[0] > 0:
                    self.screen_value[0] -= ALPHA_MAX / 15
                else:
                    self.playing, self.running = False, False
        elif self.screen_mode == 3:                     ### Song Select Screen
            if self.screen_value[2] == 0:
                if self.screen_value[0] < ALPHA_MAX:
                    self.screen_value[0] += ALPHA_MAX / 15

                self.screen_value[1] = 0
                songChange = False

                if round(0.31 * WIDTH - 75) < mouse_coord[0] < round(0.31 * WIDTH + 75):        #mouse coord check
                    if round(0.125 * HEIGHT + 30) > mouse_coord[1]:
                        self.screen_value[1] = 1
                    elif round(0.875 * HEIGHT - 30) < mouse_coord[1]:
                        self.screen_value[1] = 2
                elif round(0.69 * WIDTH - 75) < mouse_coord[0] < round(0.69 * WIDTH + 75) and round(HEIGHT / 2 + 25) < mouse_coord[1] < round(HEIGHT / 2 + 65):
                    self.screen_value[1] = 3
                elif round(0.73 * WIDTH - 75) < mouse_coord[0] < round(0.73 * WIDTH + 75) and round(HEIGHT / 2 + 85) < mouse_coord[1] < round(HEIGHT / 2 + 125):
                    self.screen_value[1] = 4
                
                if (mouse_click == 1):              #mouse clickcheck
                    if self.screen_value[1] == 1:
                        if self.song_select > 1:
                            self.song_select -= 1
                            songChange = True
                    elif self.screen_value[1] == 2:
                        if self.song_select < self.song_num:
                            self.song_select += 1
                            songChange = True
                    elif self.screen_value[1] == 3:
                        if self.song_highScore[self.song_select - 1] != -1:
                            self.screen_value[2] = 1
                    elif self.screen_value[1] == 4:
                        self.screen_value[2] = 2
                elif key_click == 273 or mouse_click == 4:     #key check
                    if self.song_select > 1:
                        self.song_select -= 1
                        songChange = True
                elif key_click == 274 or mouse_click == 5:
                    if self.song_select < self.song_num:
                        self.song_select += 1
                        songChange = True
                elif key_click == 275 or key_click == 13: 
                    if self.song_highScore[self.song_select - 1] != -1:
                        self.screen_value[2] = 1
                elif key_click == 276:
                    self.screen_value[2] = 2

                if songChange:
                    if self.song_highScore[self.song_select - 1] == -1:
                        pg.mixer.music.fadeout(600)
                    else:
                        pg.mixer.music.load(self.song_path[self.song_select - 1])
                        pg.mixer.music.play(loops = -1)
            else:
                if self.screen_value[0] > 0:
                    self.screen_value[0] -= ALPHA_MAX / 15
                else:
                    if self.screen_value[2] == 1:
                        self.screen_mode = 4
                        self.screen_value[1] = 0
                        self.screen_value[2] = 0
                        self.start_tick = pg.time.get_ticks()
                        self.load_songData()
                    else:
                        self.screen_mode = 2
                        self.screen_value[1] = 0
                        self.screen_value[2] = 0
                        self.screen_value[3] = ALPHA_MAX
                        pg.mixer.music.load(self.bg_main)
                        pg.mixer.music.play(loops = -1)
        elif self.screen_mode == 4:                             ### Play Screen
            if self.screen_value[1] == 0:
                if self.screen_value[0] < ALPHA_MAX:
                    self.screen_value[0] += ALPHA_MAX / 15
                
                if (mouse_click == 1):              #mouse clickcheck
                    if mouse_coord[0] < WIDTH / 2:
                        self.circle_dir += 1
                    else:
                        self.circle_dir -= 1
                elif key_click == 276:              #key check
                    self.circle_dir += 1
                elif key_click == 275:
                    self.circle_dir -= 1

                if self.circle_dir > 4:         #circle direction management
                    self.circle_dir = 1
                elif self.circle_dir < 1:
                    self.circle_dir = 4

                rotToDir = (self.circle_dir - 1) * 90       #circle rotation management
                
                if self.circle_rot != rotToDir:
                    if self.circle_rot >= rotToDir:
                        if self.circle_rot >= 270 and rotToDir == 0:
                            self.circle_rot += 15
                        else:
                            self.circle_rot -= 15
                    else:
                        if self.circle_rot == 0 and rotToDir == 270:
                            self.circle_rot = 345
                        else:
                            self.circle_rot += 15
                        
                if self.circle_rot < 0:         
                    self.circle_rot = 345
                elif self.circle_rot > 345:
                    self.circle_rot = 0

                self.create_shot()          #create shot
            else:
                if self.screen_value[0] > 0:
                    self.screen_value[0] -= ALPHA_MAX / 85
                else:
                    self.screen_mode = 5
                    self.screen_value[1] = 0
        else:                             ### Score Screen
            if self.screen_value[1] == 0:
                if self.screen_value[0] < ALPHA_MAX:
                    self.screen_value[0] += ALPHA_MAX / 15
                    
                if mouse_move:
                    if round(WIDTH / 2 - 160) < mouse_coord[0] < round(WIDTH / 2 - 40) and round(HEIGHT / 2 + 110) < mouse_coord[1] < round(HEIGHT / 2 + 170):
                        self.screen_value[2] = 1
                    elif round(WIDTH / 2 + 40) < mouse_coord[0] < round(WIDTH / 2 + 160) and round(HEIGHT / 2 + 110) < mouse_coord[1] < round(HEIGHT / 2 + 170):
                        self.screen_value[2] = 2

                if (mouse_click == 1):              #mouse clickcheck
                    self.screen_value[1] = self.screen_value[2]
                elif key_click == 276 or mouse_click == 4:     #key check
                    self.screen_value[2] = 1
                elif key_click == 275 or mouse_click == 5:
                    self.screen_value[2] = 2
                elif key_click == 13: 
                    self.screen_value[1] = self.screen_value[2]
            else:
                if self.screen_value[0] > 0:
                    self.screen_value[0] -= ALPHA_MAX / 15
                else:
                    self.new()
                    
                    if self.screen_value[1] == 1:
                        self.screen_mode = 3
                    else:
                        self.screen_mode = 4
                        self.start_tick = pg.time.get_ticks()
                        self.load_songData()

                    self.screen_value[1] = 0
                    self.screen_value[2] = 0
                        
    def draw(self):     ########################## Game Loop - Draw
        self.background = pg.Surface((WIDTH, HEIGHT))           #white background
        self.background = self.background.convert()
        self.background.fill(WHITE)
        self.screen.blit(self.background, (0,0))
        self.draw_screen()                      #draw screen
        self.all_sprites.draw(self.screen)
        pg.display.update()

    def draw_screen(self):                    # Draw Screen
        screen_alpha = self.screen_value[0]
        
        if self.screen_mode == 0:       #logo screen1
            screen_alpha = ALPHA_MAX - min(max(self.screen_value[0], 0), ALPHA_MAX)
            self.draw_sprite(((WIDTH - 454) / 2, (HEIGHT - 79) / 2), self.spr_printed, screen_alpha)
        elif self.screen_mode == 1:     #logo screen2
            self.spr_logoback.set_alpha(screen_alpha) if self.screen_value[3] == 0 else self.spr_logoback.set_alpha(ALPHA_MAX)
            self.screen.blit(self.spr_logoback, (0, 0))
            spr_logoRescale = pg.transform.scale(self.spr_logo, (301 + self.screen_value[1], 306 + self.screen_value[1]))
            self.draw_sprite(((WIDTH - self.screen_value[1]) / 2, 40 - self.screen_value[1] / 2), spr_logoRescale, screen_alpha)
        elif self.screen_mode == 2:     #main screen
            select_index = [True if self.screen_value[1] == i + 1 else False for i in range(4)]
            
            if self.screen_value[2] == 0:
                self.draw_sprite((0, 0), self.spr_logoback, ALPHA_MAX - self.screen_value[3])
            else:
                self.spr_logoback.set_alpha(screen_alpha)
                logoback_coord = 0 if self.screen_value[2] == 2 else round((screen_alpha - ALPHA_MAX) / 10)
                self.screen.blit(self.spr_logoback, (logoback_coord, 0))
                
            if self.screen_value[2] == 2:
                import pygame
                import os
                import pandas as pd
                import numpy as np
                from scipy.cluster import hierarchy
                import tkinter as tk
                from tkinter import ttk


                # Pygame 초기화
                pygame.mixer.init()

                # 곡 파일 경로와 이름 형식 설정
                #for song in song_lists:
                #    try:
                #        pg.mixer.music.load(os.path.join(self.sng_dir, song))
                #        self.song_list.append(song.split('.')[0])
                #        self.song_path.append(os.path.join(self.sng_dir, song))
                #    except:
                #        print("error: " + str(song) + "is unsupported format music file.")

                song_formats = {
                    1: "M01.ogg",
                    2: "M02.ogg",
                    3: "M03.ogg",
                    4: "M04.ogg",
                    5: "M05.ogg",
                    6: "M06.ogg",
                    7: "M07.ogg",
                    8: "M08.ogg",
                    9: "M09.ogg",
                    10: "M10.ogg",
                    11: "M11.ogg",
                    12: "M12.ogg"
                    }
                
                # 번역 데이터
                translations = {
                    "Moonbeats - Music Preference Survey": {
                        "English": "Moonbeats - Music Preference Survey",
                        "Korean": "Moonbeats - 음악 선호도 조사",
                        "Chinese": "Moonbeats - 音乐偏好调查",
                        "Japanese": "Moonbeats - 音楽の好み調査"
                    },
                    "Language:": {
                        "English": "Language:",
                        "Korean": "언어:",
                        "Chinese": "语言：",
                        "Japanese": "言語："
                    },
                    "Play": {
                        "English": "Play",
                        "Korean": "재생",
                        "Chinese": "播放",
                        "Japanese": "再生"
                    },
                    "Stop": {
                        "English": "Stop",
                        "Korean": "정지",
                        "Chinese": "停止",
                        "Japanese": "停止"
                    },
                    "Save": {
                        "English": "Save",
                        "Korean": "저장",
                        "Chinese": "保存",
                        "Japanese": "保存"
                    },
                    "Preference": {
                        "English": "Preference",
                        "Korean": "선호도",
                        "Chinese": "偏好",
                        "Japanese": "好み"
                    },
                    "Invalid value. Please enter a float value between 1 and 10.": {
                        "English": "Invalid value. Please enter a float value between 1 and 10.",
                        "Korean": "잘못된 값입니다. 1부터 10까지의 실수값을 입력하세요.",
                        "Chinese": "无效的值。请输入1到10之间的浮点数值。",
                        "Japanese": "無効な値です。1から10までの浮動小数点値を入力してください。"
                    },
                    "3 recommended songs:": {
                        "English": "3 recommended songs:",
                        "Korean": "추천 곡 3개:",
                        "Chinese": "3首推荐歌曲：",
                        "Japanese": "おすすめの曲3曲："
                    },
                    "Top 3 Songs": {
                        "English": "Top 3 Songs",
                        "Korean": "상위 3개의 곡",
                        "Chinese": "前3首歌曲",
                        "Japanese": "トップ3曲"
                    }
                }

                def play_music(song_number):
                    music_path = f"{self.sng_dir}/{song_formats[song_number]}"
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.play()
                    check_user_input()

                def stop_music():
                    pygame.mixer.music.stop()

                def check_user_input():
                    root.update()  # UI 업데이트
                    if pygame.mixer.music.get_busy():
                        root.after(100, check_user_input)  # 100ms마다 사용자 입력 체크
                    else:
                        save_button.config(state=tk.NORMAL)  # 저장 버튼 활성화

                def validate_value(value):
                    global current_language
                    try:
                        value = float(value)
                        if value < 1 or value > 10:
                            raise ValueError
                        return value
                    except ValueError:
                        error_message = translations["Invalid value. Please enter a float value between 1 and 10."][current_language]
                        error_label.config(text=error_message)
                        return None

                def save_values():
                    global new_pref  # 전역 변수를 사용하도록 선언
                    global num
                    global new_data
                    global prefer_data
                    global value

                    values = []
                    error_message_shown = False
                    for entry in entries:
                        new_pref = values
                        value = entry.get()
                        value = validate_value(value)
                        if value is None:
                            if value is None:
                                error_message_shown = True
                                return

                        values.append(value)
                                    
                    if not error_message_shown:
                        global top_songs
                        new_pref = values  # 입력받은 값 저장
                                    
                        save_button.config(state=tk.DISABLED)  # 저장 버튼 비활성화
                        stop_button.config(state=tk.DISABLED)  # 정지 버튼 비활성화
                                                    
                        top_songs = get_top_songs(new_pref)  # 상위 곡 가져오기
                        display_top_songs(top_songs)  # 상위 곡 표시

                        # 새로운 데이터 프레임 생성
                        music_list = ["M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10", "M11", "M12"]
                        new_data = pd.DataFrame([new_pref], columns=music_list)

                        # 기존 데이터 로드
                        os.chdir(f"{self.csv_dir}")
                        prefer_data = pd.read_csv("moonbeat_music_preference.csv")

                        # 새로운 데이터에 Id 열 번호 설정
                        new_data['Id'] = range(prefer_data['Id'].max() + 1, prefer_data['Id'].max() + 2)
                                                        
                        # 새로운 유저의 데이터를 기존 데이터에 추가
                        update_data = pd.concat([prefer_data, new_data], ignore_index=True)
                                                        
                        # 업데이트된 데이터를 CSV 파일로 저장
                        os.chdir(f"{self.csv_dir}")
                        update_data.to_csv('moonbeat_music_preference.csv', index=False)

                        num = num+1

                        # 선호도 조사 창 숨기기
                        root.withdraw()
                        # 메인 게임 창 보이기
                        root.deiconify()


                def get_top_songs(new_pref):
                    os.chdir(f"{self.csv_dir}")
                    prefer_data = pd.read_csv("moonbeat_music_preference.csv")

                    # 거리 행렬 계산
                    distance = hierarchy.distance.pdist(prefer_data.iloc[:, 1:])
                    distance_matrix = hierarchy.distance.squareform(distance)

                    # 행끼리 군집화
                    out = hierarchy.linkage(distance_matrix, method="complete")

                    # 군집 수를 4개로 설정
                    member = hierarchy.fcluster(out, 4, criterion="maxclust")

                    # 군집의 특성 살펴보기
                    cluster_means = prefer_data.iloc[:, 1:].groupby(member).mean()

                    # 새 데이터의 군집 확인
                    new_distance = hierarchy.distance.cdist(cluster_means, np.array([new_pref]))
                    new_member = member[np.argmin(new_distance)]

                    # 새 데이터가 해당하는 군집의 선호도가 높은 상위 3개의 곡을 선정
                    clss = cluster_means[cluster_means.index == new_member]
                    top_3_columns = clss.mean().sort_values(ascending=False).index[:3]

                    return top_3_columns


                def change_language(lang):
                    global current_language
                    current_language = lang
                    root.title(translations["Moonbeats - Music Preference Survey"][current_language])
                    language_label.config(text=translations["Language:"][current_language])
                    play_frame.config(text=translations["Play"][current_language])
                    stop_button.config(text=translations["Stop"][current_language])
                    preference_frame.config(text=translations["Preference"][current_language])
                    save_button.config(text=translations["Save"][current_language])
                    
                    for i, button in enumerate(play_buttons):
                        button.config(text=f"M{i+1}")


                def display_top_songs(top_songs):
                    global top_songs_label, current_language

                    # 사용자가 선택한 언어에 해당하는 텍스트 가져오기
                    recommended_songs_text = translations["3 recommended songs:"][current_language]
                    top_songs_title = translations["Top 3 Songs"][current_language]

                    # 텍스트를 포맷하여 완전한 메시지 생성
                    top_songs_text = "{}\n{}".format(recommended_songs_text, ", ".join(top_songs))

                    top_songs_window = tk.Toplevel(root)
                    top_songs_window.title(top_songs_title)

                    top_songs_label = tk.Label(top_songs_window, text=top_songs_text, fg="red", font=("Helvetica", 15, "bold"))
                    top_songs_label.pack()


                # 언어 선택 변수
                current_language = "Korean"
                                
                # 메인 창 생성
                root = tk.Tk()
                root.title(translations["Moonbeats - Music Preference Survey"][current_language])

                # 언어 선택 프레임 생성
                language_frame = tk.Frame(root)
                language_frame.pack(pady=20)

                # 언어 선택 레이블 생성
                language_label = tk.Label(language_frame, text=translations["Language:"][current_language])
                language_label.pack(side=tk.LEFT)

                # 언어 선택 콤보 박스 생성
                language_combo = ttk.Combobox(language_frame, values=list(translations["Moonbeats - Music Preference Survey"].keys()))
                language_combo.set('-----')  # 기본값 설정
                language_combo.pack(side=tk.LEFT, padx=10)

                # 언어 선택 함수 연결
                language_combo.bind("<<ComboboxSelected>>", lambda event: change_language(language_combo.get()))

                # 노래 재생 프레임 생성
                play_frame = tk.LabelFrame(root, text=translations["Play"][current_language])
                play_frame.pack(pady=20)

                # 노래 재생 버튼 생성
                play_buttons = []
                for i in range(1, 13):
                    play_button = tk.Button(play_frame, text=f"M{i}", command=lambda num=i: play_music(num))
                    play_button.pack(side=tk.LEFT, padx=10)
                    play_buttons.append(play_button)

                # 노래 정지 버튼 생성
                stop_button = tk.Button(root, text=translations["Stop"][current_language], command=stop_music)
                stop_button.pack(pady=20)

                # 선호도 입력 프레임 생성
                preference_frame = tk.LabelFrame(root, text=translations["Preference"][current_language])
                preference_frame.pack(pady=20)

                # 선호도 입력 레이블 및 엔트리 생성
                entries = []
                for i in range(1, 13):
                    label = tk.Label(preference_frame, text=f"M{i}")
                    label.grid(row=i, column=0, padx=10, pady=5)
                    entry = tk.Entry(preference_frame)
                    entry.grid(row=i, column=1, padx=10, pady=5)
                    entries.append(entry)

                scroll_frame = ttk.Frame(root)
                scroll_frame.pack(fill=tk.BOTH, expand=True)

                error_label = tk.Label(root, text="", fg="red")
                error_label.pack()

                # 저장 버튼 생성
                save_button = tk.Button(root, text=translations["Save"][current_language], command=save_values)
                save_button.pack(pady=20)

                if num == 1:
                    root.withdraw()
                    root.deiconify()
                else:
                    root.mainloop()

                help_surface = pg.Surface((WIDTH - 60, HEIGHT - 60))
                help_surface.fill(WHITE)
                help_surface.set_alpha(200)                  
                self.screen.blit(help_surface, pg.Rect(30, 30, 0, 0))
                self.draw_text("- " + self.load_language(5) + " -", 36, BLACK, 320, 50, 255)
                self.draw_text(self.load_language(9), 16, BLACK, 320, 150)
                self.draw_text(self.load_language(10), 16, BLACK, 320, 220)
                self.draw_text(self.load_language(11), 16, BLACK, 320, 290)
            else:
                self.draw_text(self.load_language(2), 36, WHITE, 480, 105, screen_alpha, select_index[0])
                self.draw_text(self.load_language(3), 36, WHITE, 480, 175, screen_alpha, select_index[1])
                self.draw_text(self.load_language(4), 36, WHITE, 480, 245, screen_alpha, select_index[2])
                self.draw_text(self.load_language(0), 24, WHITE, 480, 315, screen_alpha, select_index[3])

            


        elif self.screen_mode == 3:     #song select screen
            surface = pg.Surface((WIDTH, HEIGHT))
            self.screen.blit(self.spr_selctback, (0, 0))
            surface.set_alpha(max(screen_alpha - 50, 0))
            circle_coord = (round(WIDTH * 1.2), round(HEIGHT / 2))
            pg.draw.circle(surface, BLACK, circle_coord, round(0.78 * WIDTH + screen_alpha), 1)
            pg.draw.circle(surface, BLACK, circle_coord, round(0.32 * WIDTH + screen_alpha), 1)
            pg.draw.circle(surface, BLACK, circle_coord, max(round(-0.1 * WIDTH + screen_alpha), 1), 1)
            pg.draw.circle(surface, RED, circle_coord, max(round(-0.12 * WIDTH + screen_alpha), 1), 1)
            pg.draw.circle(surface, BLUE, circle_coord, max(round(-0.08 * WIDTH + screen_alpha), 1), 1)
            
            if self.song_select > 2:
                self.draw_text(self.song_list[self.song_select - 3], 16, BLACK, 0.29 * WIDTH, 0.25 * HEIGHT - 20, max(screen_alpha - 220, 0))
                
            if self.song_select > 1:
                self.draw_text(self.song_list[self.song_select - 2], 18, BLACK, 0.27 * WIDTH, 0.375 * HEIGHT - 20, max(screen_alpha - 180, 0))
                
            self.draw_text(self.song_list[self.song_select - 1], 24, BLACK, 0.25 * WIDTH, 0.5 * HEIGHT - 20, screen_alpha)

            if self.song_select < self.song_num:
                self.draw_text(self.song_list[self.song_select], 18, BLACK, 0.27 * WIDTH, 0.625 * HEIGHT - 20, max(screen_alpha - 180, 0))
                
            if self.song_select < self.song_num - 1:
                self.draw_text(self.song_list[self.song_select + 1], 16, BLACK, 0.29 * WIDTH, 0.75 * HEIGHT - 20, max(screen_alpha - 220, 0))
            
            button_songUp = '▲' if self.screen_value[1] == 1 else '△'
            button_songDown = '▼' if self.screen_value[1] == 2 else '▽'
            select_index = [True if self.screen_value[1] == i + 3 else False for i in range(2)]
            self.draw_text(button_songUp, 24, BLACK, 0.31 * WIDTH, 0.125 * HEIGHT - 20, screen_alpha)
            self.draw_text(button_songDown, 24, BLACK, 0.31 * WIDTH, 0.875 * HEIGHT - 30, screen_alpha)

            if self.song_highScore[self.song_select - 1] == -1:
                self.draw_text(self.load_language(12), 32, RED, 0.71 * WIDTH, HEIGHT / 2 - 100, screen_alpha)
            else:
                if self.song_highScore[self.song_select - 1] >= self.song_perfectScore[self.song_select - 1]:
                    try:
                        font = pg.font.Font(self.gameFont, 36)
                    except:
                        font = pg.font.Font(os.path.join(self.fnt_dir, DEFAULT_FONT), 36)

                    font.set_bold(True)
                    cleartext_surface = font.render(self.load_language(14), False, BLUE)
                    rotated_surface = pg.transform.rotate(cleartext_surface, 25)
                    rotated_surface.set_alpha(max(screen_alpha - 180, 0))
                    cleartext_rect = rotated_surface.get_rect()
                    cleartext_rect.midtop = (round(0.71 * WIDTH), round(HEIGHT / 2 - 150))
                    self.screen.blit(rotated_surface, cleartext_rect)
                    
                self.draw_text(self.load_language(8), 28, BLACK, 0.69 * WIDTH, HEIGHT / 2 - 130, screen_alpha)
                self.draw_text(str(self.song_highScore[self.song_select - 1]), 28, BLACK, 0.69 * WIDTH, HEIGHT / 2 - 70, screen_alpha)
                self.draw_text(self.load_language(7), 32, BLACK, 0.69 * WIDTH, HEIGHT / 2 + 25, screen_alpha, select_index[0])
                
            self.draw_text(self.load_language(6), 32, BLACK, 0.73 * WIDTH, HEIGHT / 2 + 85, screen_alpha, select_index[1])
        elif self.screen_mode == 4:             #play screen
            surface = pg.Surface((WIDTH, HEIGHT))
            self.screen.blit(self.spr_playback, (0, 0))
            surface.set_alpha(max(screen_alpha - 240, 0))
            pg.draw.circle(surface, BLACK, (round(WIDTH / 2), round(HEIGHT / 2)), 200, 1)
            self.screen.blit(surface, (0,0))
            self.draw_sprite(((WIDTH - 99) / 2, (HEIGHT - 99) / 2), self.spr_circle, screen_alpha, self.circle_rot)
            time_m = self.game_tick // 60000
            time_s = str(round(self.game_tick / 1000) - time_m * 60)

            if (len(time_s) == 1):
                time_s = "0" + time_s
                
            time_str = str(time_m) + " : " + time_s
            score_str = self.load_language(13) + " : " + str(self.score)
            self.draw_text(time_str, 24, BLACK, 10 + len(time_str) * 6, 15, screen_alpha)
            self.draw_text(score_str, 24, BLACK, WIDTH - 10 - len(score_str) * 6, 15, screen_alpha)
        else:
            surface = pg.Surface((WIDTH, HEIGHT))
            self.screen.blit(self.spr_resultback, (0, 0))
            surface.set_alpha(max(screen_alpha - 50, 0))
            circle_coord = (round(WIDTH / 2), round(HEIGHT / 2))
            pg.draw.circle(surface, BLUE, circle_coord, round(HEIGHT / 2 - 30), 1)
            pg.draw.circle(surface, BLACK, circle_coord, round(HEIGHT / 2), 1)
            pg.draw.circle(surface, RED, circle_coord, round(HEIGHT / 2 + 30), 1)
            self.draw_text(self.load_language(15) + " : " + str(self.song_perfectScore[self.song_select - 1]), 32, BLACK, WIDTH / 2, HEIGHT / 2 - 65, screen_alpha)
            self.draw_text(self.load_language(13) + " : " + str(self.score), 32, BLACK, WIDTH / 2, HEIGHT / 2 - 5, screen_alpha)
            select_index = [True if self.screen_value[2] == i + 1 else False for i in range(2)]
            self.draw_text(self.load_language(17), 24, BLACK, WIDTH / 2 - 100, HEIGHT / 2 + 125, ALPHA_MAX, select_index[0])
            self.draw_text(self.load_language(16), 24, BLACK, WIDTH / 2 + 100, HEIGHT / 2 + 125, ALPHA_MAX, select_index[1])
                        
    def load_language(self, index):
        try:
            return self.language_list[self.language_mode][index]
        except:
            return "Font Error"

    def load_songData(self):
        with open(self.song_dataPath[self.song_select - 1], "r", encoding = 'UTF-8') as data_file:
            data_fileLists = data_file.read().split('\n')
        
        for data_line in data_fileLists:
            if data_line != "" and data_line[0] != 's':
                data_fileList = data_line.split(' - ')
                time_list = data_fileList[0].split(':')
                shot_list = data_fileList[1].split(', ')
                current_songData = list()
                current_songData.append(int(time_list[0]) * 60000 + int(time_list[1]) * 1000 + int(time_list[2]) * 10)
                
                for shot in shot_list:
                    if shot[0] == 'E':
                        shot_color = -1
                    elif shot[0] == 'W':
                        shot_color = 1
                    elif shot[0] == 'B':
                        shot_color = 2
                    elif shot[0] == 'D':
                        shot_color = 3
                    else:
                        shot_color = 4

                    if shot_color != -1:
                        if shot[1] == 'D':
                            shot_mode = 0
                        elif shot[1] == 'R':
                            shot_mode = 90
                        elif shot[1] == 'U':
                            shot_mode = 180
                        else:
                            shot_mode = 270

                        if shot[2] == 'D':
                            shot_dir = 0
                        elif shot[2] == 'R':
                            shot_dir = 90
                        elif shot[2] == 'U':
                            shot_dir = 180
                        else:
                            shot_dir = 270

                        shot_data = (shot_color, shot_mode, shot_dir, int(shot[3]))
                        current_songData.append(shot_data)
                    else:
                        shot_data = -1
                        current_songData.append(shot_data)

                self.song_data.append(current_songData)

    def create_shot(self):
        if self.game_tick >= self.song_data[self.song_dataIndex][0]:
            if self.song_data[self.song_dataIndex][1] != -1:
                shot_num = len(self.song_data[self.song_dataIndex]) - 1
                
                for shot in range(shot_num):
                    shot_data = self.song_data[self.song_dataIndex][shot + 1]

                    obj_shot = Shot(self, shot_data[0], shot_data[1], shot_data[2], shot_data[3])
                    self.all_sprites.add(obj_shot)
                    self.shots.add(obj_shot)

                self.song_dataIndex += 1
            else:
                if self.score >= self.song_highScore[self.song_select - 1]:
                    with open(self.song_dataPath[self.song_select - 1], "r", encoding = 'UTF-8') as file:
                        file_lists = file.read().split('\n')

                    file_list = 'score:' + str(self.score) + ':' + str(self.song_perfectScore[self.song_select - 1]) + '\n'

                    for shot_file in file_lists:
                        if shot_file != '' and shot_file[0] != 's':
                            file_list += '\n' + shot_file
                        
                    with open(self.song_dataPath[self.song_select - 1], 'w+', encoding = 'UTF-8') as song_file:
                        song_file.write(file_list)

                    self.song_highScore[self.song_select - 1] = self.score
                    
                self.screen_value[1] = 1
            
    def draw_sprite(self, coord, spr, alpha = ALPHA_MAX, rot = 0):
        if rot == 0:
            spr.set_alpha(alpha)
            self.screen.blit(spr, (round(coord[0]), round(coord[1])))
        else:
            rotated_spr = pg.transform.rotate(spr, rot)
            rotated_spr.set_alpha(alpha)
            self.screen.blit(rotated_spr, (round(coord[0] + spr.get_width() / 2 - rotated_spr.get_width() / 2), round(coord[1] + spr.get_height() / 2 - rotated_spr.get_height() / 2)))
        
    def draw_text(self, text, size, color, x, y, alpha = ALPHA_MAX, boldunderline = False):
        try:
            font = pg.font.Font(self.gameFont, size)
        except:
            font = pg.font.Font(os.path.join(self.fnt_dir, DEFAULT_FONT), size)

        font.set_underline(boldunderline)
        font.set_bold(boldunderline)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (round(x), round(y))
            
        self.screen.blit(text_surface, text_rect)    

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        
        return image

class Shot(pg.sprite.Sprite):           ####################################### Shot Class
    def __init__(self, game, color, mode, direction, speed):      #color(WBDR) mode(DRUL) direction(DRUL)
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.color = color
        self.mode = mode
        self.direction = direction
        self.speed = speed
        self.alpha = ALPHA_MAX
        self.correct_code = [1, 2, 3, 4]
        self.correct = 0
        image = self.game.spr_shot.get_image((color - 1) * 45, 0, 45, 61)
        
        if self.mode == 0:
            self.image = pg.transform.rotate(image, 270)
            self.touch_coord = (round(- self.image.get_width() / 2), round(23 - self.image.get_height() / 2))
        elif self.mode == 90:
            self.image = image
            self.touch_coord = (round(23 - self.image.get_width() / 2), round(- self.image.get_height() / 2))
        elif self.mode == 180:
            self.image = pg.transform.rotate(image, 90)
            self.touch_coord = (round(- self.image.get_width() / 2), round(-23 - self.image.get_height() / 2))
        else:
            self.image = pg.transform.rotate(image, 180)
            self.touch_coord = (round(-23 - self.image.get_width() / 2), round(- self.image.get_height() / 2))
        
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = round(WIDTH  / 2), round(HEIGHT / 2)

        if self.direction == 0:
            self.rect.y += round(WIDTH / 2 + 100)
        elif self.direction == 90:
            self.rect.x += round(WIDTH / 2 + 100)
        elif self.direction == 180:
            self.rect.y -= round(WIDTH / 2 + 100)
        else:
            self.rect.x -= round(WIDTH / 2 + 100)

        self.rect.x += self.touch_coord[0]
        self.rect.y += self.touch_coord[1]
        
    def update(self):
        self.image.set_alpha(self.alpha)

        if self.alpha > 0:
            if self.correct == 1:
                self.alpha -= ALPHA_MAX / 5
            else:
                if self.correct == -1:
                    self.alpha -= ALPHA_MAX / 85
                
                if self.direction == 0:
                    self.rect.y -= self.speed
                elif self.direction == 90:
                    self.rect.x -= self.speed
                elif self.direction == 180:
                    self.rect.y += self.speed
                else:
                    self.rect.x += self.speed

            if self.rect.x > WIDTH * 2 or self.rect.x < -WIDTH or self.rect.y > HEIGHT * 2 or self.rect.y < -HEIGHT:
                self.kill()
        else:
            self.kill()

        if self.correct == 0 and self.rect.x == round(WIDTH / 2) + self.touch_coord[0] and self.rect.y == round(HEIGHT / 2) + self.touch_coord[1]:
            if self.game.circle_dir == self.correct_code[round(self.mode / 90 - self.color + 1)]:
                self.game.score += 100
                self.correct = 1
                
                if self.color == 1:
                    self.game.sound_drum1.play()
                elif self.color == 2:
                    self.game.sound_drum2.play()
                elif self.color == 3:
                    self.game.sound_drum3.play()
                else:
                    self.game.sound_drum4.play()
            else:
                self.correct = -1

game = Game()

while game.running:
    game.run()
    
pg.quit()


