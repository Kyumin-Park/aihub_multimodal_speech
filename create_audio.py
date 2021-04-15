import argparse
import os
import shutil
import json
import librosa
import soundfile
from glob import glob
from moviepy.editor import VideoFileClip

def create_dataset(sample_rate, input_dir, tmp_dir, output_dir):
    video_files = glob(f'{input_dir}/**/*.mp4', recursive=True)

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(f'{output_dir}/wavs')
    filelist = open(f'{output_dir}/filelist.txt', 'w', encoding='utf-8')
    total_duration = 0

    for video_path in video_files:
        # Load annotation file
        file_name = os.path.splitext(os.path.basename(video_path))[0]
        json_path = video_path.replace('mp4', 'json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                annotation = json.load(f)
        except UnicodeDecodeError:
            continue

        # Load video clip
        audio_path = video_path.replace(input_dir, tmp_dir, 1).replace('mp4', 'wav')
        orig_sr = librosa.get_samplerate(audio_path)
        y, sr = librosa.load(audio_path, sr=orig_sr)
        duration = librosa.get_duration(y, sr=sr)
        new_sr = sample_rate
        new_y = librosa.resample(y, sr, new_sr)

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
                script = refine_text(text_data['script'])

                start_idx = int(float(start_frame) / fps * new_sr)
                end_idx = int(float(end_frame) / fps * new_sr)

                # Write wav
                y_part = new_y[start_idx:end_idx]
                wav_path = os.path.join(os.path.dirname(audio_path).replace(tmp_dir, f'{output_dir}/wavs'),
                                        f'{file_name}_{speaker_id}_{start_frame}_{end_frame}.wav')
                wav_path_text = f'/path_to_speech_dataset/wavs/{file_name}_{speaker_id}_{start_frame}_{end_frame}.wav'
                if not os.path.exists(wav_path):
                    os.makedirs(os.path.dirname(wav_path), exist_ok=True)
                    soundfile.write(wav_path, y_part, new_sr)

                    # Write filelist
                    filelist.write(f'{wav_path_text}|{script}|{speaker_id}\n')
                    total_duration += (end_idx - start_idx) / float(new_sr)

    filelist.close()
    print(f'End parsing, total duration: {total_duration}')

def refine_text(text):
    # Fix invalid characters in text
    text = text.replace('…', ',')
    text = text.replace('\t', '')
    text = text.replace('-', ',')
    text = text.replace('–', ',')
    return text

def extract_audio(input_dir, output_dir):
    video_files = glob(f'{input_dir}/**/*.mp4', recursive=True)
    # Create Audio files
    for video_path in video_files:
        audio_path = video_path.replace(input_dir, output_dir, 1).replace('mp4', 'wav')
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)

        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path, verbose=False)
        clip.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--convert_video', help='convert video into .wav file', action='store_true')
    parser.add_argument('--sample_rate', help='wav file sampling rate', type=int, default=22050)
    parser.add_argument('--input_dir', help='input directory', type=str)
    parser.add_argument('--tmp_dir', help='temporary directory', type=str)
    parser.add_argument('--output_dir', help='output directory', type=str)

    args = parser.parse_args()

    if args.convert_video:
        extract_audio(args.input_dir, args.tmp_dir)
    create_dataset(args.sample_rate, args.input_dir, args.tmp_dir, args.output_dir)
