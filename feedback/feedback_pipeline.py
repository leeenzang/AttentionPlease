from .video_processing import VideoProcessor

def process_feedback(video_path, output_path):
    processor = VideoProcessor(source=video_path, save_out=output_path)
    results = processor.process_video()
    return results 