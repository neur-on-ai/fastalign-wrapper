import logging
import subprocess
import tempfile
from pathlib import Path
from typing import Tuple, List, Dict


def parse_alignments(alignments: str) -> List[Dict[int, List[int]]]:
  word_alignments = []

  for alignment in alignments.split("\n"):
    mapping: Dict[int, List[int]] = dict()
    for wa in alignment.split(" "):
      try:
        source, target = map(int, wa.split("-"))
        if source not in mapping:
          mapping[source] = []
        mapping[source].append(target)
      except ValueError:
        continue
    word_alignments.append(mapping)

  return word_alignments


class FastAligner:
  def __init__(self, binary_dir: str = None):
    base_path = Path(binary_dir) if binary_dir else Path(
        __file__).parent.parent / "external/fast_align/build"
    self.fast_align_path = base_path / "fast_align"
    self.atools_path = base_path / "atools"

    if not self.fast_align_path.exists():
      raise FileNotFoundError(
          f"fast_align binary not found at {self.fast_align_path}")
    if not self.atools_path.exists():
      raise FileNotFoundError(f"atools binary not found at {self.atools_path}")

  def _run_fast_align(self, input_file: str, reverse: bool = False) -> str:
    cmd = [str(self.fast_align_path), "-i", input_file, "-d", "-v"]
    if reverse:
      cmd.append("-r")

    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
      logging.error(
          f"fast_align {'reverse' if reverse else 'forward'} failed")
      raise ValueError("fast_align failed")

    return proc.stdout.decode()

  def align(self, sentence_pairs: List[Tuple[str, str]]) -> List[
    Dict[int, List[int]]]:
    if not sentence_pairs:
      raise ValueError("No sentence pairs provided.")

    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8",
                                     delete=False) as tmp_file:

      try:
        if not sentence_pairs:
          raise ValueError()

        ss = "\n".join(f"{src} ||| {tgt}" for src, tgt in sentence_pairs)

        if ss:
          ss += "\n"

      except (IndexError, TypeError) as e:
        raise ValueError(f"Invalid sentence pair format: {e}") from e

      tmp_file.write(ss)
      tmp_file.flush()
      input_path = tmp_file.name

    fwd_file = None
    rev_file = None
    try:
      # Run forward and reverse alignments
      forward_output = self._run_fast_align(input_path, reverse=False)
      reverse_output = self._run_fast_align(input_path, reverse=True)

      with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8",
                                       delete=False) as fwd_file, \
          tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8",
                                      delete=False) as rev_file:

        fwd_file.write(forward_output)
        fwd_file.flush()

        rev_file.write(reverse_output)
        rev_file.flush()

        # Run atools to symmetrize
        atools_cmd = [
          str(self.atools_path),
          "-i", fwd_file.name,
          "-j", rev_file.name,
          "-c", "grow-diag-final-and"  # Best symmetrization heuristic
        ]
        proc = subprocess.run(
            atools_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if proc.returncode != 0:
          logging.error(f"atools failed: {proc.stderr.decode()}")
          raise ValueError("atools failed")

        output = proc.stdout.decode()

    finally:
      Path(input_path).unlink(missing_ok=True)
      if fwd_file:
        Path(fwd_file.name).unlink(missing_ok=True)
      if rev_file:
        Path(rev_file.name).unlink(missing_ok=True)

    parsed_alignments = parse_alignments(
        output[:-1] if output.endswith('\n') else output)

    if len(parsed_alignments) != len(sentence_pairs):
      raise ValueError(
          f"Number of alignments ({len(parsed_alignments)}) does not match number of sentence pairs ({len(sentence_pairs)})"
      )

    return parsed_alignments
