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

3. Run script
```shell
python create_audio.py [--convert_video]
```

Options:
- convert_video:_ convert mp4 video into wav form first
