from PIL import Image
from Project.mapper.scripts.inference import run
from argparse import Namespace
def out(type):
    meta_data = {
        'afro': ['afro', False, False, True],
        'angry': ['angry', False, False, True],
        'Beyonce': ['beyonce', False, False, False],
        'bobcut': ['bobcut', False, False, True],
        'bowlcut': ['bowlcut', False, False, True],
        'curly hair': ['curly_hair', False, False, True],
        'Hilary Clinton': ['hilary_clinton', False, False, False],
        'Jhonny Depp': ['depp', False, False, False],
        'mohawk': ['mohawk', False, False, True],
        'purple hair': ['purple_hair', False, False, False],
        'surprised': ['surprised', False, False, True],
        'Taylor Swift': ['taylor_swift', False, False, False],
        'trump': ['trump', False, False, False],
        'Mark Zuckerberg': ['zuckerberg', False, False, False]
    }

    edit_type = type  # @param ['afro', 'angry', 'Beyonce', 'bobcut', 'bowlcut', 'curly hair', 'Hilary Clinton', 'Jhonny Depp', 'mohawk', 'purple hair', 'surprised', 'Taylor Swift', 'trump', 'Mark Zuckerberg']
    edit_id = meta_data[edit_type][0]
    latent_path = "static/latents/latents.pt"
    n_images = 1

    args = {
        "work_in_stylespace": False,
        "exp_dir": "static/img_out",
        "checkpoint_path": f"Project/notebook/mapper/pretrained/{edit_id}.pt",
        "couple_outputs": False,
        "mapper_type": "LevelsMapper",
        "no_coarse_mapper": meta_data[edit_type][1],
        "no_medium_mapper": meta_data[edit_type][2],
        "no_fine_mapper": meta_data[edit_type][3],
        "stylegan_size": 1024,
        "test_batch_size": 1,
        "latents_test_path": latent_path,
        "test_workers": 0,
        "n_images": n_images
    }
    run(Namespace(**args))
    '''result = Image.open(f"../../static/inference_results/00000.jpg")
    result = result.resize((int(result.width * 0.5), int(result.height * 0.5)))
    grid = Image.new("RGB", (result.width, result.height * n_images))
    grid.paste(result, (0, 0))
    for i in range(1, n_images):
        result = Image.open(f"results/inference_results/{str(i).zfill(5)}.jpg")
        result = result.resize((int(result.width * 0.5), int(result.height * 0.5)))
        grid.paste(result, (0, int(result.height * i)))'''

if __name__=="__main__":
    out("afro")