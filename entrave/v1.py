import tkinter as tk
import random as rd

MAX_WIDTH = 1200
MAX_HEIGHT = 900

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

        self.x = rd.randint(1, MAX_WIDTH)
        self.y = rd.randint(1, MAX_HEIGHT)

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
    def __init__(self, entity:Entity, thickness:int=10, width:int=40, height:int=40, width_mul:bool=False, mul_divid:float=1.5) -> None:
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

    def draw_entity(self):
        self.canvas.create_text(10, 10, text=f"{self.entity.id} ; {len(self.entity.members)} members ; {len(self.entity.articulations)} articulations", fill="black", anchor="nw")
        width, height = self.width, self.height
        for member in self.entity.members:
            color = "#343434"
            for articulation in member.articulations:
                self.canvas.create_line(articulation.member_a.x + int(width / 2), articulation.member_a.y  + int(height / 2), articulation.member_b.x  + int(width / 2), articulation.member_b.y  + int(height / 2), fill=color, width=self.thickness)
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
            self.canvas.create_oval(member.x - width * mul, member.y - height * mul, member.x + width_, member.y + height_, fill=color)
            self.canvas.create_text(member.x + int(width_ / 2), member.y - int(height_ / 2), text=f"{member.x} ; {member.y} ; {member.id} ; {len(member.articulations)} ar", fill="red")

    def run(self):
        self.draw_entity()
        self.root.mainloop()