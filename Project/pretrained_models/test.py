import torch
def test():
    path="e4e_ffhq_encode.pt"
    pretrained_dict = torch.load(path)
    print(pretrained_dict.items())



if __name__=="__main__":
        test()