# Chicken-So-Beautiful

## 用法

- 在matplotlib画布中预览而不输出视频

```cmd
python jntm.py -i <输入视频路径> -d <任意字符串>
```

- 输出视频到指定路径

```cmd
python jntm.py -i <输入视频路径> -o <输出路径>
```

## 鸡你太美示例

- 生成jntm.avi
```cmd
python jntm.py -i cxk.mp4 -o jntm.avi
```

- 在matplotlib画布预览
```cmd
python jntm.py -i cxk.mp4 -d 1
```

## 注意

- 只能生成.avi格式的视频
- 生成的视频没有音频
- 生成视频的帧率、帧数与原视频相同, 故可自行剪辑加上音频
