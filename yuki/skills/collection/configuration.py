import importlib

from yuki.core.console import ConsoleManager
from yuki.skills.skill import AssistantSkill
from yuki import settings
from yuki.utils.mongoDB import db
from yuki.enumerations import InputMode, MongoCollections
from yuki.utils import console
from yuki.utils import input

input_mode = db.get_documents(collection='general_settings')[0]['input_mode']
response_in_speech = db.get_documents(collection='general_settings')[0]['response_in_speech']
assistant_name = db.get_documents(collection='general_settings')[0]['assistant_name']
input_language = db.get_documents(collection='general_settings')[0]['input_language']

class ConfigurationSkills(AssistantSkill):

    @classmethod
    def configure_assistant(cls, **kwargs):

        console.print_console_header('Configure assistant')
        cls.console('NOTE: Current name: {0}'.format(assistant_name), refresh_console=False)
        console.headerize()
        cls.response('Set new assistant name: ', refresh_console=False)
        new_assistant_name = cls.user_input()

        console.headerize()

        cls.console('NOTE: Current mode: {0}'.format(input_mode), refresh_console=False)
        console.headerize()
        cls.response('Set new input mode (text or voice): ',refresh_console=False)
        input_mode_values = [mode.value for mode in InputMode]
        new_input_mode = input.validate_input_with_choices(available_choices=input_mode_values)

        cls.console("NOTE: current input language: {0}".format(input_language),refresh_console=False)
        console.headerize()
        cls.response('Set new input language: ',refresh_console=False)
        language_value = ['af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb', 'ny', 'zh-cn', 'zh-tw', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'he', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'kk', 'km', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'or', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu']
        new_input_language = input.validate_input_with_choices(available_choices=language_value)

        console.headerize()
        cls.response('Do you want response in speech?', refresh_console=False)
        new_response_in_speech = input.check_input_to_continue()

        new_settings = {
            'assistant_name': new_assistant_name,
            'input_mode': new_input_mode,
            'input_language': new_input_language,
            'response_in_speech': new_response_in_speech,
        }

        cls.console("\n The new settings are the following: \n", refresh_console=False)
        for setting_desc, value in new_settings.items():
            cls.console('* {0}: {1}'.format(setting_desc, value), refresh_console=False)

        cls.response('Do you want to save new settings? ', refresh_console=False)
        save = input.check_input_to_continue()
        if save:
            db.update_collection(collection=MongoCollections.GENERAL_SETTINGS.value, documents=[new_settings])

            import yuki
            importlib.reload(yuki)
            ConsoleManager().console_output()

        else:
            cls.console(refresh_console=True)

