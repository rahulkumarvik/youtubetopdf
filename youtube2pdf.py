import cv2
import os
import img2pdf
from pytube import YouTube

def download_and_capture_frames(video_url, interval_seconds):
    # Create a YouTube object
    yt = YouTube(video_url)

    # Get video details
    video_id = yt.video_id
    video_q="360p"
    # Create a VideoCapture object
    video_url = yt.streams.filter(file_extension="mp4", res=video_q).first().url
    cap = cv2.VideoCapture(video_url)

    # Create a directory to store frames on your desktop
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    frames_dir = os.path.join(desktop_path, f"{video_id}_frames")
    os.makedirs(frames_dir, exist_ok=True)

    frame_count = 0

    while cap.isOpened():
        # Read the frame
        ret, frame = cap.read()

        if not ret:
            break

        # Capture frame at the specified interval
        if frame_count % (interval_seconds * int(cap.get(cv2.CAP_PROP_FPS))) == 0:
            # Save the frame
            frame_path = os.path.join(frames_dir, f"{video_id}_frame_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            print(f"Captured frame {frame_count} at {frame_count // int(cap.get(cv2.CAP_PROP_FPS))} seconds")

        frame_count += 1

    # Release the VideoCapture and close the video file
    cap.release()
    cv2.destroyAllWindows()

    # After capturing the frames, convert them to a single PDF
    jpg_files = [f for f in os.listdir(frames_dir) if f.endswith(".jpg")]
    jpg_files.sort(key=lambda x: int(x[len(video_id) + 7:-4]))  # Sort files based on frame count

    pdf_bytes = img2pdf.convert([os.path.join(frames_dir, jpg_file).encode('utf-8') for jpg_file in jpg_files])

    with open(f"{frames_dir}/output.pdf", "wb") as f:
        f.write(pdf_bytes)

    return f"{frames_dir}/output.pdf"

if __name__ == "__main__":
    try:
        video_url = input("Enter YouTube video URL: ")
        interval_seconds = int(input("Enter interval in seconds:"))

        pdf_path = download_and_capture_frames(video_url, interval_seconds)
        print(f"Your frames have been captured and saved as a PDF: {pdf_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
