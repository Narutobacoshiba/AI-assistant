from yuki import settings
from yuki.utils.startup import internet_connectivity_check
from yuki.core.processor import Processor
from yuki.core.console import ConsoleManager
from yuki.utils.startup import recognize_owner
from yuki.skills.collection.activation import ActivationSkills
from yuki.skills.collection.email import EmailSkill
def main():
    console_manager = ConsoleManager()
    console_manager.console_output(info_log='Wait a second for startup checks..')
    internet_connectivity_check()
    console_manager.console_output(info_log='Application started')
    processor = Processor(console_manager=console_manager, settings_=settings)
    is_owner = recognize_owner(False) 

    if is_owner:
        console_manager.console_output(info_log="recognize master successfully!")
        ActivationSkills().assistant_greeting()
        processor._execute_autorun_skill()
        console_manager.console_output(info_log="I'm ready! Say something :-)")
        while True:
            processor.run()
            
if __name__ == '__main__':
    main()

