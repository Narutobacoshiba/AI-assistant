import sys
import time
from datetime import datetime

from yuki.skills.skill import AssistantSkill
from yuki.utils.startup import play_activation_sound
from yuki.utils.mongoDB import db
from yuki.enumerations import InputMode, MongoCollections


class ActivationSkills(AssistantSkill):

    @classmethod
    def enable_assistant(cls, **kwargs):
        input_mode = db.get_documents(collection=MongoCollections.GENERAL_SETTINGS.value)[0]['input_mode']
        if input_mode == InputMode.VOICE.value:
            play_activation_sound()

    @classmethod
    def disable_assistant(cls, **kwargs):
        cls.response('Bye')
        time.sleep(1)
        cls.console(info_log='Application terminated gracefully.')
        sys.exit()

    @classmethod
    def assistant_greeting(cls, **kwargs):
        now = datetime.now()
        day_time = int(now.strftime('%H'))

        if day_time < 12:
            cls.response('Good morning master')
        elif 12 <= day_time < 18:
            cls.response('Good afternoon master')
        else:
            cls.response('Good evening master')
