from ultralytics import YOLO
import cv2

HEIGHT = 640
WIDTH = 640


def main() -> None:
    model = YOLO("runs/detect/train/weights/best.pt")
    result = model("sample/pict/")

    for r in result:
        r.show()

    # img = result[0].plot()

    # resized_img = cv2.resize(img, (WIDTH, HEIGHT))

    # cv2.imshow("Pothole Detection", resized_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
