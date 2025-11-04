#!/usr/bin/env python3

import socket
import ssl 
import threading

def hilos_clientes(cl, clientes, username):
    user = cl.recv(1024).decode()
    username[cl] = user
    print(f"[+] Se ha conectado {user}")

    for cliente in clientes:
        if cliente is not cl:
            cliente.sendall(f"\n[+] El usuario {user} se unio".encode())

    while True:

        try:
            mensaje = cl.recv(1024).decode()

            if mensaje == "!users":
                cl.sendall(f"\n[+] Listando usuarios:\n\n{','.join(username.values())}".encode())
                continue
            elif mensaje == "!exit":
                for cliente in clientes:
                    if cliente is not cl:
                        cliente.sendall(f"\n[-] El usuario {user} abandono el chat :(".encode())
                break

            elif not mensaje:
                break
            else:
                for cliente in clientes:
                    if cliente is not cl:
                        cliente.sendall(mensaje.encode())
        except:
            break

    try:
        cl.close()
        clientes.remove(cl)
        del username[cl]
    except:
        pass


def servidor():

    host = '0.0.0.0'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sv:
        sv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Para no esperar timeweit
        sv.bind((host, port))

         # Configura SSL con contexto moderno
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile="server-cert.pem", keyfile="server-key.key")
        #

        sv.listen()
        print('[+] En escucha ...')

        clientes = [] #lista
        username = {} #diccionario

        while True:

            cl,addr = sv.accept() # aceptanos la coneccion entrante
            #
            cl = context.wrap_socket(cl, server_side=True)  # ← aquí se cifra la conexión
            #
            clientes.append(cl)
            hilo_c = threading.Thread(target=hilos_clientes, args=(cl,clientes,username))
            hilo_c.daemon = True
            hilo_c.start() # iniciamos le hilo




if __name__ == '__main__':
    servidor()
