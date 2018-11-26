import face_recognition
import numpy as np
import cv2
pic='dog.png'
mask_ori = cv2.imread(pic,-1) 
cap = cv2.VideoCapture(0) #webcame video
cap.set(cv2.CAP_PROP_FPS, 30)
 
 
 
def transparentOverlay(src, overlay, pos=(0, 0), scale=1):
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape  # Size of foreground
    rows, cols, _ = src.shape  # Size of background Image
    y, x = pos[0], pos[1]  # Position of foreground/overlay image
 
    # loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
            src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
    return src
 
 
a,b,c=2,9/5,.8
d,e=5,6.5
while 1:
    ret, img = cap.read()
    rgb_frame = img[:, :, ::-1]
    facer = face_recognition.face_locations(rgb_frame)
    faces=[(0,0,0,0)]
    if facer != []:
        faces=[(int(facer[0][3]*5/6),int(facer[0][0]*8/7),int(abs(facer[0][3]-facer[0][1])),int(abs(facer[0][0]-facer[0][2])))]

    for (x, y, w, h) in faces:
        if h > 0 and w > 0:
 
            mask_symin = int(y- d * h / 5)
            mask_symax = int(y + e *h/ 5)
            sh_mask = mask_symax - mask_symin
 
            face_mask_roi_color = img[mask_symin:mask_symax, x:int(x*a)+w]

            mask= cv2.resize(mask_ori, (int(w*b), sh_mask),interpolation=cv2.INTER_CUBIC)
            transparentOverlay(face_mask_roi_color,mask,(0,0),c)
    cv2.imshow('Thugs Life', img)
 
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        cv2.imwrite('img.jpg', img)
        break
    if k==ord('d'):
        pic='dutert.png'
        mask_ori=cv2.imread(pic,-1)
        d,e=3,8
    if k==ord('s'):
        if pic=='dutert.png':
            pic='duterte.png'
            mask_ori=cv2.imread(pic,-1)
        else:
            pic='dog.png'
            mask_ori=cv2.imread(pic,-1)
            d,e=5,7
 
cap.release()
 
cv2.destroyAllWindows()
