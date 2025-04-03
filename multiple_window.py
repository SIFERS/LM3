#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 11:45:40 2022

@author: zncg
"""

import tkinter as tk

def New_Window():
    Window = tk.Toplevel()
    canvas = tk.Canvas(Window, height=HEIGHT, width=WIDTH)
    canvas.pack()
    etiqueta = tk.Label(Window,text='Algo')
    etiqueta.pack()
    boton = tk.Button(Window,text='da click para imprimir', 
                   command=lambda: print('cualquier cosa'))
    boton.pack()

HEIGHT = 300
WIDTH = 500

ws = tk.Tk()
ws.title("Python Guides")
canvas = tk.Canvas(ws, height=HEIGHT, width=WIDTH)
canvas.pack()

button = tk.Button(ws, text="Click ME", bg='White', fg='Black',
                              command=lambda: New_Window())



button.pack()
ws.mainloop()