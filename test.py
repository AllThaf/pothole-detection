from ultralytics import YOLO
import cv2

HEIGHT = 640
WIDTH = 640

VID_SOURCE = "sample/vid/pothole1.mp4"


def main() -> None:
    model = YOLO("yolov8n.pt")

    cap = cv2.VideoCapture(VID_SOURCE)

    if not cap.isOpened():
        print("Error: Cannot open video stream")
        return

    print("Streaming... Press 'q' to quit")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Cannot read frame")
            break

        results = model(frame, verbose=False)

        annotated_frame = results[0].plot()

        resized_frame = cv2.resize(annotated_frame, (WIDTH, HEIGHT))

        cv2.imshow("Tes stream", resized_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def testing() -> None:
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
    testing()
