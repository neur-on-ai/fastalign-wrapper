import pytest

from fastalign.aligner import FastAligner


def test_alignment_basic():
  aligner = FastAligner()

  sentence_pair = [("the house", "la maison")]
  result = aligner.align(sentence_pair)

  # Should be a list containing one dictionary mapping source to target indices
  assert isinstance(result, list)
  assert len(result) == 1
  assert isinstance(result[0], dict)
  # Expecting mappings for both words (0 and 1)
  assert len(result[0]) > 0
  # Check alignment structure (keys should be integers)
  assert all(isinstance(k, int) for k in result[0].keys())
  # Check that values are lists of integers
  assert all(isinstance(v, list) and all(isinstance(i, int) for i in v) for v in
             result[0].values())


def test_alignment_empty():
  aligner = FastAligner()

  sentence_pair = [("", "")]
  result = aligner.align(sentence_pair)

  # Should be a list with one empty dictionary
  assert isinstance(result, list)
  assert len(result) == 1
  assert isinstance(result[0], dict)


def test_alignment_noisy():
  aligner = FastAligner()

  sentence_pair = [("the house!!!", "la maison???")]
  result = aligner.align(sentence_pair)

  # Should be a list containing one dictionary
  assert isinstance(result, list)
  assert len(result) == 1
  assert isinstance(result[0], dict)
  # Should have alignments
  assert len(result[0]) > 0


def test_alignment_multiple():
  aligner = FastAligner()

  sentence_pairs = [
    ("the house", "la maison"),
    ("the car", "la voiture"),
    ("the book", "le livre")
  ]
  result = aligner.align(sentence_pairs)

  # Should be a list of dictionaries, one per sentence pair
  assert isinstance(result, list)
  assert len(result) == len(sentence_pairs)
  # Check each result is a dictionary
  assert all(isinstance(item, dict) for item in result)


def test_alignment_invalid_source():
  aligner = FastAligner()

  sentence_pair = [(" ", "bonjour je suis là")]

  with pytest.raises(ValueError):
    aligner.align(sentence_pair)


def test_alignment_invalid_target():
  aligner = FastAligner()

  sentence_pair = [
    ("hi i am here", " ")]
  result = aligner.align(sentence_pair)

  # Should still return a valid structure
  assert isinstance(result, list)
  assert len(result) == 1
  assert isinstance(result[0], dict)
  assert len(result[0]) == 0


def test_alignment_multiple_invalid():
  aligner = FastAligner()

  sentence_pair = [(" ", "bonjour je suis là"),
                   ("hi i am here", "bonjour je suis là"),
                   ("hi i am here", " ")]
  result = aligner.align(sentence_pair)

  # Should still return a valid structure
  assert isinstance(result, list)
  assert len(result) == 3
  assert isinstance(result[0], dict)
  assert isinstance(result[1], dict)
  assert isinstance(result[2], dict)
  assert len(result[0]) == 0
  assert len(result[1]) > 0
  assert len(result[2]) == 0
