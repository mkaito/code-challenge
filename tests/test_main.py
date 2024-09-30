from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@patch("lib.llm.OpenAIClient.call")
@patch("lib.masker.Masker.unmask")
@patch("lib.masker.Masker.mask")
def test_llm_never_sees_pii(mock_mask, mock_unmask, mock_call_llm):
    """
    Ensure the LLM never sees PII.
    - Mask PII in prompt and context before sending to LLM.
    - LLM receives masked prompt and context.
    - Verify response is processed correctly.
    """

    # Original prompt and context containing PII
    prompt = "My name is Jebediah Kerman and my email is jeb@ksp.com."
    context = "Please process this information."

    # Expected masked prompt and context
    masked_prompt = "My name is [PERSON] and my email is [EMAIL]."
    masked_context = "Please process this information."
    llm_response_tokens = ["This", "is", "a", "mocked", "response."]

    # Mock the mask function to return masked text and PII entities
    mock_mask.side_effect = [
        (masked_prompt, ["PII1"]),
        (masked_context, ["PII2"]),
    ]

    # Mock the unmask function to return the token as is
    mock_unmask.side_effect = lambda token, _: token

    # Define an async generator to simulate LLM response tokens
    async def async_generator():
        for token in llm_response_tokens:
            yield token

    # Mock the LLM call to return the async generator
    mock_call_llm.return_value = async_generator()

    # Send a POST request to the /process endpoint
    response = client.post("/process", json={"prompt": prompt, "context": context})

    # Verify that the mask function was called with the original prompt and context
    mock_mask.assert_any_call(prompt)
    mock_mask.assert_any_call(context)
    # Verify that the LLM call was made with the masked prompt and context
    mock_call_llm.assert_called_once_with(masked_prompt, masked_context)

    # Verify the response status code and content
    assert response.status_code == 200
    assert response.text.strip() == " ".join(llm_response_tokens)
