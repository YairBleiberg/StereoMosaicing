Stereo Mosaicing

This project creates a stereo mosaic from a video, by first converting the video into many images, and using strips from each image to stitch together a panorama using RANSAC algorithm. A video of many of these panoramas from various strips creates a stereo mosaic. Feel free to try this with your own video. The raw video should be uploaded to the videos file. The camera should be held steady, and slowly move from left to right.
Run my_panorama.py in order to obtain the results, which will be in an mp4 file called my_panorama.mp4

In order to view the video, you may have to use a nonstandard video player, such as Windows Media Player.
The bonus video uses pyramid blending to blend together strips, but the results are not as good as with RANSAC.
