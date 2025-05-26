import json
import logging
import requests
from typing import Dict, Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Raspberry Pi endpoint - replace with your actual endpoint
RASPBERRY_PI_ENDPOINT = "http://your-raspberry-pi-ip:5000"

def send_command_to_pi(command: str, room: str) -> bool:
    """
    Send command to Raspberry Pi
    """
    try:
        payload = {
            "command": command,
            "room": room
        }
        response = requests.post(f"{RASPBERRY_PI_ENDPOINT}/control", json=payload)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error sending command to Raspberry Pi: {str(e)}")
        return False

def handle_open_blinds(room: str) -> Dict[str, Any]:
    """
    Handle opening blinds command
    """
    success = send_command_to_pi("open", room)
    if success:
        return {
            "output": f"Opening the {room} blinds",
            "shouldEndSession": True
        }
    return {
        "output": f"Sorry, I couldn't open the {room} blinds",
        "shouldEndSession": True
    }

def handle_close_blinds(room: str) -> Dict[str, Any]:
    """
    Handle closing blinds command
    """
    success = send_command_to_pi("close", room)
    if success:
        return {
            "output": f"Closing the {room} blinds",
            "shouldEndSession": True
        }
    return {
        "output": f"Sorry, I couldn't close the {room} blinds",
        "shouldEndSession": True
    }

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler for Alexa skill
    """
    try:
        # Get the intent name from the request
        intent_name = event['request']['intent']['name']
        
        # Get the room slot value
        slots = event['request']['intent']['slots']
        room = slots['room']['value'].lower() if 'room' in slots else "living room"
        
        # Handle different intents
        if intent_name == "OpenBlindsIntent":
            response = handle_open_blinds(room)
        elif intent_name == "CloseBlindsIntent":
            response = handle_close_blinds(room)
        else:
            response = {
                "output": "I'm not sure what you want me to do with the blinds",
                "shouldEndSession": True
            }
        
        # Construct the response
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": response["output"]
                },
                "shouldEndSession": response["shouldEndSession"]
            }
        }
        
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Sorry, I encountered an error while processing your request"
                },
                "shouldEndSession": True
            }
        } 