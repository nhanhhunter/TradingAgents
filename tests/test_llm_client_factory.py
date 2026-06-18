import pytest

from tradingagents.llm_clients.factory import create_llm_client
from tradingagents.llm_clients.openai_client import OpenAIClient


@pytest.mark.unit
@pytest.mark.parametrize("provider", ["mimo", "9router"])
def test_openai_compatible_provider_is_dispatched(provider):
    client = create_llm_client(provider, "test-model")

    assert isinstance(client, OpenAIClient)
    assert client.provider == provider
