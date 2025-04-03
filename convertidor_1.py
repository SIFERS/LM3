#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 07:51:15 2022

@author: zncg
"""

import tkinter

ventana = tkinter.Tk()
ventana.geometry('400x300')

etiqueta = tkinter.Label(ventana, text ='eV -> nm', font='Helvetica 30')
etiqueta.pack()


textBox = tkinter.Entry(ventana, font='Helvetica 15')
textBox.pack()

def ev2nm():
    evs = eval(textBox.get())
    nms= 1239.841/evs
    resultado['text']=nms

resultado = tkinter.Label(ventana, font='Hlevetica 25')
resultado.pack()

botonConvertir = tkinter.Button(ventana, text='Convertir', padx=40, pady=50,
                                command=ev2nm)
botonConvertir.pack()


ventana.mainloop()
