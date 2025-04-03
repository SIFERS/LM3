#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 08:39:49 2022

@author: zncg
"""

import tkinter
import tkinter.font as tkFont

ventana = tkinter.Tk()
ventana.geometry('800x100')
fontExample = tkFont.Font(family="Arial", size=15)

etiqueta = tkinter.Label(ventana, text ='eV -> nm', font=fontExample)

textBox = tkinter.Entry(ventana, font=fontExample)
salida = tkinter.Text(ventana,height = 1,
              width = 20,
              bg = "light cyan",font=fontExample)
def ev2nm():
    evs = eval(textBox.get())
    nms= round(1239.841/evs,5)
    salida.delete('1.0', 'end')
    salida.insert('1.0', nms)


botonConvertir = tkinter.Button(ventana, text='Convertir', padx=40,
                                command=ev2nm, font=fontExample)


etiqueta.grid(row=0,column=0)
textBox.grid(row=0, column=2)
botonConvertir.grid(row=0,column=3)
salida.grid(row=0,column=4)

ventana.mainloop()

