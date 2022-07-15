from pathlib import Path
import torch

PATH = str(Path(__file__).parent.parent.resolve()) + '/'
DATA_DIR = PATH + 'test_data/'

USING_GPU = torch.cuda.is_available()
device = torch.device('cuda' if USING_GPU else 'cpu')

if __name__ == '__main__':
    if USING_GPU:
        print('This device supports CUDA. Torch will run on the GPU.')
    else:
        print('This device does not support CUDA. Torch will run on the CPU.')
