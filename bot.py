
import subprocess
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

import datetime
import os 

AUDIO = range(1)

def start(update, context):
    """ 
        Welcome Message
    """
    update.message.reply_text('Welcome to SAWT bot! \n\n I am Automatic Speech Recogniser! \n\n Press Audio recording Button and record a sentence in English')
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
    #update.message.voice.file_id
    file = context.bot.getFile(update.message.voice.file_id)
    src_file = './audio/voice.ogg'
    file.download(src_file)
    dst_file = './audio/voice.wav'
    convert(src_file, dst_file)
    proc = subprocess.Popen(['deepspeech --model deepspeech-0.6.1-models/output_graph.pbmm --lm deepspeech-0.6.1-models/lm.binary --trie deepspeech-0.6.1-models/trie --audio {}'.format(dst_file)], stdout=subprocess.PIPE, shell=True)
    output = proc.stdout.read().decode("utf-8") 
    update.message.reply_text(output)
    
    

def cancel(update, context):
    update.message.reply_text('GoodBye!!!')

def main():
    updater = Updater("1082632506:AAHeixCInGzZu_9d8hKkvCAHn3t1BDau75Q", use_context=True)
  
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            AUDIO: [MessageHandler(Filters.voice, analyze)],
        },
        allow_reentry=True,
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()