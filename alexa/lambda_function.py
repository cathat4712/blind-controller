import json
import logging
import requests
from typing import Dict, Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Raspberry Pi endpoint - replace with your actual endpoint
RASPBERRY_PI_ENDPOINT = "http://your-raspberry-pi-ip:5000"

def create_response(output: str, should_end_session: bool = True) -> Dict[str, Any]:
    """
    Create a simplified Alexa response
    """
    try:
        response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": output
                },
                "shouldEndSession": should_end_session
            }
        }
        logger.info(f"Created response: {json.dumps(response)}")
        return response
    except Exception as e:
        logger.error(f"Error creating response: {str(e)}", exc_info=True)
        # Return a minimal valid response in case of error
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "I encountered an error. Please try again."
                },
                "shouldEndSession": True
            }
        }

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler for Alexa skill
    """
    try:
        # Log the incoming event for debugging
        logger.info("=== START OF LAMBDA HANDLER ===")
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Basic request validation
        if not isinstance(event, dict):
            logger.error("Event is not a dictionary")
            return create_response("Invalid request format")
            
        if 'request' not in event:
            logger.error("Missing 'request' field in event")
            return create_response("Invalid request format")
            
        request = event['request']
        if not isinstance(request, dict):
            logger.error("Request is not a dictionary")
            return create_response("Invalid request format")
            
        if 'type' not in request:
            logger.error("Missing 'type' field in request")
            return create_response("Invalid request type")
            
        request_type = request['type']
        logger.info(f"Processing request type: {request_type}")
        
        # Handle LaunchRequest
        if request_type == 'LaunchRequest':
            logger.info("Handling LaunchRequest")
            return create_response("Welcome to Blind Controller. You can say open or close followed by a room name.", should_end_session=False)
            
        # Handle IntentRequest
        if request_type == 'IntentRequest':
            if 'intent' not in request:
                logger.error("Missing 'intent' field in IntentRequest")
                return create_response("Invalid intent request")
                
            intent = request['intent']
            intent_name = intent.get('name', '')
            logger.info(f"Processing intent: {intent_name}")
            
            # Handle standard Amazon intents
            if intent_name == "AMAZON.HelpIntent":
                return create_response("You can say open or close followed by a room name.", should_end_session=False)
            elif intent_name == "AMAZON.StopIntent":
                return create_response("Stopping blind operation")
            elif intent_name == "AMAZON.CancelIntent":
                return create_response("Cancelling blind operation")
            elif intent_name == "AMAZON.FallbackIntent":
                return create_response("I'm not sure what you want me to do. Try saying help.", should_end_session=False)
            
            # Handle custom intents
            if intent_name == "OpenBlindsIntent":
                return create_response("Opening the blinds")
            elif intent_name == "CloseBlindsIntent":
                return create_response("Closing the blinds")
            else:
                logger.error(f"Unsupported intent: {intent_name}")
                return create_response("I'm not sure what you want me to do. Try saying help.", should_end_session=False)
        
        # If we get here, the request type is not supported
        logger.error(f"Unsupported request type: {request_type}")
        return create_response("I'm not sure what you want me to do. Try saying help.", should_end_session=False)
        
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}", exc_info=True)
        return create_response("I encountered an error. Please try again.")
    finally:
        logger.info("=== END OF LAMBDA HANDLER ===") 