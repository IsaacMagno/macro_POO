import pyautogui
from time import sleep, time
import json
import os

RIGHT = 'right'
LEFT = 'left'

class Island_Colector:
    def __init__(self, name, seed, plots, next_island):
        self.name = name
        self.seed = seed
        self.plots = plots
        self.next_island = next_island
    
    def _shift_down(self):
        pyautogui.keyDown('shiftleft')
        pyautogui.keyDown('shiftright')
        pyautogui.keyDown('shift')

    def _shift_up(self):
        pyautogui.keyUp('shiftleft')
        pyautogui.keyUp('shiftright')
        pyautogui.keyUp('shift')
    
    def to_colect_loop(self, p):
        x, y = p
        pyautogui.moveTo(x, y, 0.3)
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        sleep(0.5)
    
    def to_plant_loop(self, p):
        x, y = p
        pyautogui.moveTo(x, y, 0.3)
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        sleep(1)

    def _move_loop(self, move):
        x, y = move
        pyautogui.moveTo(x, y, 0.6)
        pyautogui.click(button = RIGHT)
        sleep(1.5)

    def _move_loop_fast(self, move):
        x, y = move
        pyautogui.moveTo(x, y, 0.6)
        pyautogui.click(button = RIGHT)
        sleep(1)

    def _mount(self):
        pyautogui.press('a', interval=3)
        sleep(0.2)

    def _inventory(self):
        pyautogui.press('i')
        sleep(1.2)

        seed = self.seed

        if seed == 'seed_1':
            pyautogui.moveTo(788, 430, 0.3)
            pyautogui.click(button = LEFT)
            sleep(0.5)
        elif seed == 'seed_2':
            pyautogui.moveTo(845, 423, 0.3)
            pyautogui.click(button = LEFT)
            sleep(0.5)
        elif seed == 'seed_3':
            pyautogui.moveTo(900, 423, 0.3)
            pyautogui.click(button = LEFT)
            sleep(0.5)

        pyautogui.moveTo(377, 312, 0.3)
        pyautogui.click(button = LEFT)
        sleep(1)

    def _bank_island(self):
        pyautogui.moveTo(424,280,1)
        sleep(0.5)
        pyautogui.doubleClick(button = LEFT)
        sleep(0.5)

        #abre os loadouts
        pyautogui.moveTo(89, 176, 1)
        sleep(0.5)
        pyautogui.click(button = LEFT)
        sleep(0.5)

        #seleciona o loadout
        pyautogui.moveTo(71,311, 1)
        sleep(0.5)
        pyautogui.click(button = LEFT)

        #equipa o loadout
        pyautogui.moveTo(205, 181, 1)
        sleep(0.5)
        pyautogui.click(button = LEFT)

        #fecha o banco e monta
        pyautogui.moveTo(635,504, 1)
        pyautogui.click(button = RIGHT)
        sleep(1)
        self._mount()

        #anda até a saida do banco
        pyautogui.moveTo(834, 576, 1)
        pyautogui.click(button = RIGHT)
        sleep(1.5)
        pyautogui.click(834, 576, button = RIGHT)
        sleep(10)

        #anda até o planejador de viagem
        with open("scripts/bank_to_island.json") as pos:
            move_list = json.load(pos)

            for move in move_list:
                for m in move["walk"]:
                    self._move_loop(m)

        # seleciona a ilha e vai até ela
        pyautogui.moveTo(626, 164, 1)
        pyautogui.click(button = LEFT)
        pyautogui.moveTo(234, 652, 1)
        sleep(1)
        pyautogui.click(button = LEFT)
        sleep(10)

    def _walk_plantation(self):
        with open("scripts/walk_to_plantation.json") as pos:
            walk_list = json.load(pos)

            for move in walk_list:
                for m in move["walk"]:
                    self._move_loop(m)

    def _colect_loop(self):
        num_plots = self.plots

        with open("scripts/colect_plots_3.json") as pos:
            plots_list = json.load(pos)

            for plot in plots_list:

                self._shift_down()

                for p in plot["plot"]:
                    self.to_colect_loop(p)

                self._shift_up()

                if plot["next"]:
                    self._mount()
                    for move in plot["next"]:
                        self._move_loop_fast(move)
                else:
                    sleep(1)

        if num_plots > 3:
            self._mount()

            self._move_loop([774, 137])

            with open("scripts/colect_plots_2.json") as pos:
                plots_list = json.load(pos)

                for plot in plots_list:

                    self._shift_down()

                    for p in plot["plot"]:
                        self.to_colect_loop(p)
                    
                    self._shift_up()

                    if plot["next"]:
                        self._mount()
                        for move in plot["next"]:
                            self._move_loop_fast(move)
                    else:
                        sleep(1)

    def _plant_loop(self):
        num_plots = self.plots
        if num_plots > 3:
            with open("scripts/plant_plots_first_2.json") as pos:
                plant_list = json.load(pos)

                for plant in plant_list:
                    self._inventory()

                    for p in plant["plant"]:
                        self.to_plant_loop(p)
                    
                    self._mount()

                    pyautogui.press('esc')
                    sleep(1)

                    if plant["next"]:
                        for move in plant["next"]:
                            self._move_loop_fast(move)
        else:
            self._move_loop([579,642])

        with open("scripts/plant_plots_last_3.json") as pos:
            plant_list = json.load(pos)

            for plant in plant_list:
                self._inventory()

                for p in plant["plant"]:
                    self.to_plant_loop(p)
                
                self._mount()

                pyautogui.press('esc')
                sleep(1)

                if plant["next"]:
                    for move in plant["next"]:
                        self._move_loop_fast(move)

    def _finish_island(self):
        with open("scripts/finish_island.json") as pos:
            to_planner = json.load(pos)

            for walk in to_planner:
                for w in walk["walk"]:
                    self._move_loop(w)

            pyautogui.moveTo(238, 478, 0.5) # abre o planejador
            pyautogui.click(button = LEFT)
            sleep(1)

            pyautogui.moveTo(109, 238, 0.5) # seleciona o texto
            pyautogui.mouseDown()
            sleep(0.25)
            pyautogui.mouseUp()

            pyautogui.press('backspace') # apaga o texto
            sleep(1)

            if self.next_island:
                pyautogui.write(self.next_island, interval = 0.10) # escreve  nome da proxima ilha
                sleep(0.5)

            else:
                pyautogui.write("cidade", interval = 0.10) # volta pra cidade
                sleep(0.5)

            pyautogui.press('enter')

            pyautogui.moveTo(211, 653, 1.2) # vai pra proxima ilha
            pyautogui.click(button = LEFT)
            sleep(10)

    def _to_bank(self):
        with open("scripts/to_bank.json") as pos:
            walk_list = json.load(pos)
            for walk in walk_list:
                for w in walk["walk"]:
                    self._move_loop(w) 

                sleep(8)

                for b in walk["bank"]:
                    self._move_loop(b)

        pyautogui.moveTo(336, 136, 0.5)
        pyautogui.click(button = 'PRIMARY')

    def colect(self):
        start = time()

        if self.name == "first":
            print('Coletor iniciado.')
            self._bank_island()
            print('Saindo do banco...')

        print('Indo para as plantações!')
        self._walk_plantation()

        print(f'Iniciando colheita')
        self._colect_loop()
        print('Colheita finalizada.')

        print('Iniciando plantação.')
        self._plant_loop()
        print('Plantação finalizada!')

        print(f'Indo para a proxima ilha.')
        self._finish_island()

        stop = time()
        print(f"\nTempo de colheita: {(stop - start):.2f} segundos.")

        if not self.next_island:
            print('Todas as ilhas foram colhidas!\nVoltando para o banco.')
            self._to_bank()
            print('Colheita finalizada.')


def run():
    with open("scripts/islands.json") as islands:
        islands_list = json.load(islands)
        try:
            for island in islands_list:

                    name = island["name"]
                    seed = island["seed"]
                    plots = island["plots"]
                    next_island = island["next_island"]

                    script = Island_Colector(name, seed, plots, next_island)
                    colector = script.colect()

        except KeyboardInterrupt:
            print('\nColheita interrompida pelo teclado!')


if __name__ == '__main__':
    run()
