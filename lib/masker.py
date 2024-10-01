import secrets
from typing import List, Sequence, Tuple

from presidio_analyzer import AnalyzerEngine, RecognizerResult
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine, DeanonymizeEngine, OperatorConfig

# Generate a 32-byte key for encryption and decryption
key = secrets.token_bytes(32)

# Configure and create an NLP engine using SpaCy
provider = NlpEngineProvider(
    nlp_configuration={
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "en", "model_name": "en_core_web_md"}],
    }
)
engine = provider.create_engine()

# Initialize the analyzer with the NLP engine
analyzer = AnalyzerEngine(nlp_engine=engine, supported_languages=["en"])

# Initialize anonymizer and deanonymizer engines
anonymizer = AnonymizerEngine()
deanonymizer = DeanonymizeEngine()


class Masker:
    @staticmethod
    def mask(text: str) -> Tuple[str, List[RecognizerResult]]:
        """
        Masks sensitive information in the given text.

        This method analyzes the input text to identify sensitive information and then
        anonymizes it using encryption.

        Args:
            text (str): The input text to be masked.

        Returns:
            Tuple[str, List[RecognizerResult]]: A tuple containing the masked text and a list
            of recognizer results detailing the sensitive information found and anonymized.
        """
        results = analyzer.analyze(text, language="en")

        masked_text = anonymizer.anonymize(
            text=text,
            analyzer_results=results,  # pyright: ignore [reportArgumentType]
            operators={"DEFAULT": OperatorConfig("encrypt", {"key": key})},
        )

        return masked_text.text, masked_text.items

    @staticmethod
    def unmask(text: str, entities: Sequence[RecognizerResult]) -> str:
        """
        Replaces masked entities in the given text with their original values.

        Args:
            text (str): The text containing masked entities.
            entities (Sequence[RecognizerResult]): A sequence of RecognizerResult objects representing the masked entities.

        Returns:
            str: The text with masked entities replaced by their original values.
        """
        return deanonymizer.deanonymize(
            text=text,
            entities=entities,  # pyright: ignore [reportArgumentType]
            operators={"DEFAULT": OperatorConfig("decrypt", {"key": key})},
        ).text
