import time
import tkinter as tk
import random as rd

MAX_WIDTH = 1200
MAX_HEIGHT = 900
MARGE = 40

class Articulation():
    def __init__(self, entity, member_a, member_b) -> None:
        self.entity = entity
        self.member_a = member_a
        self.member_b = member_b

class Member():
    def __init__(self, entity) -> None:
        self.id = rd.randint(100000, 999999)
        self.parent = entity
        self.articulations = []

        self.x = rd.randint(MARGE, MAX_WIDTH - MARGE)
        self.y = rd.randint(MARGE, MAX_HEIGHT - MARGE)

class Entity():
    def __init__(self, members:int=6, choice:bool=False) -> None:
        self.id = rd.randint(100000, 999999)

        self.members = []
        self.articulations = []

        for member in range(1, members, 2):
            a = Member(self)
            if len(self.members):
                for b in self.members.copy():
                    if choice:
                        if rd.randint(1, len(self.members)) == 1:
                            articulation = Articulation(self, a, b)
                            a.articulations.append(articulation)
                            b.articulations.append(articulation)
                            self.articulations.append(articulation)
                    else:
                        articulation = Articulation(self, a, b)
                        a.articulations.append(articulation)
                        b.articulations.append(articulation)
                        self.articulations.append(articulation)
                self.members.append(a)
            else:
                b = Member(self)
                articulation = Articulation(self, a, b)
                a.articulations.append(articulation)
                b.articulations.append(articulation)
                self.members.append(a)
                self.members.append(b)
                self.articulations.append(articulation)

class Board():
    def __init__(self, entity:Entity, thickness:int=10, width:int=40, height:int=40, width_mul:bool=False, mul_divid:float=1.5, min_speed:int=1, max_speed:int=10, interval_delay:float=1) -> None:
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

    def draw_entity(self):
        self.canvas.create_text(10, 10, text=f"{self.entity.id} ; {len(self.entity.members)} members ; {len(self.entity.articulations)} articulations", fill="black", anchor="nw")
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
            t = self.canvas.create_text(member.x + int(width_ / 2), member.y - int(height_ / 2), text=f"{member.x} ; {member.y} ; {member.id} ; {len(member.articulations)} ar", fill="red")
            self.members.append([member, o, t])
        
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
            self.canvas.itemconfig(text, text=f"{member.x} ; {member.y} ; {member.id} ; {len(member.articulations)} ar")
        for _ in self.articulations:
            articulation = _[0]
            line = _[1]
            self.canvas.coords(line, articulation.member_a.x + int(width / 2), articulation.member_a.y + int(height / 2), articulation.member_b.x + int(width / 2), articulation.member_b.y + int(height / 2))

    def update_entity_positions(self):
        for member in self.entity.members:
            directions = ["none", "left", "right", "top", "bottom", "left_top", "right_top", "left_bottom", "right_bottom"]
            rand = rd.choice(directions)
            speed = rd.randint(self.min_speed, self.max_speed)
            if not rand == "none":
                if rand == "left":
                    member.x -= speed
                elif rand == "right":
                    member.x += speed
                elif rand == "top":
                    member.y -= speed
                elif rand == "bottom":
                    member.y += speed
                elif rand == "left_top":
                    member.x -= speed
                    member.y -= speed
                elif rand == "right_top":
                    member.x += speed
                    member.y -= speed
                elif rand == "left_bottom":
                    member.x -= speed
                    member.y += speed
                elif rand == "right_bottom":
                    member.x += speed
                    member.y += speed

    def update_loop(self):
        self.update_entity_positions()
        self.update_entity()
        self.root.update()
        self.root.after(int(self.interval_delay * 1000), self.update_loop)

    def run(self):
        self.draw_entity()
        self.root.after(1000, self.update_loop)
        self.root.mainloop()