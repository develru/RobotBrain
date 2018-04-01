__author__ = 'develru'

# import cameratool
import TCPHandler

if __name__ == '__main__':
    # cam = cameratool.Capture()
    # cam.show_image()
    # cam.close()
    handler = TCPHandler.MainHandler('localhost', 9999)
    handler.main_run()