import json
import logging
import shlex

from file_interface import FileInterface

"""
* class FileProtocol bertugas untuk memproses 
data yang masuk, dan menerjemahkannya apakah sesuai dengan
protokol/aturan yang dibuat

* data yang masuk dari client adalah dalam bentuk bytes yang 
pada akhirnya akan diproses dalam bentuk string

* class FileProtocol akan memproses data yang masuk dalam bentuk
string
"""


class FileProtocol:
    def __init__(self):
        self.file = FileInterface()

    def proses_string(self, string_datamasuk=''):
        logging.warning(f"string diproses: {string_datamasuk}")
        c = shlex.split(string_datamasuk)
        try:
            c_request = c[0].strip().lower()  # Mengubah ke huruf kecil di sini
            logging.warning(f"memproses request: {c_request}")
            params = [x for x in c[1:]]
            cl = getattr(self.file, c_request)(params)
            return json.dumps(cl)
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            return json.dumps(dict(status='ERROR', data='request tidak dikenali'))

if __name__ == '__main__':
    fp = FileProtocol()
    print(fp.proses_string("list"))
    print(fp.proses_string("get pokijan.jpg"))
    print(fp.proses_string(f"upload test_upload.jpg {base64.b64encode(b'test content').decode()}"))
    print(fp.proses_string("delete test_upload.jpg"))
