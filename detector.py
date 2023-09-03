import cv2

# To capture video from webcam
# Might have to use 1 or 2 for parameter depending on if it's an integrated or usb webcam
img = cv2.imread("test.jpg")

# Load Trained CascadeClassifier XML
cascade = cv2.CascadeClassifier('cascade/cascade.xml')

rectangles = cascade.detectMultiScale(img)

for (x, y, w, h) in rectangles:
    cv2.putText(img, 'Red Panda', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
    break;


while True:
    # Display
    cv2.imshow('img', img)
    # Stop if escape key is pressed
    k = cv2.waitKey(1) & 0xff
    if k==27:
        break

#Delete any windows created
cv2.destroyallwindows()