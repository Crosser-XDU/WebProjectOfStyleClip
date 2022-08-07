from Project.aligned_image.aligned_images import align
from Project.scripts.inference import inference
from Project.notebook.out import out
def final(type):
    # @param ['afro', 'angry', 'Beyonce', 'bobcut', 'bowlcut', 'curly hair', 'Hilary Clinton', 'Jhonny Depp', 'mohawk', 'purple hair', 'surprised', 'Taylor Swift', 'trump', 'Mark Zuckerberg']
    align()
    inference()
    out(type)

if __name__=="__main__":
    final('afro')
