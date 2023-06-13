import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.dispatch_components import AbstractResponseInterceptor
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type, is_intent_name

from ask_sdk_model import Response

from utils import find_target

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type('LaunchRequest')(handler_input)
    
    def handle(self, handler_input):
        speech_text = 'I can tell you where to aim on a dartboard given a score remaining and the amount of darts you have left. Like 91 and 1 dart.'
        reprompt = 'Say a remaining score and dart amount. For example, 127 with 2 darts.'
        
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class AdviceIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name('AdviceIntent')(handler_input)
    
    def handle(self, handler_input):
        score = handler_input.request_envelope.request.intent.slots["score"].value
        darts = int(handler_input.request_envelope.request.intent.slots["darts"].value)
        target = find_target(score,darts)
        
        speech_text = f'You should aim for {find_target(score,darts)}.'
        
        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name('AMAZON.HelpIntent')(handler_input)
    
    def handle(self, handler_input):
        speech_text = f'Provide a score and dart count, and I will tell you the best location to aim for.'
        reprompt = 'Say a remaining score and dart amount. For example, 54 and 3.'
        
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name('AMAZON.CancelIntent')(handler_input) or is_intent_name('AMAZON.StopIntent')(handler_input)
    
    def handle(self, handler_input):
        speech_text = f'Goodbye.'
        
        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type('SessionEndedRequest')(handler_input)

    def handle(self, handler_input):
        logger.info(f'Session ended with reason: {handler_input.request_envelope.request.reason}')
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)

        speech_text = 'Sorry, I didn\'t catch that. Please try again.'
        reprompt = 'Could you repeat what you said?'

        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class LoggingRequestInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        print(f'Request received: {handler_input.request_envelope.request}')


class LoggingResponseInterceptor(AbstractResponseInterceptor):
    def process(self, handler_input, response):
        print(f'Response generated: {response}')



sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(AdviceIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LoggingRequestInterceptor())
sb.add_global_response_interceptor(LoggingResponseInterceptor())

lambda_handler = sb.lambda_handler()
