
from telegram import Updater, CommandHandle

def start(update, source):
    """ 
        Welcome Message
    """

def convert(src_file, dst_file):
    """ 
        Converts 48000Hz ogg format to 16000Hz wav format 
    """
    rate = 16000
    cmd = f"ffmpeg -i {src_file} -ar {rate} {dst_file} -y"

    with subprocess.Popen(cmd.split()) as p:
        try:
            p.wait(timeout=2)
        except:
            p.kill()
            p.wait()
            return False
    return True