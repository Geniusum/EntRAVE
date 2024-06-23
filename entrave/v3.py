"Constants"

MAX_WIDTH = 1200 # The width of the board, and the visualizer window
MAX_HEIGHT = 900 # The height of the board, and the visualizer window
MARGE = 40 # The marge of spawn area

"Imports & Others"

import time
import tkinter as tk
import random as rd

class Articulation():
    def __init__(self, entity, member_a, member_b) -> None:
        self.entity = entity
        self.member_a = member_a
        self.member_b = member_b

class Member():
    def __init__(self, entity) -> None:
        self.id = rd.randint(1000, 9999)
        self.entity = entity
        self.articulations = []

        self.nears = {}

        self.informations = []

        self.x = rd.randint(MARGE, MAX_WIDTH - MARGE)
        self.y = rd.randint(MARGE, MAX_HEIGHT - MARGE)

class Entity():
    def __init__(self, members:int=6, choice:bool=False, only_members:bool=False, informations:int=10, inf_evolution:bool=True) -> None:
        self.id = rd.randint(1000, 9999)

        self.members = []
        self.articulations = []
        self.informations = []

        for member in range(1, members, 2):
            a = Member(self)
            if len(self.members):
                for b in self.members.copy():
                    if choice:
                        if rd.randint(1, len(self.members)) == 1:
                            if not only_members:
                                articulation = Articulation(self, a, b)
                                a.articulations.append(articulation)
                                b.articulations.append(articulation)
                                self.articulations.append(articulation)
                    else:
                        if not only_members:
                            articulation = Articulation(self, a, b)
                            a.articulations.append(articulation)
                            b.articulations.append(articulation)
                            self.articulations.append(articulation)
                self.members.append(a)
            else:
                b = Member(self)
                if not only_members:
                    articulation = Articulation(self, a, b)
                    a.articulations.append(articulation)
                    b.articulations.append(articulation)
                    self.articulations.append(articulation)
                self.members.append(a)
                self.members.append(b)

        self.args_saves = (members, choice, only_members, informations, inf_evolution)

        for _ in range(informations):
            self.informations.append(Information(self, rd.choice(self.members), rd.randint(0, 1), inf_evolution))

class Information():
    def __init__(self, entity:Entity, member:Member, bin:int, inf_evolution:bool=True) -> None:
        self.entity = entity
        self.member: Member = member

        self.x = 0
        self.y = 0

        self.bin = bin
        self.choices = ["nothing", "transform", "relocate"]
        for _ in range(30):
            self.choices.append("nothing")
        self.choice = "nothing"
        self.choosed_member: Member = None

        self.member.informations.append(self)

        self.percent = 0
        self.speed = rd.randint(4, 10) / 10

        self.color = "#" + hex(rd.randint(200, 255)).replace("0x", "") + hex(rd.randint(200, 255)).replace("0x", "") + hex(rd.randint(200, 255)).replace("0x", "")

        self.inf_evolution = inf_evolution

    def between_numbers(self, p, min, max):
        d = p / 100
        f = max - min
        r = min + (f * d)
        return r

    def do(self):
        if self.choice == "nothing":
            self.x, self.y = self.member.x, self.member.y
            if self.inf_evolution:
                self.speed += rd.randint(0, 100) / 7000
            self.choice = rd.choice(self.choices)
        if self.choice == "transform":
            self.x, self.y = self.member.x, self.member.y
            self.bin = rd.randint(0, 1)
            self.choice = rd.choice(self.choices)
        elif self.choice == "relocate":
            if not self.choosed_member:
                members_av = []
                for ar in self.member.articulations:
                    if not ar.member_a in members_av and not ar.member_a == self.member:
                        members_av.append(ar.member_a)
                    if not ar.member_b in members_av and not ar.member_b == self.member:
                        members_av.append(ar.member_b)
                if len(members_av):
                    self.choosed_member = rd.choice(members_av)
            if self.choosed_member:
                self.x = int(self.between_numbers(self.percent, self.member.x, self.choosed_member.x))
                self.y = int(self.between_numbers(self.percent, self.member.y, self.choosed_member.y))
                self.percent += self.speed
                if self.percent >= 100:
                    self.choosed_member.informations.append(self)
                    self.member.informations.remove(self)
                    self.member = self.choosed_member
                    self.choosed_member = None
                    self.choice = rd.choice(self.choices)
                    self.percent = 0
                    self.x = self.member.x
                    self.y = self.member.y
            else:
                self.choice = rd.choice(self.choices)

