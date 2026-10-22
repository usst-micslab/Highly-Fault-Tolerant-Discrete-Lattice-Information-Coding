import os

import bchlib
import numpy as np
from PIL import Image, ImageOps, ImageDraw
from model import Encoder
import torch
from torchvision import transforms

BCH_POLYNOMIAL = 37
BCH_BITS = 3
encoder = Encoder()

def encoded(secret):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str,default='model/encoder1.pth')
    parser.add_argument('--image', type=str, default=None)
    parser.add_argument('--images_dir', type=str, default=None)
    parser.add_argument('--save_dir', type=str, default=r'./images')
    parser.add_argument('--secret', type=str, default='cv')
    parser.add_argument('--secret_size', type=int, default=32)
    parser.add_argument('--cuda', type=bool, default=True)
    args = parser.parse_args()
    encoder = Encoder()

    encoder.load_state_dict(torch.load(args.model))
    encoder.eval()

    if args.cuda:
        encoder = encoder.cuda()

    bch = bchlib.BCH(BCH_POLYNOMIAL, BCH_BITS)

    if len(secret) > 2:
        print('Error: Can only encode 56bits (2 characters) with ECC')
        return

    data = bytearray(secret + ' ' * (2 - len(secret)), 'utf-8')
    ecc = bch.encode(data)
    packet = data + ecc

    packet_binary = ''.join(format(x, '08b') for x in packet)
    secret = [int(x) for x in packet_binary]


    secret = torch.tensor(secret, dtype=torch.float).unsqueeze(0)
    if args.cuda:
        secret = secret.cuda()

    width = 400
    height = 400
    size = (width, height)
    to_tensor = transforms.ToTensor()

    if args.save_dir is not None:
        if not os.path.exists(args.save_dir):
            os.makedirs(args.save_dir)

        with torch.no_grad():

            residual = encoder(secret)
            encoded =  residual
            encoded = torch.clamp(encoded, 0, 1)
            if args.cuda:

                encoded = encoded.cpu()
            encoded = np.array(encoded.squeeze(0).squeeze(0) * 255, dtype=np.uint8)

            save_name = "111"
            im = Image.fromarray(encoded)
            im.save('D:/html/vue02/src/assets' + '/' + save_name + '_hidden.png')
            return 'abc'




# if __name__ == "__main__":
#     encoded()
