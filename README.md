# AI Hub Dialogue Speech
Speech Dataset generator from [AI Hub](https://aihub.or.kr) multimodal video dataset

## Dataset Download
Request dataset from [AI Hub Multimodal Video](https://aihub.or.kr/aidata/137).

## Convert to Speech Dataset
1. Place video dataset with following structure:
```
data
└── 0001-0400
    ├── clip_1
    │   ├── clip_1.json
    │   └── clip_1.mp4
    └── clip_2
        ├── clip_2.json
        └── clip_2.mp4
```

2. Install requirements

Requirements:

- moviepy==1.0.3
- librosa==0.8.0

3. Create audio file
```shell
python create_audio.py [--convert_video] [--sample_rate SR]
```

Option:
- convert_video: convert mp4 video into wav form first
- sample_rate: sampling rate (default: 22050)

4. Split train/dev/test set
```shell
python split.py [--path FILELIST_PATH] [--ratio RATIO] [--seed SEED]
```

Option:
- path: path of filelist. train/dev/test filelists are created in same directory.
- ratio: train_ratio:dev_ratio:test_ratio. Three ratios must be splitted with ':'
- seed: random seed for shuffling
