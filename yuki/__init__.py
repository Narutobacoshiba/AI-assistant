import os
from logging import config

import yuki.engines as engines
from yuki.enumerations import InputMode
from yuki import settings
from yuki.utils.mongoDB import db
from yuki.settings import ROOT_LOG_CONF
from yuki.utils.startup import configure_MongoDB

config.dictConfig(ROOT_LOG_CONF)

with open(ROOT_LOG_CONF['handlers']['file']['filename'], 'w') as f:
    f.close()

root_file = os.path.dirname(__file__)
with open(root_file+"\\skills\\collection\\temp\\temporary_container.txt","w") as f:
    f.close()
with open(root_file+"\\skills\\collection\\temp\\temporary_time.txt","w") as f:
    f.close()

configure_MongoDB(db, settings,is_update=False)

input_mode = db.get_documents(collection='general_settings')[0]['input_mode']
response_in_speech = db.get_documents(collection='general_settings')[0]['response_in_speech']
assistant_name = db.get_documents(collection='general_settings')[0]['assistant_name']
input_language = db.get_documents(collection='general_settings')[0]['input_language']

input_engine = engines.STTEngine(input_language) if input_mode == InputMode.VOICE.value else engines.TTTEngine(input_language)
output_engine = engines.TTSEngine() if response_in_speech else engines.TTTEngine(input_language)
