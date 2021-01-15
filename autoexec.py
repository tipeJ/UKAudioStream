import xbmc
import time
import httpd

class UKAudioCast():
    def __init__(self):
        monitor = xbmc.Monitor()

        srv = httpd.TinyWebServer(self)
        srv.create("localhost", 8090)
        srv.start()
        while not monitor.abortRequested():
            if (monitor.waitForAbort(10)):
                # Abort was requested while waiting. Exit
                break
            player = xbmc.Player()
            if player.isPlaying():
                xbmc.log("UKACAST: Player is playing following audio streams: %s" % player.getAvailableAudioStreams(), level=xbmc.LOGINFO)
            else:
                xbmc.log("hello addon! %s" % time.time(), level=xbmc.LOGINFO)

if __name__ == '__main__':
    caster = UKAudioCast()
