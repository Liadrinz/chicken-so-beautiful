# -*- coding: utf-8 -*-

import os
import sys
import cv2
import json
import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='输入视频路径', required=True)
parser.add_argument('-o', '--output', help='输出视频路径')
parser.add_argument('-d', '--demo', help='是否预览视频')
parser.add_argument('-c', '--color', help='指定颜色, 若为彩色')
args = parser.parse_args()

# 检查格式
if args.output is not None:
    if '/' in args.output or '\\' in args.output:
        if not os.path.exists('/'.join(args.output.split('/')[:-1])) and not os.path.exists('/'.join(args.output.split('\\')[:-1])):
            print('Invalid path!')
            exit(-1)
    format = args.output.split('.')[-1]
    if format != 'avi':
        args.output += '.avi'

# 进度
def progress(percent, width=50, prompt=''):
    if percent > 1:
        percent = 1
    show_str=('[%%-%ds]' %width) % (int(percent*width) * '#')
    print('\r%s %s %s%%' % (prompt, show_str, int(percent * 100)), end='', file=sys.stdout, flush=True)

def get_all_frames():
    frames = []
    capture = cv2.VideoCapture(args.input)
    frames_count = capture.get(7)
    fps = capture.get(cv2.CAP_PROP_FPS)
    idx = 0
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame = cv2.Canny(frame, 100, 100)
        frames.append(frame)
        progress((idx + 1) / frames_count, prompt='读取视频中...')
        idx += 1
    capture.release()
    return frames, fps

def gather(frame):
    points = np.argwhere(frame == 255)
    return points

def save_pic(drop_frame=0.1):
    all_frames, fps = get_all_frames()
    first_frame = all_frames[0]
    plt.figure(figsize=(first_frame.shape[1] / 30, first_frame.shape[0] / 30))
    lfs = len(all_frames)
    new_frame_files = []
    fname = ''
    prev_frame = None
    for i in range(lfs):
        frame = all_frames[i]
        if prev_frame is None or np.sum(np.abs(prev_frame - frame)) / (frame.shape[0] * frame.shape[1]) > drop_frame or fname == '':
            try:
                x, y = gather(frame).T
                plt.scatter(y, -x)
                fname = 'temp/temp%d.png' % i
                new_frame_files.append(fname)
                plt.savefig(fname)
                plt.cla()
                progress((i + 1) / lfs, prompt='捕捉帧并转换图像中...')
                prev_frame = np.array(frame)
            except Exception as e:
                print(e)
        else:
            new_frame_files.append(fname)
    return new_frame_files, fps

def make_video(images, outimg=None, fps=2, size=None, is_color=True, format="XVID", outvid=args.output):
    fourcc = cv2.VideoWriter_fourcc(*format)
    vid = None
    idx = 0
    for image in images:
        if not os.path.exists(image):
            raise FileNotFoundError(image)
        img = cv2.imread(image)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = cv2.VideoWriter(outvid, fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = cv2.resize(img, size)
        vid.write(img)
        progress((idx + 1) / len(images), prompt='拼接视频中...')
        idx += 1
    vid.release()
    
    idx = 0
    # 删除临时图片
    for image in images:
        os.remove(image)
        progress((idx + 1) / len(images), prompt='删除临时图片...')
        idx += 1

    return vid

def show():
    plt.ion()
    plt.show()
    for frame in get_all_frames()[0]:
        x, y = gather(frame).T
        plt.scatter(y, -x, c=x)
        plt.pause(0.001)
        plt.cla()

if __name__ == '__main__':
    if args.demo is not None:
        show()
    elif args.output is not None:
        images, fps = save_pic()
        make_video(images, fps=fps)
        progress(1, prompt='完成!')
