import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import cv2
import numpy as np
from ultralytics import YOLO


class PotholeDetector:
    """
    Pothole detection system with JSON export for web display
    """

    def __init__(self, model_path: str = "best.pt"):
        """Initialize detector with trained model"""
        print(f"Loading model from {model_path}...")
        self.model = YOLO(model_path)
        print("Model loaded successfully!")

    def process_video(
        self,
        video_path: str,
        street_name: str,
        direction: str,
        city: str = "Bandung",
        show_progress: bool = True,
    ) -> Dict:
        """
        Process video and detect potholes

        Args:
            video_path: Path to video file
            street_name: e.g., "Jl. Ir. H. Juanda"
            direction: e.g., "Dago Utara - Dago Selatan"
            city: City name (default: "Bandung")
            show_progress: Show processing progress

        Returns:
            Dictionary with detection results
        """
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")

        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = total_frames / fps if fps > 0 else 0

        print(f"\nVideo Info:")
        print(f"   Duration: {duration:.1f} seconds")
        print(f"   FPS: {fps:.1f}")
        print(f"   Resolution: {width}x{height}")
        print(f"   Total frames: {total_frames}")
        print(f"\nProcessing video...")

        potholes = []
        seen_potholes = []  # For deduplication
        frame_idx = 0
        process_every = 10  # Process every Nth frame to speed up

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Process every Nth frame to speed up and avoid duplicates
            if frame_idx % process_every == 0:
                results = self.model(frame, verbose=False)

                for result in results:
                    boxes = result.boxes

                    if boxes is not None and len(boxes) > 0:
                        for box in boxes:
                            conf = float(box.conf[0])

                            # Only consider high confidence detections
                            if conf > 0.5:
                                x1, y1, x2, y2 = box.xyxy[0].tolist()
                                center_x = (x1 + x2) / 2
                                center_y = (y1 + y2) / 2
                                width_box = x2 - x1
                                height_box = y2 - y1
                                area = width_box * height_box

                                # Deduplication: check if similar pothole already detected
                                is_duplicate = False
                                for existing in seen_potholes:
                                    # Calculate distance between centers
                                    dist = np.sqrt(
                                        (existing["cx"] - center_x) ** 2
                                        + (existing["cy"] - center_y) ** 2
                                    )
                                    # If within 100 pixels, consider it the same pothole
                                    if dist < 100:
                                        is_duplicate = True
                                        break

                                if not is_duplicate:
                                    pothole = {
                                        "id": len(potholes) + 1,
                                        "timestamp": round(frame_idx / fps, 2),
                                        "frame": frame_idx,
                                        "confidence": round(conf, 3),
                                        "area": int(area),
                                        "severity": self._classify_severity(area),
                                    }
                                    potholes.append(pothole)
                                    seen_potholes.append(
                                        {"cx": center_x, "cy": center_y}
                                    )

            frame_idx += 1

            # Progress indicator
            if show_progress and frame_idx % 100 == 0:
                progress = (frame_idx / total_frames) * 100
                print(
                    f"   Progress: {progress:.1f}% - Found {len(potholes)} potholes",
                    end="\r",
                )

        cap.release()

        if show_progress:
            print(f"\n   Progress: 100.0% - Found {len(potholes)} potholes")

        # Calculate statistics
        severity_stats = {
            "kecil": sum(1 for p in potholes if p["severity"] == "kecil"),
            "sedang": sum(1 for p in potholes if p["severity"] == "sedang"),
            "besar": sum(1 for p in potholes if p["severity"] == "besar"),
        }

        # Prepare output data
        result = {
            "jalan": street_name,
            "arah": direction,
            "kota": city,
            "tanggal": datetime.now().strftime("%Y-%m-%d"),
            "waktu": datetime.now().strftime("%H:%M:%S"),
            "total_lubang": len(potholes),
            "durasi_video": round(duration, 1),
            "lubang_per_menit": round(len(potholes) / (duration / 60), 2)
            if duration > 0
            else 0,
            "detail_lubang": potholes,
            "statistik": severity_stats,
        }

        return result

    def _classify_severity(self, area: float) -> str:
        """
        Classify pothole severity based on bounding box area

        Args:
            area: Bounding box area in pixels

        Returns:
            Severity level: 'kecil', 'sedang', or 'besar'
        """
        if area < 5000:
            return "kecil"
        elif area < 15000:
            return "sedang"
        else:
            return "besar"


