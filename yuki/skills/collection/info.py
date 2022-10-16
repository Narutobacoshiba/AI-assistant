from yuki.skills.skill import AssistantSkill
from yuki.utils.mongoDB import db
from yuki.utils.console import headerize

autorun_skills_format = """
-----------------------------------------------------------------------
- Autorun Skills                                                        -
-----------------------------------------------------------------------
"""
autorun_skills_body_format = """
---------------------------- Skill ({0}) ----------------------------
* Skill func: {1}
* Description: {2}
"""

basic_skills_format = """
-----------------------------------------------------------------------
- Basic Skills                                                        -
-----------------------------------------------------------------------
"""

basic_skills_body_format = """
---------------------------- Skill ({0}) ----------------------------
* Skill func: {1}
* Description: {2}
* Tags: {3}
"""

learned_skills_format = """
-----------------------------------------------------------------------
- Learned Skills                                                      -
-----------------------------------------------------------------------
"""

learned_skills_body_format = """
-------------------------- Learned Skill ({0}) ------------------------
* Skill func: {1}
* Question: {2}
* Response: {3}
"""


class AssistantInfoSkills(AssistantSkill):

    @classmethod
    def assistant_check(cls, **kwargs):
        cls.response('Hey master!')

    @classmethod
    def tell_the_skills(cls, **kwargs):
        try:
            response_base = 'I can do the following: \n\n'
            response = cls._create_skill_response(response_base)
            cls.response(response)
        except Exception as e:
            cls.console(error_log="Error with the execution of skill with message {0}".format(e))
            cls.response("Sorry I faced an issue")

    @classmethod
    def assistant_help(cls, **kwargs):
        cls.console(headerize('Help'))
        response_base = ''
        try:
            response = cls._create_skill_response(response_base)
            cls.console(response)
        except Exception as e:
            cls.console(error_log="Error with the execution of skill with message {0}".format(e))
            cls.response("Sorry I faced an issue")

    @classmethod
    def _create_skill_response(cls, response):
        autorun_skills = db.get_documents(collection='autorun_skills')
        response = response + autorun_skills_format
        for skill_id, skill in enumerate(autorun_skills, start=1):
            response = response + autorun_skills_body_format.format(skill_id,
                                                                  skill.get('name'),
                                                                  skill.get('description'),
                                                                  )

        basic_skills = db.get_documents(collection='enabled_basic_skills')
        response = response + basic_skills_format
        for skill_id, skill in enumerate(basic_skills, start=1):
            response = response + basic_skills_body_format.format(skill_id,
                                                                  skill.get('name'),
                                                                  skill.get('description'),
                                                                  skill.get('tags')
                                                                  )
                                                                  
        skills = db.get_documents(collection='learned_skills')
        response = response + learned_skills_format
        for skill_id, skill in enumerate(skills, start=1):
            response = response + learned_skills_body_format.format(skill_id,
                                                                    skill.get('name'),
                                                                    skill.get('tags'),
                                                                    skill.get('func')
                                                                    )

        return response
