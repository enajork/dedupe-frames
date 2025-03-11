import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def is_similar_to_any(frame, saved_frames, threshold=0.99):
    """Check if the given frame is similar to any of the saved frames."""
    gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for i, saved_frame in enumerate(saved_frames):
        gray2 = cv2.cvtColor(saved_frame, cv2.COLOR_BGR2GRAY)
        similarity, _ = ssim(gray1, gray2, full=True)
        if similarity >= threshold:
            print(f"Frame skipped (similar to frame {i}) | Similarity: {similarity:.4f}")
            return True  # Frame is too similar to an existing one

    return False  # Frame is unique

def remove_duplicate_frames(input_video, output_video, similarity_threshold=0.99):
    """
    Remove duplicate frames across the whole .mov video.

    Args:
        input_video (str): Path to input .mov file.
        output_video (str): Path to output .mov file.
        similarity_threshold (float): SSIM threshold for frame similarity.
    """
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Processing video: {input_video}")
    print(f"Resolution: {width}x{height}, FPS: {fps}, Total Frames: {total_frames}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Change codec if needed
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    saved_frames = []  # Store unique frames
    frame_count = 0
    unique_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        frame_count += 1
        print(f"Processing frame {frame_count}/{total_frames}... ", end="")

        if not is_similar_to_any(frame, saved_frames, similarity_threshold):
            saved_frames.append(frame)
            out.write(frame)
            unique_count += 1
            print(f"Saved as unique frame {unique_count}.")
        else:
            print("Skipped.")

    cap.release()
    out.release()
    print(f"\nProcessing complete. Unique frames saved: {unique_count}/{total_frames}")
    print(f"Processed video saved as {output_video}")

# Example usage
input_file = "timelapse.mov"
output_file = "output.mov"
remove_duplicate_frames(input_file, output_file)
