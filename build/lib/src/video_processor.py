import cv2
import numpy as np
import os

from .xml_parser import parse_xml

def process_video_with_annotations(xml_file_path, video_path, output_dir):
    rois_info = parse_xml(xml_file_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Unable to open video file")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for label, roi_info in rois_info.items():
        output_video_name = f'{label}.mp4'
        output_video_path = os.path.join(output_dir, output_video_name)

        max_width = max_height = 0
        for roi_data in roi_info:
            width = roi_data["xbr"] - roi_data["xtl"]
            height = roi_data["ybr"] - roi_data["ytl"]
            max_width = max(max_width, width)
            max_height = max(max_height, height)

        frame_size = max(max_width, max_height)
        black_frame_size = max(800, frame_size + 100)

        out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (int(black_frame_size), int(black_frame_size)))

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            roi_info_frame = next((item for item in roi_info if item["frame"] == frame_count), None)
            if roi_info_frame:
                roi = frame[int(roi_info_frame["ytl"]):int(roi_info_frame["ybr"]),
                            int(roi_info_frame["xtl"]):int(roi_info_frame["xbr"])]

                black_frame_size = max(800, frame_size + 100)
                black_frame_size = int(black_frame_size)

                black_frame = np.zeros((black_frame_size, black_frame_size, 3), np.uint8)

                start_y = (black_frame_size - roi.shape[0]) // 2
                start_x = (black_frame_size - roi.shape[1]) // 2

                black_frame[start_y:start_y + roi.shape[0], start_x:start_x + roi.shape[1]] = roi

                out.write(black_frame)

            frame_count += 1

        out.release()

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    cap.release()

def main():
    root_path = input("Enter the root path should contain annotation XML file and video: ")

    xml_file_path = os.path.join(root_path,'annotations.xml')

    video_path = None
    for file in os.listdir(root_path):
        if file.lower().endswith((".mov", ".mp4")):
            video_path = os.path.join(root_path, file)
            break

    if video_path is None:
        print("Error: No video file found in the directory")
        return

    output_dir = root_path

    process_video_with_annotations(xml_file_path, video_path, output_dir)

if __name__ == "__main__":
    main()
