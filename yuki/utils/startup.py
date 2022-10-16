import os
import time
import requests
import logging
from playsound import playsound

from yuki.utils import console
from yuki.enumerations import MongoCollections
from yuki.core.console import ConsoleManager
from yuki.skills.collection.security import master_recognizer

def play_activation_sound():
    utils_dir = os.path.dirname(__file__)
    activation_soundfile = os.path.join(utils_dir, '..', 'resources\\music', 'activation_sound.wav')
    playsound(activation_soundfile)


def internet_connectivity_check(url='http://www.google.com/', timeout=2):
    console_manager = ConsoleManager()
    try:
        console_manager.console_output(info_log='Checking internet connection..')
        _ = requests.get(url, timeout=timeout)
        console_manager.console_output(info_log='Internet connection passed!')
        return True
    except requests.ConnectionError:
        console_manager.console_output(warn_log="No internet connection.")
        console_manager.console_output(warn_log="Skills with internet connection will not work")
        return False


def configure_MongoDB(db, settings,is_update=False):
    if db.is_collection_empty(collection=MongoCollections.GENERAL_SETTINGS.value) or is_update:
        console.print_console_header()
        print('First time configuration..')
        console.print_console_header()
        time.sleep(1)

        default_assistant_name = settings.DEFAULT_GENERAL_SETTINGS['assistant_name']
        default_input_mode = settings.DEFAULT_GENERAL_SETTINGS['input_mode']
        default_input_language = settings.DEFAULT_GENERAL_SETTINGS['input_language']
        default_response_in_speech = settings.DEFAULT_GENERAL_SETTINGS['response_in_speech']
        
        new_settings = {
            'assistant_name': default_assistant_name,
            'input_mode': default_input_mode,
            'input_language': default_input_language,
            'response_in_speech': default_response_in_speech,
        }

        try:
            db.update_collection(collection=MongoCollections.GENERAL_SETTINGS.value, documents=[new_settings])
            #console.print_console_header('Assistant Name')
            print('Assistant name- {0} configured successfully!'.format(default_assistant_name.lower()))
            print('Input mode - {0} configured successfully!'.format(default_input_mode))
            print('Input language - {0} configured successfully!'.format(default_input_language))
            print('Speech response output- {0} configured successfully!'.format(default_response_in_speech))

            time.sleep(4)

        except Exception as e:
            logging.error('Failed to configure assistant settings with error message {0}'.format(e))

    from yuki.skills.registry import CONTROL_SKILLS, ENABLED_BASIC_SKILLS, AUTORUN_SKILLS

    all_skills = {
        MongoCollections.CONTROL_SKILLS.value: CONTROL_SKILLS,
        MongoCollections.ENABLED_BASIC_SKILLS.value: ENABLED_BASIC_SKILLS,
        MongoCollections.AUTORUN_SKILLS.value: AUTORUN_SKILLS
    }
    for collection, documents in all_skills.items():
        db.update_collection(collection, documents)


def recognize_owner(is_owner):
    if is_owner:
        return True

    utils_dir = os.path.dirname(__file__)
    protoPath = os.path.join(utils_dir, '..', 'resources\\face_recognize_model', 'deploy.prototxt')
    modelPath = os.path.join(utils_dir, '..', 'resources\\face_recognize_model', 'res10_300x300_ssd_iter_140000.caffemodel')
    embedderPath = os.path.join(utils_dir, '..', 'resources\\face_recognize_model', 'embedding_model.t7')
    recognizerPath = os.path.join(utils_dir, '..', 'resources\\face_recognize_model', 'recognizer.pickle')
    lePath = os.path.join(utils_dir, '..', 'resources\\face_recognize_model', 'le.pickle')

    result = master_recognizer(protoPath, modelPath, embedderPath, recognizerPath, lePath)
    return result
