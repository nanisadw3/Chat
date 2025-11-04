# Chat Multiusuario Cifrado con CustomTkinter

Este es un proyecto de chat multiusuario desarrollado en Python que utiliza `customtkinter` para la interfaz gráfica y cifrado SSL/TLS para garantizar la seguridad de las comunicaciones.

## Características

*   **Interfaz Gráfica Atractiva:** Interfaz de usuario moderna y personalizable gracias a `customtkinter`.
*   **Comunicación Segura:** Todos los mensajes entre el cliente y el servidor están cifrados utilizando SSL/TLS.
*   **Multiusuario:** El servidor puede gestionar múltiples clientes de forma simultánea.
*   **Comandos Especiales:**
    *   `!users`: Muestra una lista de todos los usuarios conectados al chat.
    *   `!exit`: Permite a un usuario desconectarse de forma segura del chat.

## Requisitos

*   Python 3.x
*   La librería `customtkinter`. Puedes instalarla usando pip:
    ```bash
    pip install customtkinter
    ```
*   `openssl` para generar los certificados de seguridad.

## Instalación y Uso

Sigue estos pasos para poner en marcha el chat:

**1. Clona el Repositorio**

```bash
git clone <URL-del-repositorio>
cd <nombre-del-directorio>
```

**2. Genera los Certificados SSL**

El servidor requiere un certificado y una clave privada para establecer una conexión segura. Ejecuta los siguientes comandos en tu terminal para generarlos:

```bash
openssl genpkey -algorithm RSA -out server-key.key -aes256
openssl req -new -key server-key.key -out server.csr
openssl x509 -req -days 365 -in server.csr -signkey server-key.key -out server-cert.pem
openssl rsa -in server-key.key -out server-key.key
```

Esto creará los archivos `server-cert.pem` y `server-key.key` necesarios para el servidor.

**3. Inicia el Servidor**

Abre una terminal y ejecuta el siguiente comando para iniciar el servidor. Este permanecerá a la espera de conexiones entrantes.

```bash
python server.py
```

Deberías ver el mensaje `[+] En escucha ...`, indicando que el servidor está listo.

**4. Inicia uno o más Clientes**

Abre una nueva terminal por cada cliente que quieras conectar. Al ejecutar el script, se te solicitará un nombre de usuario.

```bash
python client.py
```

Tras introducir un nombre de usuario, se abrirá la ventana del chat y podrás empezar a comunicarte.

## Aviso

Este proyecto utiliza un certificado SSL autofirmado con fines de demostración. En un entorno de producción, deberías utilizar un certificado emitido por una Autoridad de Certificación (CA) reconocida para garantizar la máxima seguridad.
