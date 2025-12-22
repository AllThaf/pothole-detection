from ultralytics import YOLO, solutions
import cv2

WIDTH = 640
HEIGHT = 640

VID_SOURCE = "sample/vid/pothole1.mp4"


def count_resize() -> dict:
    cap = cv2.VideoCapture(VID_SOURCE)
    assert cap.isOpened(), "Cannot open video source"

    region_points = [
        (10, HEIGHT - 100),
        (WIDTH - 10, HEIGHT - 100),
        (WIDTH - 10, HEIGHT - 50),
        (10, HEIGHT - 50),
    ]

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    video_writer = cv2.VideoWriter(
        "result.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (WIDTH, HEIGHT)
    )

    counter = solutions.ObjectCounter(show=True, region=region_points, model="best.pt")

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

    return results.classwise_count


def count() -> dict:
    cap = cv2.VideoCapture(VID_SOURCE)
    assert cap.isOpened(), "Cannot open video source"

    w, h, fps = (
        int(cap.get(x))
        for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS)
    )

    region_points = [(10, h - 200), (w - 10, h - 200), (w - 10, h - 50), (10, h - 50)]

    video_writer = cv2.VideoWriter(
        "result.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h)
    )

    counter = solutions.ObjectCounter(show=True, region=region_points, model="best.pt")

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

    return results.classwise_count


def analyze(count_info: dict) -> None:
    pass


if __name__ == "__main__":
    # result = count()
    analyze({"Lubang": {"in": 31, "out": 0}})
