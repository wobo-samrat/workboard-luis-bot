# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, TurnContext
from botbuilder.schema import InputHints

from .show_okr_dialog import ShowOKRDialog
from .update_okr_dialog import UpdateOKRDialog
from models.okr_details import ShowOKRDetails,UpdateOKRDetails
from work_board_recognizer import WorkBoardRecognizer
from helpers.luis_helper import LuisHelper, Intent
from actions.main_actions import MainAction


class MainDialog(ComponentDialog):
    def __init__(
        self, luis_recognizer: WorkBoardRecognizer, show_okr_dialog: ShowOKRDialog,
        update_okr_dialog : UpdateOKRDialog
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)
        self._action = MainAction()
        self._luis_recognizer = luis_recognizer
        self._show_okr_dialog_id = show_okr_dialog.id
        self._update_okr_dialog_id = update_okr_dialog.id

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(show_okr_dialog)
        self.add_dialog(update_okr_dialog)
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.intro_step, self.act_step, self.final_step]
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
                    "'LuisAPIHostName' to the appsettings.json file.",
                    input_hint=InputHints.ignoring_input,
                )
            )

            return await step_context.next(None)
        message_text = (
            str(step_context.options)
            if step_context.options  
            else self._action.get_random_utterance('welcome_msg')
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        intent, score,luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )  
        print('intent in main dialog is => ',intent) 
        print('result in main dialog is => ',luis_result)    
        if score > 0.3: 

            
            if intent=='greet':
                greet_back_txt = self._action.get_random_utterance('greet_back')
                greet_back_message = MessageFactory.text(
                greet_back_txt, greet_back_txt, InputHints.ignoring_input
                )
                await step_context.context.send_activity(greet_back_message)

            elif intent == 'show_OKR' and luis_result:            
                # Run the showOKRDialog giving it whatever details we have from the LUIS call.
                return await step_context.begin_dialog(self._show_okr_dialog_id, luis_result)  

            elif intent == 'update_okr'  and luis_result:
                # Run the updateOKRDialog giving it whatever details we have from the LUIS call.
                return await step_context.begin_dialog(self._update_okr_dialog_id, luis_result)  

            else:
                only_OKR_text = self._action.get_random_utterance('only_okr_msg')
                only_show_update_okr_message = MessageFactory.text(
                only_OKR_text, only_OKR_text, InputHints.ignoring_input
                )
                await step_context.context.send_activity(only_show_update_okr_message)


    #         elif intent == Intent.GET_WEATHER.value:
    #             get_weather_text = "TODO: get weather flow here"
    #             get_weather_message = MessageFactory.text(
    #                 get_weather_text, get_weather_text, InputHints.ignoring_input
    #             )
    #             await step_context.context.send_activity(get_weather_message)

        else:
            didnt_understand_text = self._action.get_random_utterance('not_understand_msg')
            didnt_understand_message = MessageFactory.text(
                didnt_understand_text, didnt_understand_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(didnt_understand_message)

        return await step_context.next(None)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # If the child dialog ("showOKRDialog") was cancelled or the user failed to confirm,
        # the Result here will be null.
        prompt_message = self._action.get_random_utterance('final_prompt')
        return await step_context.replace_dialog(self.id, prompt_message)

