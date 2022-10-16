from word2number import w2n

from yuki.skills.skill import AssistantSkill
from yuki.utils.mapping import math_symbols_mapping


class MathSkills(AssistantSkill):
    
    @classmethod
    def do_calculations(cls, voice_transcript, **kwargs):
        transcript_with_numbers = cls._replace_words_with_numbers(voice_transcript)
        math_equation = cls._clear_transcript(transcript_with_numbers)
        try:
            result = str(eval(math_equation))
            cls.response(result)
        except Exception as e:
            cls.console_manager.console_output('Failed to eval the equation --> {0} with error message {1}'.format(math_equation, e))

    @classmethod
    def _replace_words_with_numbers(cls, transcript):
        transcript_with_numbers = ''
        for word in transcript.split():
            try:
                number = w2n.word_to_num(word)
                transcript_with_numbers += ' ' + str(number)
            except ValueError as e:
                transcript_with_numbers += ' ' + word
        return transcript_with_numbers

    @classmethod
    def _clear_transcript(cls, transcript):
        cleaned_transcript = ''
        for word in transcript.split():
            if word.isdigit() or word in math_symbols_mapping.values():
                cleaned_transcript += word
            else:
                cleaned_transcript += math_symbols_mapping.get(word, '')
        return cleaned_transcript
