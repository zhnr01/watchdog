import hashlib


class FingerprintService:
    def create(self, message: str, stack_trace: str) -> str:
        payload = f"{message}:{stack_trace}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()