import subprocess
from pathlib import Path
import tempfile
from typing import Tuple, List


class FastAligner:
    def __init__(self, binary_path: str = None):
        default_path = Path(__file__).parent.parent / "external/fast_align/build/fast_align"
        self.binary_path = Path(binary_path) if binary_path else default_path

        if not self.binary_path.exists():
            raise FileNotFoundError(f"fast_align binary not found at {self.binary_path}")

    def align(self, sentence_pair: List[Tuple[str, str]], forward=True, score=False, quiet=True) -> str:
        with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False) as tmp_file:
            try:
                if not sentence_pair:
                    return ""

                ss = "\n".join(f"{src} ||| {tgt}" for src, tgt in sentence_pair)

                if ss:
                    ss += "\n"

            except (IndexError, TypeError) as e:
                raise ValueError(f"Invalid sentence pair format: {e}") from e
            tmp_file.write(ss.strip() + "\n")
            tmp_file.flush()
            input_path = tmp_file.name

        cmd = [str(self.binary_path), "-i", input_path]
        if forward:
            cmd.append("-d")
        if score:
            cmd.append("-o")
        if quiet:
            cmd.append("-v")

        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Clean up
        Path(input_path).unlink(missing_ok=True)

        if proc.returncode != 0:
            raise RuntimeError(f"fast_align failed: {proc.stderr.decode()}")

        return proc.stdout.decode().strip()
