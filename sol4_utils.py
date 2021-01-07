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


def build_laplacian_pyramid(im, max_levels, filter_size):
    pyr, filter_vec = build_gaussian_pyramid(im, max_levels, filter_size)
    for i in range(len(pyr)-1):
        pyr[i] = pyr[i] - expand(pyr[i+1], filter_size)
    return [pyr, filter_vec]


def laplacian_to_image(lpyr, filter_vec, coeff):
    # we reverse the pyramid to start the sum from the bottom
    lpyr.reverse()
    coeff.reverse()
    img = coeff[0]*lpyr[0]
    for i in np.arange(1, len(lpyr)):
        img = expand(img, filter_vec.size) + coeff[i]*lpyr[i]
    return img


def render_pyramid(pyr, levels):
    res = (pyr[0]-np.amin(pyr[0]))/(np.amax(pyr[0])-np.amin(pyr[0]))
    N, M = pyr[0].shape
    for i in np.arange(1, levels):
        normalized_level = (pyr[i]-np.amin(pyr[i]))/(np.amax(pyr[i])-np.amin(pyr[i]))
        add_level = np.pad(normalized_level, ((0, N-pyr[i].shape[0]), (0, 0)), mode='constant')
        res = np.append(res, add_level, axis=1)
    return res



def pyramid_blending(im1, im2, mask, max_levels, filter_size_im, filter_size_mask):
        im_blend = np.zeros(im1.shape)
        for channel in range(3):
            L1, filter_vec = build_laplacian_pyramid(im1[:,:,channel], max_levels, filter_size_im)
            L2, filter_vec = build_laplacian_pyramid(im2[:,:,channel], max_levels, filter_size_im)
            Gm, filter_vec = build_gaussian_pyramid(np.float64(mask), max_levels, filter_size_mask)
            Lout = []
            for i in range(len(L1)):
                Lout.append(L1[i]*Gm[i] + L2[i]*(1-Gm[i]))
            im_blend[:,:,channel] = laplacian_to_image(Lout, build_filter(filter_size_im), np.ones(len(Lout)).tolist())
        return np.clip(im_blend, 0, 1)
