# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints
from .cancel_and_help_dialog import CancelAndHelpDialog
from helpers.luis_helper import LuisHelper, Intent
from work_board_recognizer import WorkBoardRecognizer
from actions.okr_actions import ShowOKRAction

from datatypes_date_time.timex import Timex


class ShowOKRDialog(CancelAndHelpDialog):
    def __init__(self,luis_recognizer: WorkBoardRecognizer, dialog_id: str = None):
        super(ShowOKRDialog, self).__init__(dialog_id or ShowOKRDialog.__name__)
        self._luis_recognizer = luis_recognizer
        self._action = ShowOKRAction()
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))        
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.ask_obj_step,
                    self.process_usr_reply_step  
                ],
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    """
    Bot asks back the user about 
    :param step_context:
    :return DialogTurnResult:
    """

    async def ask_obj_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        
        okr_details = step_context.options

        if okr_details.okr_usr_rply is None:
            
            message_text = self._action.get_random_utterance('ask_objectives')
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(okr_details.okr_usr_rply)

    """
    user's response registered by the bot.
    :param step_context:
    :return DialogTurnResult:
    """

    async def process_usr_reply_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        okr_details = step_context.options
        
        okr_details.okr_usr_rply = step_context.result
        
        intent, score, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )

        print('intent in okr ',intent)
        if score > 0.3:
            if intent == 'confirm' or intent=='affirm_okr':
                 
                 message_text = self._action.get_random_utterance('route_okr') + ' . '
                 message_text = message_text + '\n'                         
                 message_text = message_text + 'call API to show OKR page with entity < ' + okr_details.get_okr_type()  + '>'
                # prompt_message = MessageFactory.text(
                #     message_text, message_text, InputHints.ignoring_input
                # )

                 prompt_message = MessageFactory.text(
                    message_text, message_text, InputHints.ignoring_input
                 )
            
            else:
                message_text = self._action.get_random_utterance('close_okr')
                prompt_message = MessageFactory.text(
                    message_text, message_text, InputHints.ignoring_input
                )
        else:
            message_text = self._action.get_random_utterance('not_understand_msg')
            prompt_message = MessageFactory.text(
                    message_text, message_text, InputHints.ignoring_input
                )
            
        await step_context.context.send_activity(prompt_message)  
            
        return await step_context.end_dialog(okr_details)
