import os
import cv2


def extract_frames_from_video(video_path, output_folder):
    """
    从视频中提取每一帧并保存为图片。

    参数:
        video_path (str): 视频文件的路径。
        output_folder (str): 保存图片的文件夹路径。
    """
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"无法打开视频文件：{video_path}")
        return

    frame_count = 0  # 帧计数器

    while True:
        ret, frame = cap.read()  # 读取一帧
        if not ret:
            break  # 如果读取失败，退出循环

        # 构造图片文件名
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")

        # 保存图片
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    # 释放视频文件
    cap.release()
    print(f"视频 {video_path} 提取完成，共提取 {frame_count} 帧。")


def process_videos_in_folder(input_folder):
    """
    遍历文件夹中的视频文件，并为每个视频创建一个文件夹来保存帧。

    参数:
        input_folder (str): 包含视频文件的文件夹路径。
    """
    # 遍历文件夹中的所有文件
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        # 检查是否为视频文件（通过扩展名）
        if os.path.isfile(file_path) and filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            # 创建以视频文件名命名的文件夹
            video_name = os.path.splitext(filename)[0]  # 去掉扩展名
            output_folder = os.path.join(input_folder, video_name)

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            print(f"处理视频：{filename}，帧将保存到：{output_folder}")
            extract_frames_from_video(file_path, output_folder)


# 使用示例
input_folder = "./"  # 替换为包含视频文件的文件夹路径
process_videos_in_folder(input_folder)
