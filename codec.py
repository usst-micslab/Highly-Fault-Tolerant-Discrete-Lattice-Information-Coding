"""Portable inference wrapper around the unchanged inherited DL-code networks."""
import argparse
import json
import os
from pathlib import Path
import sys

import bchlib
import numpy as np
from PIL import Image, ImageOps
import torch

ROOT = Path(__file__).resolve().parent


def text_to_bits(text):
    try:
        raw = text.encode('ascii')
    except UnicodeEncodeError as exc:
        raise ValueError('Use at most two ASCII bytes, not multibyte characters.') from exc
    if not 1 <= len(raw) <= 2:
        raise ValueError('The inherited text interface supports one or two ASCII bytes.')
    data = bytearray(raw.ljust(2, b' '))
    bch = bchlib.BCH(3, 37)
    packet = data + bch.encode(data)
    bits = np.unpackbits(np.frombuffer(packet, dtype=np.uint8)).astype(np.float32)
    if bits.size != 32:
        raise ValueError('Unexpected BCH packet size; use the pinned bchlib version.')
    return bits


def bits_to_text(bits):
    bits = np.asarray(bits).reshape(-1)
    if bits.size != 32 or not np.isfinite(bits).all():
        raise ValueError('Expected 32 finite predicted bits.')
    packet = bytearray(np.packbits(np.round(bits).astype(np.uint8)).tobytes())
    bch = bchlib.BCH(3, 37)
    data, ecc = packet[:-bch.ecc_bytes], packet[-bch.ecc_bytes:]
    errors = bch.decode(data, ecc)
    if errors < 0:
        return None, errors
    bch.correct(data, ecc)
    try:
        return data.decode('ascii').rstrip(' '), errors
    except UnicodeDecodeError:
        return None, errors


def load_networks(weights_dir, device):
    # Model source is left exactly as supplied. Do not import train.py: it starts training.
    os.environ.setdefault('MPLCONFIGDIR', str(ROOT/'.local/matplotlib'))
    sys.path.insert(0, str(ROOT/'train code/black_white'))
    from model import Encoder, Decoder
    directory = Path(weights_dir)
    paths = [directory/'encoder1.pth', directory/'decoder1.pth']
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError('Required trusted weight file: '+str(path))
    encoder, decoder = Encoder().to(device), Decoder().to(device)
    # PyTorch 1.11 has no weights_only loader; load only trusted, laboratory-supplied files.
    encoder.load_state_dict(torch.load(str(paths[0]), map_location=device), strict=True)
    decoder.load_state_dict(torch.load(str(paths[1]), map_location=device), strict=True)
    return encoder.eval(), decoder.eval()


def extract_bits(decoder, image_path, device):
    with Image.open(image_path) as opened:
        image = np.asarray(ImageOps.fit(opened.convert('L'), (400,400)), dtype=np.float32)/255.
    tensor = torch.from_numpy(image).reshape(1,1,400,400).to(device)
    with torch.no_grad():
        values = decoder(tensor)[0].cpu().numpy()
    if not np.isfinite(values).all():
        raise FloatingPointError('Non-finite decoder output')
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['roundtrip','encode','decode'])
    parser.add_argument('--weights-dir', default=str(ROOT/'train code/black_white/model'))
    parser.add_argument('--secret', default='cv')
    parser.add_argument('--image', help='Input code image for decode mode; not a cover image.')
    parser.add_argument('--output-dir', default=str(ROOT/'.local/output'))
    parser.add_argument('--name', default='lattice')
    parser.add_argument('--device', choices=['cpu','cuda'], default='cpu')
    parser.add_argument('--threads', type=int, default=2)
    args = parser.parse_args()
    if args.threads < 1:
        parser.error('--threads must be positive')
    if Path(args.name).name != args.name or args.name in ('.','..'):
        parser.error('--name must be a simple filename stem')
    if args.mode == 'decode' and not args.image:
        parser.error('--image is required in decode mode')
    if args.device == 'cuda' and not torch.cuda.is_available():
        parser.error('CUDA is unavailable; use --device cpu')
    torch.set_num_threads(args.threads)
    device = torch.device(args.device)
    encoder, decoder = load_networks(args.weights_dir, device)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    report = {'mode':args.mode,'device':str(device),'weights_included_in_release':False}
    if args.mode in ('encode','roundtrip'):
        try:
            expected_bits = text_to_bits(args.secret)
        except ValueError as exc:
            parser.error(str(exc))
        with torch.no_grad():
            image = encoder(torch.from_numpy(expected_bits).unsqueeze(0).to(device))[0,0].cpu().numpy()
        if image.shape != (400,400) or not np.isfinite(image).all():
            raise FloatingPointError('Invalid encoder output')
        image_path = output_dir/(args.name+'.png')
        Image.fromarray((np.clip(image,0,1)*255).astype(np.uint8)).save(image_path)
        report.update({'input_text':args.secret,'output_image':str(image_path.resolve()),'shape':[400,400]})
    else:
        image_path = Path(args.image)
    if args.mode in ('decode','roundtrip'):
        probabilities = extract_bits(decoder, image_path, device)
        bits = np.round(probabilities).astype(np.uint8)
        text, corrected = bits_to_text(bits)
        report.update({'raw_bits':bits.tolist(),'decoded_text':text,'bch_corrected_errors':corrected,
                       'decode_success':text is not None})
        if args.mode == 'roundtrip':
            report.update({'raw_bit_errors':int(np.count_nonzero(bits!=expected_bits)),
                           'exact_text_recovery':text==args.secret.rstrip(' ')})
    report_path = output_dir/(args.name+'_report.json')
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
