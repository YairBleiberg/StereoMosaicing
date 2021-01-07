from scipy.signal import convolve2d
import numpy as np
from imageio import imread
from skimage.color import rgb2gray
from scipy import ndimage

def gaussian_kernel(kernel_size):
    conv_kernel = np.array([1, 1], dtype=np.float64)[:, None]
    conv_kernel = convolve2d(conv_kernel, conv_kernel.T)
    kernel = np.array([1], dtype=np.float64)[:, None]
    for i in range(kernel_size - 1):
        kernel = convolve2d(kernel, conv_kernel, 'full')
    return kernel / kernel.sum()


def blur_spatial(img, kernel_size):
    kernel = gaussian_kernel(kernel_size)
    blur_img = np.zeros_like(img)
    if len(img.shape) == 2:
        blur_img = convolve2d(img, kernel, 'same', 'symm')
    else:
        for i in range(3):
            blur_img[..., i] = convolve2d(img[..., i], kernel, 'same', 'symm')
    return blur_img


Z = 256


def read_image(filename, representation):
    im = imread(filename)
    if representation == 2:
        return (im.astype(np.float64))/(Z-1)
    else:
        if len(im.shape) == 3:
            return (rgb2gray(im).astype(np.float64)) / (Z - 1)
        else:
            return (im.astype(np.float64))/(Z-1)


def build_filter(filter_size):
    if filter_size == 1:
        return np.ones((1,1))
    filter = np.ones(2)
    for i in np.arange(filter_size-2):
        filter = np.convolve(filter, np.ones(2))
    filter /= np.sum(filter)
    return np.expand_dims(filter, axis=0)


def blur_and_reduce(im, filter_size):
    # first blur and take every 2nd pixel along x axis
    kernel = build_filter(filter_size)
    im = ndimage.filters.convolve(im, kernel, mode='mirror')
    im = im[:, ::2]
    # then do it along y axis
    im = ndimage.filters.convolve(im, kernel.transpose(), mode='mirror')
    im = im[::2, :]
    return im


def expand(im, filter_size):
    N, M = im.shape
    # first do along x axis
    kernel = build_filter(filter_size)
    im = np.insert(im, np.arange(1, M), 0,  axis=1)
    im = np.append(im, np.zeros((N,1)), axis=1)
    # twice the kernel in order to maintain same average pixel brightness when expanding
    im = ndimage.filters.convolve(im, 2*kernel, mode='mirror')
    # now, along y axis
    im = np.insert(im, np.arange(1, N), 0, axis=0)
    im = np.append(im, np.zeros((1, 2*M)), axis=0)
    im = ndimage.filters.convolve(im, 2*kernel.transpose(), mode='mirror')
    return im


def build_gaussian_pyramid(im, max_levels, filter_size):
    pyr = [im]
    for i in np.arange(max_levels-1):
        if np.min(im.shape) < 32:
            break
        im = blur_and_reduce(im, filter_size)
        pyr.append(im)
    return [pyr, build_filter(filter_size)]