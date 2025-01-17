import logging
import threading
import time

def thread_function():
    logging.info("Thread %s: starting")
    time.sleep(2)
    logging.info("Thread %s: finishing")

if __name__ == "__main__":
    import gtk
    width = gtk.gdk.screen_width()
    height = gtk.gdk.screen_height()
    print(width)
    print(height)

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, daemon=True)
    logging.info("Main    : before running thread")
    x.start()
    logging.info("Main    : wait for the thread to finish")
    # x.join()
    logging.info("Main    : all done")