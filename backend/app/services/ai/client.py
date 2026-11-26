"""Jedyne wejście do modelu językowego. Plik należy do Epiku 4.

Epik 5 (US 5.5) i Epik 6 (US 6.3) wywołują tylko complete() i obsługują LLMNotConfigured.
"""


class LLMNotConfigured(RuntimeError):
    """Brak klucza API albo dostawcy."""


def complete(*, task: str, system: str, prompt: str) -> str:
    raise LLMNotConfigured("Model językowy nie jest jeszcze podłączony (US 4.3)")
