#!/usr/bin/env python3

from tkinter import LEFT, RIGHT
import customtkinter as ctk 
import socket
import threading
import time


class Ventana:

    def __init__(self,root, cl, username):
        self.root = root
        self.cl = cl
        self.username = username

        self.root.title("Cliente")
        self.root.geometry('700x500')

        self.root.protocol("WM_DELETE_WINDOW", self.salir)


        area = ctk.CTkTextbox(root, state='disabled', font=('CaskaydiaMono Nerd Font',20))
        area.pack(pady=10, padx=10, fill="both" ,expand = True)


        frame = ctk.CTkFrame(root, bg_color='transparent')
        frame.pack(fill="both")

        txt_mensaje = ctk.CTkEntry(frame, font=('CaskaydiaMono Nerd Font',17))
        txt_mensaje.bind("<Return>", lambda _:self.mandar_mensaje(area, txt_mensaje)) #recoje el evento de dar enter
        txt_mensaje.pack(fill="both",expand= True, side=LEFT,padx=10, pady=10 )

        btn_enviar = ctk.CTkButton(frame, text="Enviar", command=lambda:self.mandar_mensaje(area, txt_mensaje))
        btn_enviar.pack(side=RIGHT, padx=5, pady=5)

        btn_listar = ctk.CTkButton(root, text="Listar Usuarios", command=self.listar_usuarios)
        btn_listar.pack(side=RIGHT)

        btn_salir = ctk.CTkButton(root, text="Salir", command=self.salir)
        btn_salir.pack(side=LEFT)

        hilo_escucha = threading.Thread(target=self.recivir_mensaje, args=(area,))
        hilo_escucha.daemon = True
        hilo_escucha.start()

    def salir(self):
        try:
            mensaje = "!exit"
            self.cl.sendall(mensaje.encode())
            time.sleep(0.1)
            self.cl.close()
        except:
            pass

        self.root.quit()
        self.root.destroy()


    def listar_usuarios(self):
        try: 
            mensaje = "!users"
            self.cl.sendall(mensaje.encode())
        except:
            pass


    def mandar_mensaje(self, area, txt_mensaje):
        mensaje = txt_mensaje.get()
        if mensaje:
            self.cl.sendall(f"{self.username}: {mensaje}".encode())
            txt_mensaje.delete(0, ctk.END)
            area.configure(state='normal')
            area.insert(ctk.END,f"{self.username}: {mensaje}\n")
            area.configure(state='disabled')

    def recivir_mensaje(self, area):

        while True:
            try:
                mensaje = self.cl.recv(1024).decode()
                if mensaje:
                    area.configure(state='normal')
                    area.insert(ctk.END, f"{mensaje}\n")
                    area.see(ctk.END)
                    area.configure(state='disabled')
            except Exception:
                break

def cliente():

    host = 'localhost'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cl:

        cl.connect((host, port))
        username = input("Ingresa tu usuario -> ")
        cl.sendall(username.encode())
        root = ctk.CTk()
        app = Ventana(root, cl, username)
        root.mainloop()


if __name__ == '__main__':
    cliente()
