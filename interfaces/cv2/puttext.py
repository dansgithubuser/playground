import cv2

a = cv2.imread('../../gull.jpg')
for i, color in enumerate([(0, 0, 0), (255, 128, 0)]):
    a = cv2.putText(
        a,
        'AAAAAAAAAAAAA',
        (8, 600-8),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2-i,
    )
cv2.imwrite('aaaaaaaa.jpg', a)
