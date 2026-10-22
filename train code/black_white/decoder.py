import glob
import bchlib
import numpy as np
from PIL import Image, ImageOps
import torch
from torchvision import transforms
from model import Decoder
BCH_POLYNOMIAL = 37
BCH_BITS = 3


def decoded(url):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str,default='model/decoder1.pth')
    parser.add_argument('--image', type=str, default=None)
    parser.add_argument('--images_dir', type=str, default=None)
    parser.add_argument('--secret_size', type=int, default=100)
    parser.add_argument('--cuda', type=bool, default=True)
    args = parser.parse_args()


    files_list = [url]
    # elif args.images_dir is not None:
    #     files_list = glob.glob(args.images_dir + '/*')
    # else:
    #     print('Missing input image')
    #     return
    decoder = Decoder()
    decoder.load_state_dict(torch.load(args.model))


    decoder.eval()
    if args.cuda:
        decoder = decoder.cuda()

    bch = bchlib.BCH(BCH_POLYNOMIAL, BCH_BITS)

    width = 400
    height = 400
    size = (width, height)
    to_tensor = transforms.ToTensor()

    with torch.no_grad():
        for filename in files_list:
            image = Image.open(filename)
            image = ImageOps.fit(image, size)
            image = to_tensor(image).unsqueeze(0)
            if args.cuda:
                image = image.cuda()

            secret = decoder(image)
            if args.cuda:
                secret = secret.cpu()
            secret = np.array(secret[0])
            print(secret)
            secret = np.round(secret)
            print(secret)

            packet_binary = "".join([str(int(bit)) for bit in secret[:32]])
            packet = bytes(int(packet_binary[i: i + 8], 2) for i in range(0, len(packet_binary), 8))
            packet = bytearray(packet)

            data, ecc = packet[:-bch.ecc_bytes], packet[-bch.ecc_bytes:]

            bitflips = bch.decode_inplace(data, ecc)

            if bitflips != -1:
                try:
                    code = data.decode("utf-8")
                    return code
                except:
                    return '-1'
            return '-1'


if __name__ == "__main__":
    decoded()
