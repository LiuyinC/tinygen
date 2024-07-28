from app.services.gpt_service import GPTService


def get_gpt_service() -> GPTService:
    return GPTService()