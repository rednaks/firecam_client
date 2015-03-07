import socket
import sys


def usage():
  print 'Usage : {0} <ip>'.format(sys.argv[0])
  print 'ip : FirefoxOS IP address on your local network'


if __name__ == '__main__':

  if(len(sys.argv) < 2):
    usage()
    sys.exit(-1)

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    s.connect((sys.argv[1], 8080))
  except Exception as e:
    print e
    sys.exit(-1)

  the_data = ""
  while True:
    data = s.recv(1024)
    if(data.startswith('data:')):
      # update the image TODO

      # restart the process
      the_data = data
    else:
      the_data = the_data + data

