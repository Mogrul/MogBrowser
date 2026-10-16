from typing import Any


class Responses:
    @staticmethod
    def send_fail(message: str, code = 404) -> tuple[dict[str, Any], int]:
        return {
            "success": False,
            "error": {
                "code": code,
                "message": message
            }
        }, code