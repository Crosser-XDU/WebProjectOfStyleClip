import torch
import argparse
from Project.models.psp import pSp
import torch.onnx
import onnx
import onnxruntime

def setup_model(checkpoint_path, device='cpu'):
    model = onnx.load("e4e.onnx")
    onnx.checker.check_model(model)
    session = onnxruntime.InferenceSession("e4e.onnx")
    ckpt = torch.load(checkpoint_path)
    opts = ckpt['opts']
    opts['checkpoint_path'] = checkpoint_path
    opts['device'] = device
    latent_avg=ckpt['latent_avg']
    opts = argparse.Namespace(**opts)
    return session, opts,latent_avg


'''ckpt = torch.load(checkpoint_path)
    opts = ckpt['opts']

    opts['checkpoint_path'] = checkpoint_path
    opts['device'] = device
    opts = argparse.Namespace(**opts)

    net = pSp(opts).encoder
    net.eval()
    #net = net.to(device)
    x=torch.randn(1,3,1024,1024,requires_grad=False)
    torch.onnx.export(
        net,
        x,
        "e4e1.onnx",
        export_params = True,
        opset_version=11,  # the ONNX version to export the model to
        do_constant_folding=True,  # whether to execute constant folding for optimization
        input_names=['input'],  # the model's input names
        output_names=['output']
    )
    return net, opts
'''
''''
def load_e4e_standalone(checkpoint_path, device='cuda'):
    ckpt = torch.load(checkpoint_path, map_location='cpu')
    opts = argparse.Namespace(**ckpt['opts'])
    e4e = Encoder4Editing(50, 'ir_se', opts)
    e4e_dict = {k.replace('encoder.', ''): v for k, v in ckpt['state_dict'].items() if k.startswith('encoder.')}
    e4e.load_state_dict(e4e_dict)
    e4e.eval()
    e4e = e4e.to(device)
    latent_avg = ckpt['latent_avg'].to(device)

    def add_latent_avg(model, inputs, outputs):
        return outputs + latent_avg.repeat(outputs.shape[0], 1, 1)

    e4e.register_forward_hook(add_latent_avg)
    return e4e
'''