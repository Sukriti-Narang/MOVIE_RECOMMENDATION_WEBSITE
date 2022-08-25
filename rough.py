from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *

def main():
    import time
    
    put_processbar('bar');
    for i in range(1, 11):
        set_processbar('bar', i / 10)
        time.sleep(0.1)

start_server(main, port=8080, debug=True)
