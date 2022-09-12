from glob import glob
import cv2
import matplotlib.pyplot as plt
import multiprocessing
from tqdm import tqdm
from functools import partial
IMG_SIZE = 224
n_cpus = multiprocessing.cpu_count()


def resize_images(list_of_files):
    """
        Resize all images in the list
    """
    for filepath in tqdm(list_of_files):
        try:
            image = plt.imread(filepath)
            image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
            filename = filepath.split("/")[1]
            plt.imsave("artic-images-resized/{}".format(filename), image)
        except:
            print("Failed:", filepath)
            continue


if __name__ == "__main__":
    all_image_filenames = glob("artic-images/*.jpg")
    # Divide the list of files into n_cpu number of
    # chunks and resize the images in the lists 
    # in parallel
    parallel_processes = []
    for i in range(n_cpus):
        p = multiprocessing.Process(target=partial(
            resize_images, all_image_filenames[i::n_cpus]))
        parallel_processes.append(p)
    for proc in parallel_processes:
        proc.start()
