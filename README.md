fastalign wrapper for Python
==========

A Python wrapper around [fast_align](https://github.com/clab/fast_align) for word alignment in parallel corpora. This package allows you to use `fast_align` from Python and build the C++ binary automatically during installation.

---

## 🚀 Features

- Python class `FastAligner` for easy access to fast_align
- Automatically compiles `fast_align` during install using `CMake`
- Uses `subprocess` internally and returns alignments as strings

---

## 📦 Installation

```bash
git clone https://github.com/neur-on-ai/fastalign-wrapper
cd fastalign-wrapper
git submodule update --init --recursive
pip install -e .
```

## 🧠 Usage
````python
from fastalign.aligner import FastAligner

aligner = FastAligner()
result = aligner.align([("the house", "la maison")])
print(result)  # Output: "[{0: [0], 1: [1]}]"
````

## 📋 License

MIT – same license as `fast_align`.

## 🙏 Credits

[fast_align](https://github.com/clab/fast_align) by the Carnegie Mellon University

Python wrapper maintained by [NEUR.ON](https://neur-on.ai/)
