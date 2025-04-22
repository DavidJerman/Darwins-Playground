import torch

def setup():
    print("----- Setup -----")

    used_device = 'cpu'

    if torch.cuda.is_available():
        device = torch.device('cuda')
        used_device = 'cuda'
        print('CUDA is available. Default device will be GPU.')
    else:
        device = torch.device('cpu')
        print('CUDA is not available. Default device will be  CPU.')

    sample_tensor = torch.randn(3, 4).to(device)
    print(f"Tensor on device: {sample_tensor.device}")

    print("----- Setup complete -----")

    return used_device
