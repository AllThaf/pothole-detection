from ultralytics import YOLO


def train() -> None:
    model = YOLO("pretrained-model/yolov8n.pt")
    model.train(
        data="dataset/data.yaml", epochs=100, imgsz=640, workers=1, device="cuda"
    )


if __name__ == "__main__":
    train()
