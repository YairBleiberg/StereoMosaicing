Stereo Mosaicing


https://user-images.githubusercontent.com/107566470/211909072-2c86a3f6-3e8c-4ea5-ae62-3603f9588015.mp4


A stereo mosaic is a video of panoramas, where at each frame in the video, the panorama is of a "push broom" camera with a different angle. That is, at first there will be a panorama taken by a left-facing camera, then by a center facing camera, etc.
![image](https://user-images.githubusercontent.com/107566470/211910371-23fb7d11-3cdc-480c-8150-33d62511c632.png)


This is obtained by gathering all the strips representing parts of the photo
This project creates a stereo mosaic from a video, by first converting the video into many images, and using strips from each image to stitch together a panorama using RANSAC algorithm. A video of many of these panoramas from various strips creates a stereo mosaic. Feel free to try this with your own video. The raw video should be uploaded to the videos file. The camera should be held steady, and slowly move from left to right.
Run my_panorama.py in order to obtain the results, which will be in an mp4 file called my_panorama.mp4

In order to view the video, you may have to use a nonstandard video player, such as Windows Media Player.
The bonus video uses pyramid blending to blend together strips, but the results are not as good as with RANSAC.
