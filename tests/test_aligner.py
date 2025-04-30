from fastalign.aligner import FastAligner


def test_alignment_basic():
    aligner = FastAligner()

    # This is a basic aligned sentence: "the house ||| la maison"
    # Expected output is likely "0-0 1-1" depending on fast_align behavior
    sentence_pair = [("the house","la maison")]
    result = aligner.align(sentence_pair)

    # Should be a non-empty string of alignment pairs like "0-0 1-1"
    assert isinstance(result, str)
    assert "-" in result
    assert result.strip() != ""

def test_alignment_empty():
    aligner = FastAligner()

    # Empty input should return an empty string or some indication of no alignment
    sentence_pair = [("", "")]
    result = aligner.align(sentence_pair)

    # Should be an empty string or some indication of no alignment
    assert result == "" or result is None

def test_alignment_noisy():
    aligner = FastAligner()

    # Noisy input with special characters
    sentence_pair = [("the house!!!", "la maison???")]
    result = aligner.align(sentence_pair)

    # Should be a non-empty string of alignment pairs like "0-0 1-1"
    assert isinstance(result, str)
    assert "-" in result
    assert result.strip() != ""

def test_alignment_multiple():
    aligner = FastAligner()

    # Multiple sentence pairs
    sentence_pairs = [
        ("the house", "la maison"),
        ("the car", "la voiture"),
        ("the book", "le livre")
    ]
    result = aligner.align(sentence_pairs)

    # Should be a non-empty string of alignment pairs like "0-0 1-1"
    assert isinstance(result, str)
    assert "-" in result
    assert result.count("\n") == len(sentence_pairs) - 1
    assert result.strip() != ""