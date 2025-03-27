# Darwin's Playground

A multi-agent evolutionary simulation exploring adaptation, selection, and survival strategies.

## How to run

You can install the latest version of torch with GPU CUDA support using 
`pip install --pre torch --index-url https://download.pytorch.org/whl/nightly/cu128`.
If you do not wish to use CUDA, install libraries listed in `requirements.txt` with
`pip install -r requirements.txt`. 

If you have an Nvidia GPU and decide to use it with the latest torch version,
you will also need to install Nvidia's drivers, CUDA (12.8.1) and CUDnn (9.8.0), as
well as packages listed in `requirements-nvidia.txt`. But first you need to install
the latest torch version as described above!

## Examples

Examples are located in `src/examples/ray/rllib/examples/`. The ray library is added as a
submodule. You can clone it with `git submodule update --init --recursive`.
