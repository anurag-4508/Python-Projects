import cv2


src = cv2.imread("myImg.jpg", cv2.IMREAD_UNCHANGED)
print('Original Dimensions : ',src.shape)

def resizeImage(scale_percent):
    width = int(src.shape[1] * scale_percent / 100)
    height = int(src.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(src, dim)

    cv2.imshow("Resized image", resized)
    imgDir = f"D:/cv2-resized-image-{scale_percent}.png"
    print('Resized Dimensions : ', resized.shape)
    print("Resized image saved as ",imgDir)
    cv2.imwrite(imgDir, resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=="__main__":
    try:
        scale_percent = int(input("Enter scale percentage :")) # percent of original size
        resizeImage(scale_percent)

    except Exception as e:
        print("Some error occured :",e)