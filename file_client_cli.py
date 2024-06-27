import socket
import json
import base64
import logging

server_address = ('0.0.0.0', 8080)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message")
        sock.sendall(command_str.encode())
        data_received = ""
        while True:
            data = sock.recv(4096)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except Exception as e:
        logging.warning(f"error during data receiving: {e}")
        return False
    finally:
        sock.close()

def remote_list():
    command_str = "LIST"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        with open(namafile, 'wb+') as fp:
            fp.write(isifile)
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filename="", chunk_size=4096):
    try:
        with open(filename, 'rb') as fp:
            while True:
                chunk = fp.read(chunk_size)
                if not chunk:
                    break
                filedata = base64.b64encode(chunk).decode()
                command_str = f"UPLOAD {filename} {filedata}"
                hasil = send_command(command_str)
                if hasil['status'] != 'OK':
                    print("Upload gagal")
                    return False
        print("Upload berhasil")
        return True
    except FileNotFoundError:
        print("File tidak ditemukan")
        return False

def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print("Hapus berhasil")
        return True
    else:
        print("Hapus gagal")
        return False

if __name__ == '__main__':
    server_address = ('172.16.16.101', 8080)
    
    while True:
        print("\nPilihan:")
        print("1. List - remote_list()")
        print("2. Upload - remote_upload('namafile')")
        print("3. Delete - remote_delete('namafile')")
        print("4. Get - remote_get('namafile')")
        print("5. Keluar dari program")

        pilihan = input("Masukkan pilihan (1/2/3/4/5): ")

        if pilihan == '1':
            remote_list()
        elif pilihan == '2':
            filename = input("Masukkan nama file untuk diupload: ")
            remote_upload(filename)
        elif pilihan == '3':
            filename = input("Masukkan nama file untuk dihapus: ")
            remote_delete(filename)
        elif pilihan == '4':
            filename = input("Masukkan nama file untuk diunduh: ")
            remote_get(filename)
        elif pilihan == '5':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Masukkan angka 1 sampai 5.")
