import wolframalpha

from yuki.settings import WOLFRAMALPHA_API
from yuki.skills.collection.internet import InternetSkills
from yuki.skills.skill import AssistantSkill
from yuki.utils.mongoDB import db
from yuki.utils import input

class WolframSkills(AssistantSkill):

    @classmethod
    def call_wolframalpha(cls, voice_transcript, **kwargs):
        client = wolframalpha.Client(WOLFRAMALPHA_API['key'])
        if voice_transcript:
            try:
                if WOLFRAMALPHA_API['key']:
                    cls.console(info_log='Wolfarm APi call with query message: {0}'.format(voice_transcript))
                    cls.response("Wait a second, I search..")
                    res = client.query(voice_transcript)
                    wolfram_result = next(res.results).text
                    cls.console(debug_log='Successful response from Wolframalpha')
                    cls.response("I found an anwser for you: "+wolfram_result)
                    cls.response("Is that the response you want?",refresh_console=False)
                    
                    user_response = input.check_input_to_continue()
                    if not user_response:
                        cls.console(text='Suggested Response: ')
                        wolfram_result = cls.user_input()

                    new_skill = {'name': 'learned_skill',
                                'enable': True,
                                'func': wolfram_result,
                            'tags': voice_transcript,
                            },
                            
                    query = {"tags":voice_transcript}
                    find_document_from_database = db.find_document(collection='learned_skills', query=query)
                    if find_document_from_database:
                        for document in find_document_from_database:
                            db.delete_document(collection='learned_skills',query=document)
    
                    db.insert_many_documents(collection='learned_skills', documents=new_skill)

                    return wolfram_result
                        
                else:
                    cls.response("WolframAlpha API is not working.\n"
                          "You can get an API key from: https://developer.wolframalpha.com/portal/myapps/ ")
            except Exception as e:
                if InternetSkills.internet_availability():
                    cls.console(error_log='There is no result from Wolfram API with error: {0}'.format(e))
                else:
                    cls.response('Sorry, but I could not find something')

    @classmethod
    def tell_response(cls, **kwargs):
        cls.response(kwargs.get('skill').get('response'))
