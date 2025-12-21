from ultralytics import YOLO, solutions
import cv2

WIDTH = 640
HEIGHT = 640

VID_SOURCE = "sample/vid/pothole3.mp4"
# VID_SOURCE = "car2.mp4"


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


def counting_resize() -> None:
    cap = cv2.VideoCapture(VID_SOURCE)
    assert cap.isOpened(), "Cannot open video source"

    region_points = [(100, 300), (WIDTH - 100, 300)]

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    video_writer = cv2.VideoWriter(
        "result.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (WIDTH, HEIGHT)
    )

    counter = solutions.ObjectCounter(
        show=True, region=region_points, model="runs/detect/train/weights/best.pt"
    )

    while cap.isOpened():
        succes, im0 = cap.read()
        if not succes:
            print(results.classwise_count)
            print("End of video stream or cannot fetch the frame.")
            break

        # Resize frame sebelum diproses
        resized_im0 = cv2.resize(im0, (WIDTH, HEIGHT))
        results = counter(resized_im0)

        video_writer.write(results.plot_im)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print(results.classwise_count)
            break

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()


def counting() -> None:
    cap = cv2.VideoCapture(VID_SOURCE)
    assert cap.isOpened(), "Cannot open video source"

    region_points = [(100, 300), (100, 300)]

    w, h, fps = (
        int(cap.get(x))
        for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS)
    )
    video_writer = cv2.VideoWriter(
        "result.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h)
    )

    counter = solutions.ObjectCounter(
        show=True, region=region_points, model="runs/detect/train/weights/best.pt"
    )

    while cap.isOpened():
        succes, im0 = cap.read()
        if not succes:
            print(results.classwise_count)
            print("End of video stream or cannot fetch the frame.")
            break

        results = counter(im0)

        video_writer.write(results.plot_im)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print(results.classwise_count)
            break

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    counting_resize()
