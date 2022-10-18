from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from glob import glob
from tqdm import tqdm
import os, shutil


def read_video(vid_path):
    return VideoFileClip(vid_path)

def read_wav(wav_path):
    return AudioFileClip(wav_path)

def replace_audio(video, audio):
    new_audio = CompositeAudioClip([audio])
    video.audio = new_audio
    video_new_audio = video.set_audio(audio)
    return video_new_audio

def mkdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def write_video(video, out_path):
    video.write_videofile(out_path, video.fps, codec="mpeg4")

# Read the WAV Audio from the folder
wav_path = "ckpt/dog/inference_result"
wav_files = glob(os.path.join(wav_path, "*.wav"))

# Read the Videos from the other folder
video_path = "data/VAS/dog/videos"
video_files = glob(os.path.join(video_path, "*.mp4"))

# Create a directory for inference results with one directory for original and one generated audio
output_original_path = "data/VAS/dog/inference/original"
output_generated_path = "data/VAS/dog/inference/generated"
mkdir(output_original_path)
mkdir(output_generated_path)

# Copy the original videos to the original folder based on the audio
wav_filenames = [os.path.basename(wav_file) for wav_file in wav_files]
filtered_filenames = sorted([filename.replace(".wav", "") for filename in wav_filenames]) # video_001.wav --> video_001


# filtered_video_files = [filename for filename in video_files if filename in filtered_filenames] # Get the files which are relevant
for filtered_filename in tqdm(filtered_filenames):
    src = os.path.join(video_path, filtered_filename+".mp4")
    dst = os.path.join(output_original_path, filtered_filename+".mp4")
    try:
        shutil.copy(src, dst)
    except Exception as e:
        print(f"Error: {e}")

# Put the replaced audio in the generated folder
for filtered_filename in tqdm(filtered_filenames):
    src_a = os.path.join(wav_path, filtered_filename+".wav")
    src_v = os.path.join(video_path, filtered_filename+".mp4")
    dst = os.path.join(output_generated_path, filtered_filename+".mp4")
    try:
        video = read_video(src_v)
        audio = read_wav(src_a)
        replaced_video = replace_audio(video, audio)
        write_video(replaced_video, dst)
    except Exception as e:
        print(f"Error: {e}")
