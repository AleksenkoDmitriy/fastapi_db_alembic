import logging
import json
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path
from src.core.config import settings


class UserActionLogger:
    """Логгер для действий пользователей"""
    
    def __init__(self):
        self.logger = logging.getLogger("user_actions")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        log_file = Path(settings.USER_ACTION_LOG_FILE)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(settings.USER_ACTION_LOG_FILE, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        
        self.logger.addHandler(file_handler)
        
        if settings.DEBUG:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter('%(asctime)s - USER_ACTION - %(message)s'))
            self.logger.addHandler(console_handler)
    
    def log_action(
        self,
        user_id: Optional[int],
        username: Optional[str],
        action: str,
        resource_type: str,
        resource_id: Optional[Any] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        status: str = "success"
    ):
        """Логирование действия пользователя"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "username": username,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details or {},
            "ip_address": ip_address,
            "status": status
        }
        
        self.logger.info(json.dumps(log_entry, ensure_ascii=False))


user_logger = UserActionLogger()


def get_user_logger() -> UserActionLogger:
    """Получить логгер для действий пользователя"""
    return user_logger