# WHU-SEN-City
A paired SAR-to-optical image translation dataset which covers 34 big cities of China.
The Sentinel-2 and pseudo-color Sentinel-1 images were uploaded to this project.

The original paired Sentinel-1 and Sentinel-2 images of WHU-SEN-City are uploading (The uploading is not finished yet, we will upload all images ASAP).
You can use the python codes of this project to split the images to small paired patches. The detailed steps are as below:

1) Download the WHU-SEN-City dataset from the below link:
https://drive.google.com/drive/folders/1Eas1qXHdzseEdkjY-0jNp67F6PGrBJ2i?usp=sharing
For Chinese users, you also can download the data from this link:
https://pan.baidu.com/s/1hIicX-X98gdfZmEUSvVbVA  Auth code: n8pv 

(2) Unzip all files(including the files in subfolders) and put the dataset to the folder of this project.

(3) Run read_sen_dataset.py to split the images.

Requirements:
Python > 3.5
numpy
opencv
scipy