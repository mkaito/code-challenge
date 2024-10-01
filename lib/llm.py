import openai


class OpenAIClient:
    """
    A client for interacting with the OpenAI API.
    """

    def __init__(self):
        self.client = openai.OpenAI()

    async def call(self, prompt, context):
        """
        Asynchronously generates a response for the given prompt and context.

        Args:
            prompt (str): The user's input prompt.
            context (str): The context to provide to the language model.

        Yields:
            str: The generated response tokens.
        """
        async for token in self._generate_response(prompt, context):
            yield token

    async def _generate_response(self, prompt, context):
        """
        Asynchronously generates response tokens from the OpenAI model.

        Args:
            prompt (str): The user's input prompt.
            context (str): The context to provide to the language model.

        Yields:
            str: The generated response tokens.
        """
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
                {"role": "system", "content": context},
            ],
            stream=True,
        )

        async for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
