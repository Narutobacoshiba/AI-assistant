import logging 
from yuki.core.console import ConsoleManager
from yuki.utils.console import user_input
from yuki.engines.ltl import L2L
from yuki.settings import DEFAULT_GENERAL_SETTINGS

class TTTEngine:

    def __init__(self,input_language):
        self.logger = logging
        self.console_manager = ConsoleManager()
        self.input_language = input_language

    def recognize_input(self, **kwargs):
        try:
            text_transcript = input(user_input).lower()
            while text_transcript == '':
                text_transcript = input(user_input).lower()
                if self.input_language != 'en':
                    text_transcript = L2L(text_transcript,self.input_language,'en')

            return text_transcript
        except EOFError as e:
            self.console_manager.console_output(error_log='Failed to recognize user input with message: {0}'.format(e))

    def assistant_response(self, message, refresh_console=True):
        try:
            if message:
                self.console_manager.console_output(message, refresh_console=refresh_console)
        except RuntimeError as e:
            self.console_manager.console_output(error_log='Error in assistant response with message: {0}'.format(e))