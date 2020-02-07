import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

# Above code just diables certs because of virtual env.

from flask import Flask
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter

# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import gettext

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractRequestInterceptor, AbstractExceptionHandler)
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from alexa import data
from ddog import query_ddog_cpu

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.WELCOME_MESSAGE)

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )

def get_resolved_value(request, slot_name):
    """Resolve the slot name from the request using resolutions."""
    # type: (IntentRequest, str) -> Union[str, None]
    try:
        return (request.intent.slots[slot_name].resolutions.
                resolutions_per_authority[0].values[0].value.name)
    except (AttributeError, ValueError, KeyError, IndexError, TypeError) as e:
        logger.info("Couldn't resolve {} for request: {}".format(slot_name, request))
        logger.info(str(e))
        return None

class GetMetricsIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetMetrics")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # _ = handler_input.attributes_manager.request_attributes["_"]
        # speak_output = _(data.HELLO_MSG)
        metric = get_resolved_value(handler_input.request_envelope.request, "metric")
        if metric == 'cpu':
            cpu = query_ddog_cpu()
            return (
                handler_input.response_builder
                .speak("Your average cpu right now is {}".format(cpu))
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
            )

        return (
            handler_input.response_builder
            .speak("Latency = Time")
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )



class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.HELP_MSG)

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.GOODBYE_MSG)

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        _ = handler_input.attributes_manager.request_attributes["_"]
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = _(data.REFLECTOR_MSG).format(intent_name)

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.ERROR)

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class LocalizationInterceptor(AbstractRequestInterceptor):
    """
    Add function to request attributes, that can load locale specific data
    """

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        i18n = gettext.translation(
            'data', localedir='locales', languages=[locale], fallback=True)
        handler_input.attributes_manager.request_attributes["_"] = i18n.gettext

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

@app.route('/ddog/webhook')
def alert(payload):
    return payload

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetMetricsIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(IntentReflectorHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())

sb.add_exception_handler(CatchAllExceptionHandler())


skill_response = SkillAdapter(
    skill=sb.create(), skill_id="amzn1.ask.skill.1fd6a485-84ff-406c-aba1-75007ce3df11", app=app)

skill_response.register(app=app, route="/")
if __name__ == '__main__':
    app.run()
