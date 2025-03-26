# Darwin's Playground

A multi-agent evolutionary simulation exploring adaptation, selection, and survival strategies.

## How to run

To run this project, you will need to install libraries listed in `requirements.txt` with
`pip install -r requirements.txt`. If you have an Nvidia GPU, you will also need to install
Nvidia's drivers, CUDA (12.8.1) and CUDnn (9.8.0).

You can install the latest version of torch with 
`pip install --pre torch --index-url https://download.pytorch.org/whl/nightly/cu128`.

## Examples

Examples are located in `src/examples/ray/rllib/examples/`. The ray library is added as a
submodule. You can clone it with `git submodule update --init --recursive`.
