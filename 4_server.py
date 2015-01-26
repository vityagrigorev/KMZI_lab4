import socket
import argparse
import decrypt

def readFile(fname):
    try:
        with open(fname, 'rb') as f:
            inf = f.read()
    except IOError:
        exit('No such file or directory ' + fname)
    return inf	
        
def writeFile(inf):
    f = open("out.txt", 'wb')
    f.write(''.join(inf))
		
def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('Vig_key')
    parser.add_argument('AES_key')
    parser.add_argument('port')
    return parser.parse_args()	
		
def get(port):
    sock = socket.socket()
    sock.bind(('', int(port)))
    sock.listen(1)
    try:
        sock.settimeout(60)
        conn, addr = sock.accept()
        sock.settimeout(None)
    except socket.timeout:
        exit('Connection timed out')
    except socket.error:
        exit('Error of connection')
    print('Connected:', addr)
    data = bytes()
    tmp = conn.recv(1024)
    while tmp:
        data += tmp
        tmp = conn.recv(1024)

    print 'Message received!'
    print '________'
    conn.close()
    sock.close()
    return data
        
def main():
    args = getArgs()
    Vig_key = readFile(args.Vig_key)
    AES_key = readFile(args.AES_key)
    img = get(args.port)
    final_value = decrypt.main(Vig_key, AES_key, 'step_image.png')
    writeFile(final_value)
    print '________'
    print 'End'

if __name__ == '__main__':
    main()
