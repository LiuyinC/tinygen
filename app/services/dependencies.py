from app.services.event_logger_service import EventLogger
from app.services.gpt_service import GPTService

gpt_service_instance = GPTService()
event_logger = EventLogger()

def get_gpt_service() -> GPTService:
    return gpt_service_instance

def get_event_logger() -> EventLogger:
    return event_logger
