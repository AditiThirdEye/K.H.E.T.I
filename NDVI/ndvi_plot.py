# Libraries required
import rasterio 
import numpy as np
import cv2
import matplotlib.pyplot as plt

# function
def get_average_NDVI(ndvi2,x1,x2,y1,y2):
  sum=0
  total=0
  for i in range(x1,x2):
    for j in range(y1,y2):
      sum+=ndvi2[i][j]
      total+=1
  return sum/total

# get the input images here
band_red2 = rasterio.open('/data/IMG_0605_3.tif')
band_nir2 = rasterio.open('/data/IMG_0605_4.tif')

red2 = band_red2.read(1).astype('float64')
nir2 = band_nir2.read(1).astype('float64')
ndvi2= (nir2-red2)/(nir2+red2)

rgb_matrix = np.zeros((ndvi2.shape[0],ndvi2.shape[1],3), np.uint8)

res = ndvi2.copy()
for i in range(ndvi2.shape[0]):
  for j in range(ndvi2.shape[1]):
        if(res[i][j] >=-1 and res[i][j] <0):
            rgb_matrix[i][j]=[128,128,128]
        elif(res[i][j]>=0 and res[i][j]<0.15):
            rgb_matrix[i][j]=[0,128,255]  
        elif(res[i][j]>=0.15 and res[i][j]<0.30):
            rgb_matrix[i][j]=[125,255,255]
        elif(res[i][j]>=0.3 and res[i][j]<0.45):
            rgb_matrix[i][j]=[64,255,0] 
        elif(res[i][j]>=0.45 and res[i][j]<0.6):
            rgb_matrix[i][j]=[64,255,0] 
        else:
            rgb_matrix[i][j]=[0,128,128]

NDVI_avg = [get_average_NDVI(ndvi2,0,480,0,426),get_average_NDVI(ndvi2,0,480,426,852),get_average_NDVI(ndvi2,0,480,852,1280),
            get_average_NDVI(ndvi2,480,960,0,426), get_average_NDVI(ndvi2,480,960,426,852), get_average_NDVI(ndvi2,480,960,852,1280)]

img1 = rgb_matrix.copy()
cv2.rectangle(img1,(0, 0),(426, 480),(255, 0, 0),5)
cv2.rectangle(img1,(0, 480),(426, 959),(255, 0, 0),5)
cv2.rectangle(img1,(426, 0),(852, 480),(255, 0, 0),5)
cv2.rectangle(img1,(426, 480),(852, 959),(255, 0, 0),5)
cv2.rectangle(img1,(852, 0),(1279, 480),(255, 0, 0),5)
cv2.rectangle(img1,(852, 480),(1279, 959),(255, 0, 0),5)

colors = []
rules = []
for i in range(0,6):
  if NDVI_avg[i]<0.10:
    colors.append((0,0,255))
    rules.append(i+1)
  else:
    colors.append((0,0,0))

cv2.putText(img1, "1", (180, 260), cv2.FONT_HERSHEY_SIMPLEX, 4, colors[0], 10)
cv2.putText(img1, "2", (600, 260), cv2.FONT_HERSHEY_SIMPLEX, 4, colors[1], 10)
cv2.putText(img1, "3", (1000, 260), cv2.FONT_HERSHEY_SIMPLEX, 4, colors[2], 10)
cv2.putText(img1, "4", (180, 760), cv2.FONT_HERSHEY_SIMPLEX, 4, colors[3], 10)
cv2.putText(img1, "5", (600, 760), cv2.FONT_HERSHEY_SIMPLEX, 4, colors[4], 10)
cv2.putText(img1, "6", (1000, 760), cv2.FONT_HERSHEY_SIMPLEX, 4, colors[5], 10)

plt.figure(figsize = (10,10))
test_img4 = cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
plt.imshow(test_img4)
print("Please look after plot no.",rules," The crops have lower produce in this area so make sure you add more fertilizer to crops in these plots")

