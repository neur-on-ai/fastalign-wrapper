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
