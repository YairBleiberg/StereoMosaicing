Stereo Mosaicing


https://user-images.githubusercontent.com/107566470/211909072-2c86a3f6-3e8c-4ea5-ae62-3603f9588015.mp4


A stereo mosaic is a video of panoramas, where at each frame in the video, the panorama is of a "push broom" camera with a different angle. That is, at first there will be a panorama taken by a left-facing camera, then by a center facing camera, etc.

![image](https://user-images.githubusercontent.com/107566470/211910371-23fb7d11-3cdc-480c-8150-33d62511c632.png =400x200)


To simplify slightly, this is obtained by stitching together into a panorama all the leftmost strips of the series of images to obtain the "left-facing camera", all the center strips to obtain the "center-facing camera", etc.
We use Harris corner detector algorithm to detect points of interest in each image, extract their MOPS-like descriptors, and use RANSAC algorithm in order to find the homography that best describes the transformation between two adjacent images. We then align all the images, and take appropriate strips to generate the mosaic, using appropriate blending to ensure the images generated have as few artifacts as possible. 


Feel free to try this with your own video. The raw video should be uploaded to the videos file. The camera should be held steady, and slowly move from left to right.
Run my_panorama.py in order to obtain the results, which will be in an mp4 file called my_panorama.mp4

In order to view the video, you may have to use a nonstandard video player, such as Windows Media Player.
The bonus video uses pyramid blending to blend together strips, but the results are not as good as with RANSAC.
