import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

ORANGE_MIN = np.array([5, 50, 225],np.uint8)
ORANGE_MAX = np.array([20, 255, 255],np.uint8)

def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist
def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar

cap = cv2.VideoCapture(0)

while cap.isOpened():

    ret, frame = cap.read()
    cv2.imshow('Capturing', frame)
    height, width, _ = frame.shape

    # convert to hsv colorspace
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # find the colors within the boundaries
    mask = cv2.inRange(hsv, ORANGE_MIN, ORANGE_MAX)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)

    if contours:

        max_cnt = sorted(contours, key=lambda cnt: cv2.contourArea(cnt), reverse = True)[0]

        # cv2.drawContours(frame, [max_cnt], -1, (0, 255, 0), 2)
        x, y, w, h = cv2.boundingRect(max_cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        cv2.imshow('Capturing', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            img = frame
            cv2.destroyAllWindows()
            cap.release()
            break

img = img[y:y+h, x:x+w]

cv2.imshow('Captured', img)

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
clt = KMeans(n_clusters=3) #cluster number
clt.fit(img)

hist = find_histogram(clt)
bar = plot_colors2(hist, clt.cluster_centers_)

plt.axis("off")
plt.imshow(bar)
plt.show()