class Board():
    def __init__(self, entity:Entity, thickness:int=10, width:int=40, height:int=40, width_mul:bool=False, mul_divid:float=1.5, min_speed:int=1, max_speed:int=10, interval_delay:float=1, sync:bool=False) -> None:
        self.root = tk.Tk()
        self.root.geometry(f"{MAX_WIDTH}x{MAX_HEIGHT}")
        self.root.title("Generation Entity")
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.entity = entity
        self.thickness = thickness
        self.width = width
        self.height = height
        self.width_mul = width_mul
        self.mul_divid = mul_divid
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.interval_delay = interval_delay

        self.articulations = []
        self.members = []
        self.indicators = []
        self.informations = []

        self.process = ""

        self.sync = sync

    def draw_entity(self):
        self.canvas.create_text(10, 10, text=f"{self.entity.id} ; {len(self.entity.members)} members ; {len(self.entity.articulations)} articulations : {len(self.entity.informations)} informations", fill="black", anchor="nw")
        width, height = self.width, self.height
        for member in self.entity.members:
            color = "#343434"
            for articulation in member.articulations:
                s = self.canvas.create_line(articulation.member_a.x + int(width / 2), articulation.member_a.y  + int(height / 2), articulation.member_b.x  + int(width / 2), articulation.member_b.y  + int(height / 2), fill=color, width=self.thickness)
                self.articulations.append([articulation, s])
        for member in self.entity.members:
            color = "lightblue"
            width_, height_ = width, height
            mul = 1
            if self.width_mul:
                mul = len(member.articulations)
                mul = int(mul / self.mul_divid)
                if mul <= 0:
                    mul = 1
                width_, height_ = width * mul, height * mul
            o = self.canvas.create_oval(member.x - width * mul, member.y - height * mul, member.x + width_, member.y + height_, fill=color)
            t = self.canvas.create_text(member.x + int(width_ / 2), member.y - int(height_ / 2), text=f"{member.x} ; {member.y} ; {member.id} ; {len(member.articulations)} ar ; {len(member.informations)} inf", fill="red")
            self.members.append([member, o, t])
        accurate_x = 0
        x_list = []
        accurate_y = 0
        y_list = []
        for member in self.entity.members:
            x_list.append(member.x)
            y_list.append(member.y)
        try:
            accurate_x = int(sum(x_list) / len(x_list))
        except:
            accurate_x = 0
        try:
            accurate_y = int(sum(y_list) / len(y_list))
        except:
            accurate_y = 0
        try: mul
        except: mul = 1
        a = self.canvas.create_oval(accurate_x - width * mul, accurate_y - height * mul, accurate_x + width, accurate_y + height, fill="green")
        t = self.canvas.create_text(accurate_x + int(width / 2), accurate_y - int(height / 2), text=f"{accurate_x} ; {accurate_y}", fill="red")
        self.indicators.append([a, t])
        for information in self.entity.informations:
            width = 10
            height = 10
            class member:
                x = information.x
                y = information.y
            color = information.color
            width_, height_ = width, height
            mul = 1
            o = self.canvas.create_oval(member.x - width * mul, member.y - height * mul, member.x + width_, member.y + height_, fill=color)
            t = self.canvas.create_text(member.x + int(width_ / 2), member.y - int(height_ / 2), text=information.bin, fill="black")
            self.informations.append([o, t, information])

    def update_entity(self):
        width, height = self.width, self.height
        for _ in self.members:
            width_, height_ = width, height
            mul = 1
            member = _[0]
            if self.width_mul:
                mul = len(member.articulations)
                mul = int(mul / self.mul_divid)
                if mul <= 0:
                    mul = 1
                width_, height_ = width * mul, height * mul
            oval = _[1]
            text = _[2]
            self.canvas.coords(oval, member.x - width * mul, member.y - height * mul, member.x + width_, member.y + height_)
            self.canvas.coords(text, member.x + int(width_ / 2), member.y - int(height_ / 2))
            self.canvas.itemconfig(text, text=f"{member.x} ; {member.y} ; {member.id} ; {len(member.articulations)} ar ; {len(member.informations)} inf")
        for _ in self.articulations:
            articulation = _[0]
            line = _[1]
            self.canvas.coords(line, articulation.member_a.x + int(width / 2), articulation.member_a.y + int(height / 2), articulation.member_b.x + int(width / 2), articulation.member_b.y + int(height / 2))
        for _ in self.indicators:
            oval = _[0]
            text = _[1]
            accurate_x = 0
            x_list = []
            accurate_y = 0
            y_list = []
            for member in self.entity.members:
                x_list.append(member.x)
                y_list.append(member.y)
            try: mul
            except: mul = 1
            try:
                accurate_x = int(sum(x_list) / len(x_list))
            except:
                accurate_x = 0
            try:
                accurate_y = int(sum(y_list) / len(y_list))
            except:
                accurate_y = 0
            self.canvas.coords(oval, accurate_x - width * mul, accurate_y - height * mul, accurate_x + width, accurate_y + height)
            self.canvas.coords(text, accurate_x + int(width / 2), accurate_y - int(height / 2))
            self.canvas.itemconfig(text, text=f"{accurate_x} ; {accurate_y}")
        for _ in self.informations:
            oval = _[0]
            text = _[1]
            information = _[2]
            width = 10
            height = 10
            class member:
                x = information.x
                y = information.y
            color = information.color
            width_, height_ = width, height
            mul = 1
            self.canvas.coords(oval, member.x - width * mul, member.y - height * mul, member.x + width_, member.y + height_)
            self.canvas.coords(text, member.x, member.y)
            self.canvas.itemconfig(text, text=information.bin)

    def between_numbers(self, p, min, max):
        d = p / 100
        f = max - min
        r = min + (f * d)
        return r

    def update_entity_positions(self, self_member:bool=True, reference=None):
        for member in self.entity.members:
            directions = ["none", "left", "right", "top", "bottom", "left_top", "right_top", "left_bottom", "right_bottom"]
            rand = rd.choice(directions)
            speed = rd.randint(self.min_speed, self.max_speed)
            def change(sel, divid:int=1):
                if not rand == "none":
                    sp = int(speed / divid)
                    if rand == "left": sel.x -= sp
                    elif rand == "right": sel.x += sp
                    elif rand == "top": sel.y -= sp
                    elif rand == "bottom": sel.y += sp
                    elif rand == "left_top": sel.x -= sp; member.y -= sp
                    elif rand == "right_top": sel.x += sp; member.y -= sp
                    elif rand == "left_bottom": sel.x -= sp; member.y += sp
                    elif rand == "right_bottom": sel.x += sp; member.y += sp
            def sync(sel, divid:int=1, reference=None):
                if reference == None: reference = member
                #sp = int(speed / divid)
                if self.sync:
                    if rd.randint(1, 2) == 1: sel.x = round(self.between_numbers(rd.randint(0, 10) / 10, sel.x, reference.x))
                    if rd.randint(1, 2) == 1: sel.y = round(self.between_numbers(rd.randint(0, 10) / 10, sel.y, reference.y))

            if self_member:
                change(member)
            for sel, near in member.nears.items():
                priority = near["priority"]
                id = near["id"]
                if self_member:
                    if self.sync:
                        sync(sel, priority, reference)
                    else:
                        change(sel, priority)
                else:
                    if self.sync:
                        sync(sel, priority, reference)

    def calculate_distances(self):
        for sel_member in self.entity.members:
            sel_member = self.entity.members[0]
            self.nears = {}
            def find(member, first, priority:int=1):
                articulations = member.articulations
                todo = []
                for articulation in articulations:
                    other = articulation.member_a
                    if other == sel_member:
                        other = articulation.member_b
                    if not other in self.nears.keys() and other != first:
                        self.nears[other] = {
                            "priority": priority,
                            "id": other.id
                        }
                        todo.append([find, (other, first, priority + 1)])
                for _ in todo:
                    func = _[0]
                    args = _[1]
                    func(*args)
            find(sel_member, sel_member)
            sel_member.nears = self.nears

    def __drag_member(self, event, _):
        x, y = event.x, event.y
        member = _[0]
        oval = _[1]
        dx = x - member.x
        dy = y - member.y
        self.canvas.move(oval, dx, dy)
        member.x = x
        member.y = y
        self.calculate_distances()
        self.update_entity()
        self.update_entity_positions(False, member)

    def bind_drag(self):
        for _ in self.members:
            member = _[0]
            oval = _[1]
            text = _[2]
            self.canvas.tag_bind(oval, "<B1-Motion>", lambda event, ink=_: self.__drag_member(event, ink))
            self.canvas.tag_bind(text, "<B1-Motion>", lambda event, ink=_: self.__drag_member(event, ink))

    def update_loop(self):
        self.calculate_distances()
        self.update_entity_positions()
        self.update_entity()
        self.root.update()
        self.root.after(int(self.interval_delay * 1000), self.update_loop)

    def update_loop_neuronal(self):
        self.calculate_distances()
        self.update_entity_positions()

    def update_loop_fluxes(self, move:bool=False):
        if move:
            self.calculate_distances()
            self.update_entity_positions()
        for information in self.entity.informations:
            information.do()
        self.update_entity()
        self.root.update()
        self.root.after(int(self.interval_delay * 1000), lambda: self.update_loop_fluxes(move))

    def right_button_menu(self, event): 
        try: 
            self.rc_menu.tk_popup(event.x_root, event.y_root) 
        finally: 
            self.rc_menu.grab_release()

    def reload(self):
        self.entity.__init__(*self.entity.args_saves)
        self.canvas.delete("all")
        self.members = []
        self.articulations = []
        self.indicators = []
        self.draw_entity()
        self.bind_drag()

    def rest(self):
        self.rc_menu = tk.Menu(self.root, tearoff=0)
        self.rc_menu.add_command(label="Create member")
        self.rc_menu.add_command(label="Create articulation")
        self.rc_menu.add_command(label="Delete member")
        self.rc_menu.add_command(label="Delete articulation")
        self.rc_menu.add_command(label="Reload entity", command=self.reload)

        self.root.bind("<Button-3>", self.right_button_menu)

    def run(self, process:str="move"):
        self.process = process
        self.rest()
        if process == "move":
            self.draw_entity()
            self.root.after(1000, self.update_loop)
            self.root.mainloop()
        elif process == "static":
            self.draw_entity()
            self.root.mainloop()
        elif process == "edit":
            self.draw_entity()
            self.bind_drag()
            self.root.mainloop()
        elif process == "editmove":
            self.draw_entity()
            self.bind_drag()
            self.root.after(1000, self.update_lop)
            self.root.mainloop()
        elif process == "create":
            self.draw_entity()
            self.bind_drag()
            self.root.mainloop()
        elif process == "fluxes":
            self.draw_entity()
            self.root.after(1000, self.update_loop_fluxes)
            self.root.mainloop()
        elif process == "movefluxes":
            self.draw_entity()
            self.root.after(1000, lambda: self.update_loop_fluxes(True))
            self.root.mainloop()
        elif process == "editfluxes":
            self.draw_entity()
            self.bind_drag()
            self.root.after(1000, self.update_loop_fluxes)
            self.root.mainloop()
        elif process == "editmovefluxes":
            self.draw_entity()
            self.bind_drag()
            self.root.after(1000, lambda: self.update_loop_fluxes(True))
            self.root.mainloop()
        else:
            self.draw_entity()
            self.root.after(1000, self.update_loop)
            self.root.mainloop()