def save_results(result: Dict, output_file: str = "data/detections.json"):
    """
    Save detection results to JSON file

    Args:
        result: Detection results dictionary
        output_file: Path to output JSON file
    """
    # Create data directory if it doesn't exist
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    # Load existing data or create new list
    if Path(output_file).exists():
        with open(output_file, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                print("Warning: Existing JSON file is corrupted, creating new one")
                all_data = []
    else:
        all_data = []

    # Append new result
    all_data.append(result)

    # Save to file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"\nData saved to {output_file}")


def print_summary(result: Dict):
    """Print detection summary to console"""
    print(f"\n{'=' * 60}")
    print(f"SUMMARY")
    print(f"{'=' * 60}")
    print(f"Jalan       : {result['jalan']}")
    print(f"Arah        : {result['arah']}")
    print(f"Tanggal     : {result['tanggal']} {result['waktu']}")
    print(f"Total Lubang: {result['total_lubang']}")
    print(f"Durasi Video: {result['durasi_video']} detik")
    print(f"Lubang/Menit: {result['lubang_per_menit']}")
    print(f"\nKlasifikasi:")
    print(f"  Kecil  : {result['statistik']['kecil']}")
    print(f"  Sedang : {result['statistik']['sedang']}")
    print(f"  Besar  : {result['statistik']['besar']}")
    print(f"{'=' * 60}\n")


def interactive_mode():
    """Interactive mode for processing videos"""
    print("\n" + "=" * 60)
    print("POTHOLE DETECTION SYSTEM - INTERACTIVE MODE")
    print("=" * 60 + "\n")

    # Initialize detector
    try:
        detector = PotholeDetector("best.pt")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Get user input
    print("\nInput Information:")
    print("-" * 60)

    video_path = input("Video path (e.g., sample/vid/pothole1.mp4): ").strip()
    if not video_path:
        print("Video path cannot be empty!")
        return

    if not Path(video_path).exists():
        print(f"Video file not found: {video_path}")
        return

    street_name = input("Nama jalan (e.g., Jl. Ir. H. Juanda): ").strip()
    if not street_name:
        print("Street name cannot be empty!")
        return

    direction = input("Arah perekaman (e.g., Dago Utara - Dago Selatan): ").strip()
    if not direction:
        print("Direction cannot be empty!")
        return

    city = input("Kota (default: Bandung): ").strip() or "Bandung"

    # Process video
    try:
        result = detector.process_video(
            video_path=video_path,
            street_name=street_name,
            direction=direction,
            city=city,
            show_progress=True,
        )

        # Print summary
        print_summary(result)

        # Save results
        save_results(result)

        # Also save to web folder if it exists
        web_data_path = "web/data/detections.json"
        if Path("web").exists():
            save_results(result, web_data_path)
            print(f"Data also saved to {web_data_path}")

        print("Processing complete!")

    except Exception as e:
        print(f"\nError during processing: {e}")
        import traceback

        traceback.print_exc()


def batch_mode():
    """Batch processing mode for multiple videos"""
    print("\n" + "=" * 60)
    print("POTHOLE DETECTION SYSTEM - BATCH MODE")
    print("=" * 60 + "\n")

    # Example batch configuration
    # You can modify this list for your needs
    videos_to_process = [
        {
            "video_path": "sample/vid/pothole1.mp4",
            "street_name": "Jl. Ir. H. Juanda",
            "direction": "Dago Utara - Dago Selatan",
            "city": "Bandung",
        },
        # Add more videos here
        # {
        #     'video_path': 'sample/vid/pothole2.mp4',
        #     'street_name': 'Jl. Soekarno-Hatta',
        #     'direction': 'Timur - Barat',
        #     'city': 'Bandung'
        # },
    ]

    detector = PotholeDetector("best.pt")

    for idx, video_config in enumerate(videos_to_process, 1):
        print(
            f"\n[{idx}/{len(videos_to_process)}] Processing: {video_config['street_name']}"
        )

        try:
            result = detector.process_video(**video_config)
            print_summary(result)
            save_results(result)

        except Exception as e:
            print(f"Error processing {video_config['video_path']}: {e}")
            continue

    print("\nBatch processing complete!")


def main():
    """Main entry point"""
    print("\n" + "=" * 60)
    print("POTHOLE DETECTION SYSTEM")
    print("    Politeknik Negeri Bandung - PCD Semester 5")
    print("=" * 60 + "\n")

    print("Select mode:")
    print("1. Interactive mode (process one video)")
    print("2. Batch mode (process multiple videos)")
    print("3. Exit")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice == "1":
        interactive_mode()
    elif choice == "2":
        batch_mode()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
