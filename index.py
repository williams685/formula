"""
Title: One Formula That Demystifies 3D Graphics
Reference: https://github.com/tsoding/formula
"""
import tkinter as tk
import math

import cube
import penger

def clear() -> None:
    canvas.delete("all")


def point(**p) -> None:
    size = 20
    canvas.create_rectangle(p["x"] - size / 2,
                            p["y"] - size / 2, 
                            (p["x"] - size / 2) + size, 
                            (p["y"] - size / 2) + size, 
                            fill="#50FF50")


def line(p1:dict, p2:dict) -> None:
    canvas.create_line(
        p1["x"],
        p1["y"],
        p2["x"],
        p2["y"],
        fill="#50FF50",
        smooth=True,
        width=3
    )

    
def screen(**p) -> dict:
    # -1..1 => 0..2 => 0..1 => 0..w
    return {
        "x": (p["x"] + 1) / 2 * game_width,
        "y": (1 - (p["y"] + 1) / 2) * game_height
    }


def project(**p) -> dict:
    return {
        "x": p["x"] / p["z"],
        "y": p["y"] / p["z"]
    }


def translate_z(dz, /, **p) -> dict:
    return {"x":p["x"], "y":p["y"], "z": p["z"] + dz}


def rotate_xz(angle, /, **p) -> dict:
    c = math.cos(angle)
    s = math.sin(angle)
    return {
        "x": p["x"] * c - p["z"] * s,
        "y": p["y"],
        "z": p["x"] * s + p["z"] * c
    }


def frame() -> None:
    global angle
    dt = 1 / fps
    angle += math.pi * dt
    clear()
    # for v in vs:
    #     res = rotate_xz(angle, x=v["x"], y=v["y"], z=v["z"])
    #     res = translate_z(dz, x=res['x'], y=res["y"], z=res['z'])
    #     res = project(x=res["x"], y=res["y"], z=res["z"])
    #     res = screen(x=res["x"], y=res["y"])
    #     point(x=res["x"], y=res["y"])

    for f in fs:
        for i in range(len(f)):
            a = vs[f[i]]
            b = vs[f[(i+1) % len(f)]]
            res1 = rotate_xz(angle, x=a["x"], y=a["y"], z=a["z"])
            res1 = translate_z(dz, x=res1['x'], y=res1["y"], z=res1['z'])
            res1 = project(x=res1["x"], y=res1["y"], z=res1["z"])
            res1 = screen(x=res1["x"], y=res1["y"])

            res2 = rotate_xz(angle, x=b["x"], y=b["y"], z=b["z"])
            res2 = translate_z(dz, x=res2['x'], y=res2["y"], z=res2['z'])
            res2 = project(x=res2["x"], y=res2["y"], z=res2["z"])
            res2 = screen(x=res2["x"], y=res2["y"])
            line(res1, res2)

    root.after(int(1000/fps), frame)



if __name__ == "__main__":
    game_width  = 600
    game_height = 600
    dz = 1
    fps = 60
    angle = 0
    # vs = penger.vs
    # fs = penger.fs
    vs = cube.vs
    fs = cube.fs
    
    root = tk.Tk()
    root.title("The 3D Graphics By Implemented With A Formula")
    root.geometry("600x600+400+50")
    root.resizable(False, False)
    canvas = tk.Canvas(root, 
                       width=game_width, 
                       height=game_height,
                       background="#101010")
    canvas.pack(padx=10, pady=10)
    root.after(int(1000/fps), frame)
    root.mainloop()