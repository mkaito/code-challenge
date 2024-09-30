from presidio_analyzer import RecognizerResult

from lib.masker import Masker


def compare_entities(entity, expected_entity):
    # Compare entity attributes with expected values
    assert entity.entity_type == expected_entity.entity_type
    assert entity.start == expected_entity.start
    assert entity.end == expected_entity.end


def test_unmask_single_entity():
    """
    Test masking and unmasking of a single PII entity.
    """

    text = "My name is Jebediah Kerman."
    name = "Jebediah Kerman"

    expected_entity = RecognizerResult(
        entity_type="PERSON", start=11, end=55, score=0.85
    )

    expected_unmasked_text = text

    # Mask the text and get entities
    actual_masked_text, entities = Masker.mask(text)

    # Verify text is masked and entity is detected
    assert actual_masked_text != text
    assert name not in actual_masked_text
    assert len(entities) == 1
    compare_entities(entities[0], expected_entity)

    # Unmask the text and verify it matches the original
    actual_unmasked_text = Masker.unmask(actual_masked_text, entities)
    assert actual_unmasked_text == expected_unmasked_text
