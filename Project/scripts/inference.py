import argparse

import torch
import os

from Project.configs import data_configs
from Project.datasets.inference_dataset import InferenceDataset
from torch.utils.data import DataLoader
from Project.utils.model_utils import setup_model

def main(args,device):
    net, opts ,latent_avg= setup_model(args.ckpt, device)
    is_cars = 'cars_' in opts.dataset_type
    args, data_loader = setup_data_loader(args, opts)
    # Check if latents exist
    latents_file_path = os.path.join(args.save_dir, 'latents.pt')
    latent_codes = get_all_latents(net, device,data_loader,latent_avg, args.n_sample, is_cars=is_cars)
    torch.save(latent_codes, latents_file_path)



def setup_data_loader(args, opts):
    dataset_args = data_configs.DATASETS[opts.dataset_type]
    transforms_dict = dataset_args['transforms'](opts).get_transforms()
    images_path = args.images_dir if args.images_dir is not None else dataset_args['test_source_root']
    print(f"images path: {images_path}")
    align_function = None
    test_dataset = InferenceDataset(root=images_path,
                                    transform=transforms_dict['transform_test'],
                                    preprocess=align_function,
                                    opts=opts)

    data_loader = DataLoader(test_dataset,
                             batch_size=args.batch,
                             shuffle=False,
                             num_workers=0,
                             drop_last=True)

    print(f'dataset length: {len(test_dataset)}')

    if args.n_sample is None:
        args.n_sample = len(test_dataset)
    return args, data_loader


def get_latents(net, x,latent_avg, is_cars=False):
    input = {net.get_inputs()[0].name: to_numpy(x)}
    codes = net.run(None,input)
    codes=torch.from_numpy(codes[0])
    if codes.ndim == 2:
        codes = codes + latent_avg.repeat(codes.shape[0], 1, 1)[:, 0, :]
    else:
        codes = codes + latent_avg.repeat(codes.shape[0], 1, 1)
    return codes


def get_all_latents(net, device ,data_loader, latent_avg,n_images=None, is_cars=False):
    all_latents = []
    with torch.no_grad():
        for batch in data_loader:
            x = batch
            inputs = x.float()
            latents = get_latents(net, inputs,latent_avg, is_cars)
            all_latents.append(latents)
    return torch.cat(all_latents)

#@torch.no_grad()
#def generate_inversions(args, g, latent_codes, is_cars):
#    print('Saving inversion images')
#    inversions_directory_path = os.path.join(args.save_dir, 'inversions')
#    os.makedirs(inversions_directory_path, exist_ok=True)
#    for i in range(min(args.n_sample, len(latent_codes))):
#        imgs, _ = g([latent_codes[i].unsqueeze(0)], input_is_latent=True, randomize_noise=False, return_latents=True)
#        if is_cars:
#            imgs = imgs[:, :, 64:448, :]
#        save_image(imgs[0], inversions_directory_path, i + 1)


#def run_alignment(image_path):
#    predictor = dlib.shape_predictor(paths_config.model_paths['shape_predictor'])
#    aligned_image = align_face(filepath=image_path, predictor=predictor)
 #   print("Aligned image has shape: {}".format(aligned_image.size))
 #   return aligned_image

def to_numpy(tensor):
    return tensor.cpu().numpy()

def inference():
    device = "cpu"
    parser = argparse.ArgumentParser(description="Inference")
    parser.add_argument("--images_dir", type=str, default='static/img_aligned',
                        help="The directory of the images to be inverted")
    parser.add_argument("--save_dir", type=str, default='static/latents',
                        help="The directory to save the latent codes and inversion images. (default: images_dir")
    parser.add_argument("--batch", type=int, default=1, help="batch size for the generator")
    parser.add_argument("--n_sample", type=int, default=None, help="number of the samples to infer.")
    parser.add_argument("--latents_only", action="store_true",default=True, help="infer only the latent codes of the directory")
    parser.add_argument("--align", action="store_true",default=False,help="align face images before inference")
    parser.add_argument("--ckpt", default='Project/pretrained_models/e4e_ffhq_encode.pt',help="path to generator checkpoint")

    args = parser.parse_args()
    main(args,device)

if __name__=="__main__":
    inference()