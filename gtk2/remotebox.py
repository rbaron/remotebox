import rb
import rhythmdb

import threading
import socket
import time
import string
import re
import base64

# Empty HOST - INADDR_ANY
HOST = ''
PORT = 30666
BUFFSIZE = 4096

#class RemoteboxPlugin(GObject.Object, Peas.Activatable):
class RemoteboxPlugin(rb.Plugin):
    def __init__(self):
        super(RemoteboxPlugin, self).__init__()

    def activate(self, shell):
        print "Hello Remotebox!"
        self.shell = shell;

        # Start a new thread, pass self.object = self.shell as argument
        t = MyThread(self.shell)
        t.daemon = True
        t.start()

    def deactivate(self, shell):
        print "Goodbye Remotebox!"

class SockServer:
  def __init__(self):
    self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.addr = (HOST, PORT)
    self.sock.bind(self.addr)
    self.sock.listen(1)

  #Blocks here until someone connects
  def accept(self):
    (self.clientSock, self.clientAddr) = self.sock.accept()
    print "Client connected!"

  def receive(self):
    self.buff = self.clientSock.recv(BUFFSIZE)
    return self.buff

  def send(self, text):
    self.clientSock.send(text)

  def cleanup(self):
    self.clientSock.close()

class MyThread(threading.Thread):
  def __init__(self, RBShell):
    super(MyThread, self).__init__()
    self.srv = SockServer()
    self.shell = RBShell
    self.player = RBShell.get_player()
    self.db = self.shell.props.db

  def run(self):
    while(1):
      print "Accepting..."
      self.srv.accept()
      while(1):
        print "Receiving..."
        try:
          self.buff = self.srv.receive()
    
          if len(self.buff) == 0: 
            print "Received 0 bytes. Assuming disconnection."
            break
  
          print "Received: ",self.buff

          parts = string.split(self.buff)

          # Try to run rhythmbox api functions
          try:

            if parts[0] == "play":
              # Is there a song selected?
              if self.player.get_playing_entry():
                try:
                  self._play()
                  self.srv.send("ok\n")
                except Exception, e:
                  self.srv.send("Error on play: no track selected!\n")
              else:
                self.srv.send("Error on play: no track selected!\n")

            elif parts[0] == "pause":
              try:
                self._pause()
                self.srv.send("ok\n")
              except Exception, e:
                self.srv.send("Error on pause: no track selected!\n")

            elif parts[0] == "stop":
              try:
                self._stop()
                self.srv.send("ok\n")
              except Exception, e:
                self.srv.send("Error on stop: no track selected!\n")

            elif parts[0] == "next":
              try:
                self._next()
                self.srv.send("ok\n")
              except Exception, e:
                self.srv.send("Error on next: no track selected!\n")

            elif parts[0] == "prev":
              try:
                self._prev()
                self.srv.send("ok\n")
              except Exception, e:
                self.srv.send("Error on prev: no track selected!\n")

            elif parts[0] == "goto":
                self._goto(parts[1])
                self.srv.send("ok\n")

            elif parts[0] == "vol":
                if len(parts) == 1:
                  print "Volume: "+str(self._getVol())
                  #self.srv.send("ok\n")
                  self.srv.send(str(self._getVol())+"\n")

                else:
                  # Try to convert to float
                  try:
                    if float(parts[1]) <= 1 and float(parts[1]) >= 0:
                      print "Set volume to "+str(float(parts[1]))
                      self._setVol(float(parts[1]))
                      self.srv.send("ok\n")
                    else:
                      print "Invalid volume setting."
                      self.srv.send("Invalid volume setting.\n")
                  except Exception, e:
                    print "Invalid volume setting."
                    self.srv.send("Invalid volume setting.\n")
                  
            # Big string. First sends the size in bytes. Then keeps sending BUFFSIZE bytes per loop
            elif parts[0] == "list":
                xml = self._getTrackList()

                # Send size
                self.srv.send(str(len(xml))+"\n")

                # Send xml list
                ptr = 0;
                while(1):
                  end = ptr+BUFFSIZE
                  if end > len(xml):
                    end = len(xml)-1
                  chunk = xml[ptr:(ptr+BUFFSIZE)]
                  self.srv.send(chunk)
                  if end == len(xml)-1:
                    #Send EOL
                    self.srv.send("\n")
                    break
                  else:
                    ptr = ptr + BUFFSIZE

            else:
                self.srv.send("Unrecognized input.\n")

          except Exception, e:
            print "Error while running rhythmbox api functions", str(e)
            pass

        except Exception, e:
          print "Receiving failed! Assuming disconnection...", str(e)
          break
  
  def _play(self):
    self.player.play()

  def _pause(self):
    self.player.pause()
    
  def _stop(self):
    self.player.stop()

  def _next(self):
    self.player.do_next()

  def _prev(self):
    self.player.do_previous()

  def _getVol(self):
    return self.player.get_volume()

  def _setVol(self, vol):
    if vol > 1.0:
      vol = 1.0
    elif vol < 0.0:
      vol = 0.0
    self.player.set_volume(vol)

  def _goto(self, trackuri):
    if trackuri:
      # Find entry by uri
      entry = self.db.entry_lookup_by_location(trackuri)

      # Source = main library (all local songs)
      source =  self.shell.props.library_source

      #print "Entry title: ",entry.get_string(RB.RhythmDBPropType.TITLE)
      self.player.play_entry(entry, source)

  def _getTrackList(self):

    xml = "<xml version='1.0' encoding='utf-8'><tracks>"

    # TODO: find a way to list every item im library, not only what user sees in the UI (query)
    # I couldn't find the GTK2 equivalente of GTK3's base_query_model
    #print dir(self.shell.props.library_source.props)

    for row in self.shell.props.library_source.props.query_model:
      entry = row[0]

      artist = base64.b64encode(self.db.entry_get(entry, rhythmdb.PROP_ARTIST))
      title= base64.b64encode(self.db.entry_get(entry, rhythmdb.PROP_TITLE))
      album = base64.b64encode(self.db.entry_get(entry, rhythmdb.PROP_ALBUM))
      url = base64.b64encode(self.db.entry_get(entry, rhythmdb.PROP_LOCATION))

      xml += "<track>"
      xml += "<artist>"+artist+"</artist>"
      xml += "<title>"+title+"</title>"
      xml += "<album>"+album+"</album>"
      xml += "<url>"+url+"</url>"
      xml += "</track>"

    xml += "</tracks></xml>"

    return xml
