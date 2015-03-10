import socket
import sys
import base64
import threading

import numpy
import cv2


frame = None
die = False

def usage():
  print 'Usage : {0} <ip>'.format(sys.argv[0])
  print 'ip : FirefoxOS IP address on your local network'


def update_frame(aData):
  #remove the header
  data = aData.replace('data:image/png;base64,', '')
  # base64 decode
  global frame
  frame = base64.b64decode(data)


class ThreadedConn(threading.Thread):
  def run(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      s.connect((sys.argv[1], 8080))
    except Exception as e:
      print e
      sys.exit(-1)


    the_data = ""
    while True:
      if(die):
        break
      data = s.recv(1024)
      if(data.startswith('data:')):
        # update the image
        update_frame(the_data)
        # restart the process
        the_data = data
      else:
        the_data = the_data + data


if __name__ == '__main__':

  if(len(sys.argv) < 2):
    usage()
    sys.exit(-1)

  th = ThreadedConn(name="Connection deamon")
  th.start()

  print "Press Ctrl-C to close the program." 



  try:
    while True:
      if frame is not None:
        img = cv2.imdecode(numpy.frombuffer(frame, numpy.uint8), 
            cv2.CV_LOAD_IMAGE_COLOR)

        if img is not None:
          cv2.imshow("FireCam", img)
          cv2.waitKey(30)
  except KeyboardInterrupt as e:
    print "Killing Connection thread"
    die = True




