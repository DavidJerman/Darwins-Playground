# Darwin's Playground

A multi-agent evolutionary simulation exploring adaptation, selection, and survival strategies.

## How to run

Before installing, this step might differ based on whether you have CUDA installed on your system.
If you do, you will first need to install the correct version of CUDA by following
[PyTorch Installation Instructions](https://pytorch.org/).

If you do not have CUDA installed, you can install torch by simply running:

```bash
pip3 install torch
```

Other libraries can be installed with (tested with Python 3.10 and 3.11):

```bash
pip3 install matplotlib numpy "ray[rllib]" pygame gymnasium
```

## Examples

Examples are located in `src/examples/ray/rllib/examples/`. The ray library is added as a
submodule. You can clone it with `git submodule update --init --recursive`.
