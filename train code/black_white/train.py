import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

import utils
from tensorboardX import SummaryWriter

class Flatten(nn.Module):
    def __init__(self):
        super(Flatten, self).__init__()

    def forward(self, input):
        return input.view(input.size(0), -1)
class Dense(nn.Module):
    def __init__(self, in_features, out_features, activation='relu', kernel_initializer='he_normal'):
        super(Dense, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.activation = activation
        self.kernel_initializer = kernel_initializer

        self.linear = nn.Linear(in_features, out_features)
        # initialization
        if kernel_initializer == 'he_normal':
            nn.init.kaiming_normal_(self.linear.weight)
        else:
            raise NotImplementedError

    def forward(self, inputs):
        outputs = self.linear(inputs)
        if self.activation is not None:
            if self.activation == 'relu':
                outputs = nn.ReLU(inplace=True)(outputs)
        return outputs


# 定义编码器
class Conv2D(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3, activation='relu', strides=1):
        super(Conv2D, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.activation = activation
        self.strides = strides

        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, strides, int((kernel_size - 1) / 2))
        # default: using he_normal as the kernel initializer
        nn.init.kaiming_normal_(self.conv.weight)

    def forward(self, inputs):
        outputs = self.conv(inputs)
        if self.activation is not None:
            if self.activation == 'relu':
                outputs = nn.ReLU(inplace=True)(outputs)
            else:
                raise NotImplementedError
        return outputs
class Encoder(nn.Module):
    def __init__(self):
        super(Encoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(32, 128), # 假设输入是32位信息
            nn.ReLU(),
            nn.Linear(128, 400*400) # 输出为400x400像素的图像，展平状态
        )
        self.conv1 = Conv2D(1, 32, 3, activation='relu')
        self.conv2 = Conv2D(32, 32, 3, activation='relu', strides=2)
        self.conv3 = Conv2D(32, 64, 3, activation='relu', strides=2)
        self.conv4 = Conv2D(64, 128, 3, activation='relu', strides=2)
        self.conv5 = Conv2D(128, 256, 3, activation='relu', strides=2)
        self.up6 = Conv2D(256, 128, 3, activation='relu')
        self.conv6 = Conv2D(256, 128, 3, activation='relu')
        self.up7 = Conv2D(128, 64, 3, activation='relu')
        self.conv7 = Conv2D(128, 64, 3, activation='relu')
        self.up8 = Conv2D(64, 32, 3, activation='relu')
        self.conv8 = Conv2D(64, 32, 3, activation='relu')
        self.up9 = Conv2D(32, 32, 3, activation='relu')
        self.conv9 = Conv2D(65, 32, 3, activation='relu')
        self.residual = Conv2D(32, 1, 1, activation=None)


    def forward(self, x):
        encoded = self.encoder(x)
        inputs = encoded.view(-1, 1, 400, 400)
        conv1 = self.conv1(inputs)
        conv2 = self.conv2(conv1)
        conv3 = self.conv3(conv2)
        conv4 = self.conv4(conv3)
        conv5 = self.conv5(conv4)
        up6 = self.up6(nn.Upsample(scale_factor=(2, 2))(conv5))
        merge6 = torch.cat([conv4, up6], dim=1)
        conv6 = self.conv6(merge6)
        up7 = self.up7(nn.Upsample(scale_factor=(2, 2))(conv6))
        merge7 = torch.cat([conv3, up7], dim=1)
        conv7 = self.conv7(merge7)
        up8 = self.up8(nn.Upsample(scale_factor=(2, 2))(conv7))
        merge8 = torch.cat([conv2, up8], dim=1)
        conv8 = self.conv8(merge8)
        up9 = self.up9(nn.Upsample(scale_factor=(2, 2))(conv8))
        merge9 = torch.cat([conv1, up9, inputs], dim=1)
        conv9 = self.conv9(merge9)
        residual = self.residual(conv9)
        residual  = torch.where(residual >= 0.08, torch.ones_like(residual), torch.zeros_like(residual))
        return residual

def transform_net(encoded_image,  global_step):
    sh = encoded_image.size()
    ramp_fn = lambda ramp: np.min([global_step / ramp, 1.])

    rnd_bri = ramp_fn(1000) * 0.3
    rnd_hue = ramp_fn(1000) * 0.1
    rnd_brightness = utils.get_rnd_brightness_torch(rnd_bri, rnd_hue, batch_size)  # [batch_size, 3, 1, 1]
    jpeg_quality = 100. - torch.rand(1)[0] * ramp_fn(1000) * (100. - 50)
    rnd_noise = torch.rand(1)[0] * ramp_fn(1000) * 0.02

    contrast_low = 1. - (1. - 0.5) * ramp_fn(1000)
    contrast_high = 1. + (1.5 - 1.) * ramp_fn(1000)
    contrast_params = [contrast_low, contrast_high]

    rnd_sat = torch.rand(1)[0] * ramp_fn(1000) * 1.0

    # blur
    N_blur = 7
    f = utils.random_blur_kernel(probs=[.25, .25], N_blur=N_blur, sigrange_gauss=[1., 3.], sigrange_line=[.25, 1.],
                                 wmin_line=3)

    f = f.cuda()
    encoded_image = F.conv2d(encoded_image, f, bias=None, padding=int((N_blur - 1) / 2))

    # noise
    noise = torch.normal(mean=0, std=rnd_noise, size=encoded_image.size(), dtype=torch.float32)

    noise = noise.cuda()
    encoded_image = encoded_image + noise
    encoded_image = torch.clamp(encoded_image, 0, 1)


    # contrast & brightness
    contrast_scale = torch.Tensor(encoded_image.size()[0]).uniform_(contrast_params[0], contrast_params[1])
    contrast_scale = contrast_scale.reshape(encoded_image.size()[0], 1, 1, 1)


    contrast_scale = contrast_scale.cuda()
    rnd_brightness = rnd_brightness.cuda()
    encoded_image = encoded_image * contrast_scale
    encoded_image = encoded_image + rnd_brightness
    encoded_image = torch.clamp(encoded_image, 0, 1)


    # saturation
    sat_weight = torch.FloatTensor([.3, .6, .1]).reshape(1, 3, 1, 1)

    sat_weight = sat_weight.cuda()
    encoded_image_lum = torch.mean(encoded_image * sat_weight, dim=1).unsqueeze_(1)
    encoded_image = (1 - rnd_sat) * encoded_image + rnd_sat * encoded_image_lum

    # jpeg
    encoded_image = encoded_image.reshape([-1, 1, 400, 400])
    if not True:
        encoded_image = utils.jpeg_compress_decompress(encoded_image, rounding=utils.round_only_at_0,
                                                       quality=jpeg_quality)

    return encoded_image

# 定义解码器
class Decoder(nn.Module):
    def __init__(self):
        super(Decoder, self).__init__()
        self.decoder = nn.Sequential(
            Conv2D(1, 32, 3, strides=2, activation='relu'),
            Conv2D(32, 32, 3, activation='relu'),
            Conv2D(32, 64, 3, strides=2, activation='relu'),
            Conv2D(64, 64, 3, activation='relu'),
            Conv2D(64, 64, 3, strides=2, activation='relu'),
            Conv2D(64, 128, 3, strides=2, activation='relu'),
            Conv2D(128, 128, 3, strides=2, activation='relu'),
            Flatten(),
            Dense(21632, 512, activation='relu'),
            Dense(512, 32, activation=None))

    def forward(self, x):
        return torch.sigmoid(self.decoder(x))

# 实例化模型
encoder = Encoder().cuda()
decoder = Decoder().cuda()

# 定义损失函数和优化器
criterion = nn.MSELoss()
params = list(encoder.parameters()) + list(decoder.parameters())
optimizer = optim.Adam(params, lr=0.001)

# 示例输入（32位信息）
batch_size = 4




def get_secret_acc(secret_true, secret_pred):
    if 'cuda' in str(secret_pred.device):
        secret_pred = secret_pred.cpu()
        secret_true = secret_true.cpu()
    secret_pred = torch.round(secret_pred)
    correct_pred = torch.sum((secret_pred - secret_true) == 0, dim=1)
    str_acc = 1.0 - torch.sum((correct_pred - secret_pred.size()[1]) != 0).numpy() / correct_pred.size()[0]
    bit_acc = torch.sum(correct_pred).numpy() / secret_pred.numel()
    return bit_acc, str_acc


def build_model(encoder, decoder,
                  global_step, writer):
    secret_input  = torch.randint(0, 2, (batch_size, 32), dtype=torch.uint8).float().cuda()
    residual_warped = encoder(secret_input)
    encoded_warped = torch.clamp(residual_warped, 0, 1)

    # transformed_image = transform_net(encoded_warped, global_step)

    decoded_secret = decoder(encoded_warped)
    bit_acc, str_acc = get_secret_acc(secret_input, decoded_secret)

    criterion = nn.MSELoss().cuda()

    cross_entropy = nn.BCELoss()

    cross_entropy = cross_entropy.cuda()
    secret_loss = cross_entropy(decoded_secret, secret_input)
    white_image =  torch.ones((4, 1, 400, 400), dtype=torch.uint8).float().cuda()
    img_loss = criterion(white_image, encoded_warped)
    if global_step < 1000:
        loss = secret_loss
    else:
        loss = img_loss + secret_loss*0.1






    writer.add_scalar('loss/secret_loss', secret_loss, global_step)
    writer.add_scalar('loss/loss', loss, global_step)

    writer.add_scalar('metric/bit_acc', bit_acc, global_step)
    writer.add_scalar('metric/str_acc', str_acc, global_step)
    if global_step % 20 == 0:
        # writer.add_image('input/image_input', image_input[0], global_step)
        # writer.add_image('input/image_warped', input_warped[0], global_step)
        writer.add_image('encoded/encoded_warped', encoded_warped[0], global_step)
        writer.add_image('encoded/residual_warped', residual_warped[0] + 0.5, global_step)
        # writer.add_image('encoded/encoded_image', encoded_image[0], global_step)
        # writer.add_image('transformed/transformed_image', transformed_image[0], global_step)
        # writer.add_image('transformed/test', test_transform[0], global_step)

    return loss, secret_loss,img_loss, bit_acc, str_acc


def train(global_steps):
    writer = SummaryWriter()
    for global_step in range(global_steps):

        loss, secret_loss, img_loss, bit_acc, str_acc =  build_model(encoder, decoder, global_step, writer)
        print(f"global_step : {global_step}, loss: {loss}, secret_loss: {secret_loss}")


        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if global_step % 1000 == 0:
            torch.save(encoder.state_dict(), 'model/encoder.pth')
            torch.save(decoder.state_dict(), 'model/decoder.pth')

train(14000)