import curses
from random import randint


print('''SNAKE
    Pravidlá hry:
    - hra končí ak snake narazí do steny alebo sám do seba
    - 1 bod za každý $
    - ESC pre ukončenie hry
    - Ovládanie šipkami (UP, DOWN, LEFT, RIGHT)
    ***************************************************
    Press ENTER to play......
''')
x = input()


ESC = 27
skore = 0

'''Inincializácia a nastavenie hernej plochy'''
# ***************************************************
hra = curses.initscr()
# zneviditelní kurzor
curses.curs_set(0)
# nevypisuje znaky
curses.noecho()
vyska_okna, sirka_okna = 20, 60
# inicializácia herného okna
okno = curses.newwin(vyska_okna, sirka_okna, 0, 0)
okno.border(0)
# umožnuje používať funkcie špecialnych znakov(šípky)
okno.keypad(True)
# refreshuje okno (v ms intervaloch)
okno.timeout(100)
# ***************************************************

# hlavička hry
okno.addstr(0,27,'SNAKE')
okno.addstr(0,1,'ESC - koniec hry')

# inicializácia snake - hada o veľkosti 3 blokov na pozícii (10,10)
had_x = 25
had_y = 10
snake = [[had_y, had_x], [had_y, had_x+1], [had_y, had_x+2]]

# inicializácia bloku bodov na pozícii (10,50)
body = [10, 30]
okno.addch(int(body[0]), int(body[1]), '$')

# štartovací smer hada
c = curses.KEY_LEFT

'''Loop samotnej hry'''
# ***************************************************
while True:

    # odchytáva stlačené klávesy
    # ak dedôjde k stlačeniu žiadnej klavesy funkcia getch() vráti -1
    dalsi_c = okno.getch()
    if dalsi_c not in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_UP, ESC] or dalsi_c == -1:
        c = c
    else:
        c = dalsi_c

    # ak snake narazí do steny okna alebo sám do seba    
    if snake[0][0] in [0, vyska_okna-1] or snake[0][1]  in [0, sirka_okna-1] or snake[0] in snake[1:]:
        curses.endwin()
        print(f'Tvoje skóre je {skore}.')
        quit()

    # momentálna poloha začiatku snake
    snake_hlava = [snake[0][0], snake[0][1]]

    # definícia funkcií klávesov pre ovládanie
    # výpočet pozície novej hlavy
    if c == curses.KEY_DOWN:
        snake_hlava[0] += 1
    if c == curses.KEY_RIGHT:
        snake_hlava[1] += 1
    if c == curses.KEY_UP:
        snake_hlava[0] -= 1
    if c == curses.KEY_LEFT:
        snake_hlava[1] -= 1
    if c == ESC:
        curses.endwin()
        print(f'Tvoje skóre je {skore}.')
        quit()

    # vloženie novej hlavy do tela snake -> posunutie    
    snake.insert(0, snake_hlava)

    '''Ak snake narazí na blok s bodom'''
    # ***************************************************
    if snake[0] == body:
        skore += 1
        body = None
        while not body:
            # náhodné koordinácie nového bodu
            nove_body = [randint(2, vyska_okna-2),randint(2, sirka_okna-2)]
            # kontrola koordinácií nového bodu aby sa nevygeneroval na pozícii snake
            if nove_body not in snake:
                body = nove_body
            else:
                body = None
        # vypísanie nového bodu na okno
        okno.addch(body[0], body[1], '$')
    else:
        # Ak snake narazí na blok s bodom, preskočí sa tento blok kódu, tým pádom sa nezmaže posledný článok ale stále sa jeden pridá, čím dôjde k natiahnutiu snake.
        # zmazanie konca snake(chvostu) -> posunutie
        snake_koniec = snake.pop()
        okno.addch(int(snake_koniec[0]), int(snake_koniec[1]), ' ')
    # ***************************************************

    # update skóre
    okno.addstr(0, 40, 'skóre ' + str(skore))
    # vypísanie nového članku snake -> posunutie
    okno.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_DIAMOND)
# ***************************************************