import socket
import argparse
import crypt

def readFile(fname):
    try:
        with open(fname, 'rb') as f:
            inf = f.read()
    except IOError:
        exit('No such file or directory ' + fname)
    return inf	

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('inFile_text')
    parser.add_argument('Vig_key')
    parser.add_argument('AES_key')
    parser.add_argument('imagefile')
    parser.add_argument('host')
    parser.add_argument('port')
    return parser.parse_args()	
	
def send(data, host, port):
    sock = socket.socket()
    try:
        sock.connect((host, int(port)))
        print('Connection with ' + host)
    except socket.error:
        exit('Error connection with ' + host)
    sock.send(data)
    print 'Message sent!'
    sock.close()

def main():

    args = getArgs()
    data = readFile(args.inFile_text)
    Vig_key = readFile(args.Vig_key)
    AES_key = readFile(args.AES_key)
    res = crypt.main(data, Vig_key, AES_key, args.imagefile)
    print '________'
    send(res, args.host, args.port)
	
if __name__ == '__main__':
    main()	
