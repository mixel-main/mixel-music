from app.core.config import get_config
from app.core.logger import get_logger


class BaseService:
    def __init__(self) -> None:
        self.config = get_config()
        self.logger = get_logger()
