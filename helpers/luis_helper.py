# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum
from typing import Dict
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext

from models.okr_details import ShowOKRDetails,UpdateOKRDetails


class Intent(Enum):
    BOOK_FLIGHT = "BookFlight"
    CANCEL = "Cancel"
    GET_WEATHER = "GetWeather"
    NONE_INTENT = "NoneIntent"


def top_intent(intent_dict) :
    max_intent = Intent.NONE_INTENT
    max_value = 0.0
    for intent, intentScore in intent_dict.items():
        if intentScore.score > max_value:
            max_intent, max_value = intent, intentScore.score
    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(
        luis_recognizer: LuisRecognizer, turn_context: TurnContext
    ) -> (Intent, object):
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        result = None
        intent = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)
            print('recognizer_result ',recognizer_result)

            intents = (
                sorted(
                    recognizer_result.intents,
                    key=recognizer_result.intents.get,
                    reverse=True,
                )
                if recognizer_result.intents
                else None
            )

            topIntent = top_intent(recognizer_result.intents)
            
            if topIntent.intent == 'show_OKR':
                result = ShowOKRDetails() 
                okrtype_entities = recognizer_result.entities.get("$instance", {}).get(
                    "okr_type", []
                )                
                if len(okrtype_entities) > 0:
                    result.okr_type = okrtype_entities[0]["text"]
                else:
                    result.okr_type = None

            elif topIntent.intent == 'update_okr':
                  result = UpdateOKRDetails()
                  okrtype_entities = recognizer_result.entities.get("$instance", {}).get(
                    "okr_type", []
                    )                
                  if len(okrtype_entities) > 0:
                    result.okr_type = okrtype_entities[0]["text"]
                  else:
                    result.okr_type = None

        except Exception as e:
            print(e)
        print('luis return val ==> ', topIntent.intent,topIntent.score, result)
        return topIntent.intent,topIntent.score, result
