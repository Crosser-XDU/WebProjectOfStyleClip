import torch
from torch import nn
from Project.models.encoders import psp_encoders
from Project.configs.paths_config import model_paths


def get_keys(d, name):
    if 'state_dict' in d:
        d = d['state_dict']
    d_filt = {k[len(name) + 1:]: v for k, v in d.items() if k[:len(name)] == name}
    return d_filt


class pSp(nn.Module):

    def __init__(self, opts):
        super(pSp, self).__init__()
        self.opts = opts
        # Define architecture
        self.encoder = self.set_encoder()
        # Load weights if needed
        self.load_weights()

    def set_encoder(self):
        if self.opts.encoder_type == 'GradualStyleEncoder':
            encoder = psp_encoders.GradualStyleEncoder(50, 'ir_se', self.opts)
        elif self.opts.encoder_type == 'Encoder4Editing':
            encoder = psp_encoders.Encoder4Editing(50, 'ir_se', self.opts)
        elif self.opts.encoder_type == 'SingleStyleCodeEncoder':
            encoder = psp_encoders.BackboneEncoderUsingLastLayerIntoW(50, 'ir_se', self.opts)
        else:
            raise Exception('{} is not a valid encoders'.format(self.opts.encoder_type))
        return encoder

    def load_weights(self):
        if self.opts.checkpoint_path is not None:
            print('Loading e4e over the pSp framework from checkpoint: {}'.format(self.opts.checkpoint_path))
            ckpt = torch.load(self.opts.checkpoint_path)
            self.encoder.load_state_dict(get_keys(ckpt, 'encoder'), strict=False)
            self.__load_latent_avg(ckpt)
        else:
            print('Loading encoders weights from irse50!')
            encoder_ckpt = torch.load(model_paths['ir_se50'])
            self.encoder.load_state_dict(encoder_ckpt, strict=False)
            print('Loading decoder weights from pretrained!')
            ckpt = torch.load(self.opts.stylegan_weights)
            self.decoder.load_state_dict(ckpt['g_ema'], strict=False)
            self.__load_latent_avg(ckpt, repeat=self.encoder.style_count)

    def forward(self, x, resize=False, latent_mask=None, input_code=False, randomize_noise=True,
                inject_latent=None, return_latents=False, alpha=None):
        if input_code:
            codes = x
        else:
            codes = self.encoder(x)
            # normalize with respect to the center of an average face
            if self.opts.start_from_latent_avg:
                if codes.ndim == 2:
                    codes = codes + self.latent_avg.repeat(codes.shape[0], 1, 1)[:, 0, :]
                else:
                    codes = codes + self.latent_avg.repeat(codes.shape[0], 1, 1)

        if latent_mask is not None:
            for i in latent_mask:
                if inject_latent is not None:
                    if alpha is not None:
                        codes[:, i] = alpha * inject_latent[:, i] + (1 - alpha) * codes[:, i]
                    else:
                        codes[:, i] = inject_latent[:, i]
                else:
                    codes[:, i] = 0

        input_is_latent = not input_code
        images, result_latent = self.decoder([codes],
                                             input_is_latent=input_is_latent,
                                             randomize_noise=randomize_noise,
                                             return_latents=return_latents)

        if resize:
            images = self.face_pool(images)

        if return_latents:
            return images, result_latent
        else:
            return images

    def __load_latent_avg(self, ckpt, repeat=None):
        if 'latent_avg' in ckpt:
            self.latent_avg = ckpt['latent_avg'].to(self.opts.device)
        elif self.opts.start_from_latent_avg:
            # Compute mean code based on a large number of latents (10,000 here)
            with torch.no_grad():
                self.latent_avg = self.decoder.mean_latent(10000).to(self.opts.device)
        else:
            self.latent_avg = None
        if repeat is not None and self.latent_avg is not None:
            self.latent_avg = self.latent_avg.repeat(repeat, 1)

class opts():
    def __init__(self,enco,path,size,dev,start_from_latent_avg):
        self.encoder_type=enco
        self.checkpoint_path=path
        self.stylegan_size=size
        self.device=dev
        self.start_from_latent_avg=start_from_latent_avg