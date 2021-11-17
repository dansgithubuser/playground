import cv2

a = cv2.imread('../../gull.jpg')
b = cv2.imread('../../goose.jpg')
b = cv2.resize(b, (800, 600))
c = cv2.hconcat([a, b])
cv2.imwrite('gullgoose.jpg', c)
