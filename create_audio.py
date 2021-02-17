import os
import shutil
import json
import librosa
import soundfile
from glob import glob
from moviepy.editor import VideoFileClip

def create_audio():
    video_files = glob('data/**/*.mp4', recursive=True)
    # Create Audio files
    for video_path in video_files:
        audio_path = video_path.replace('data', 'raw_audio', 1).replace('mp4', 'wav')
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)

        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path)
        clip.close()

    if os.path.exists('speech_dataset'):
        shutil.rmtree('speech_dataset')
    os.makedirs('speech_dataset/wavs')
    filelist = open('./speech_dataset/filelist.txt', 'w', encoding='utf-8')
    total_duration = 0

    for video_path in video_files:
        # Load annotation file
        file_name = os.path.splitext(os.path.basename(video_path))[0]
        json_path = video_path.replace('mp4', 'json')
        with open(json_path, 'r', encoding='utf-8') as f:
            annotation = json.load(f)

        # Load video clip
        audio_path = video_path.replace('data', 'raw_audio', 1).replace('mp4', 'wav')
        y, sr = librosa.load(audio_path, sr=44100)
        duration = librosa.get_duration(y, sr=sr)

        # Metadata
        n_frames = float(annotation['nr_frame'])
        fps = n_frames / duration

        for frame, frame_data in annotation['data'].items():
            for sub_id, info_data in frame_data.items():
                if 'text' not in info_data.keys():
                    continue

                # Extract data
                text_data = info_data['text']
                speaker_id = info_data['person_id']
                start_frame = text_data['script_start']
                end_frame = text_data['script_end']
                script = text_data['script']

                start_idx = int(float(start_frame) / fps * sr)
                end_idx = int(float(end_frame) / fps * sr)

                # Write wav
                y_part = y[start_idx:end_idx]
                wav_path = f'./speech_dataset/wavs/{file_name}_{speaker_id}_{start_frame}_{end_frame}.wav'
                if not os.path.exists(wav_path):
                    soundfile.write(wav_path, y_part, sr)

                    # Write filelist
                    filelist.write(f'{wav_path}|{script}|{speaker_id}\n')
                    total_duration += (end_idx - start_idx) / float(sr)

    filelist.close()
    print(f'End parsing, total duration: {total_duration}')

if __name__ == '__main__':
    create_audio()
