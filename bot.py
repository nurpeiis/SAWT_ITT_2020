
import subprocess
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

AUDIO = range(1)

def start(update, context):
    """ 
        Welcome Message
    """
    update.message.reply('Welcome to SAWT bot! \n\n I am Automatic Speech Recogniser! \n\n Press Audio recording Button and record a sentence in English')

    return AUDIO


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

def analyze(update, context):
    """ 
        Given Audio File it will perform S2T using DeepSpeech
    """
    pass

def cancel(update, context):
    update.message.reply_text('GoodBye!!!')

def main():
    updater = Updater("TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            AUDIO: [MessageHandler(Filters.audio, analyze)],
        },
        allow_reentry=True,
        fallbacks=[CommandHandler('cancel', cancel)]
    )


if __name__ == '__main__':
    main()