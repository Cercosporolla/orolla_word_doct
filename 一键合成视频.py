import os
import subprocess
from natsort import natsorted

def get_video_files(folder_path):
    """
    获取指定文件夹下所有 .mov 和 .mp4 格式的视频文件，并按自然顺序排序
    """
    supported_formats = (".mov", ".mp4")
    video_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path)
                   if file.lower().endswith(supported_formats)]
    # 使用 natsort 按自然顺序排序
    video_files = natsorted(video_files)
    return video_files

def check_ffmpeg(ffmpeg_path=None):
    """
    检查 ffmpeg 是否可用，如果未指定路径，则尝试使用默认路径
    """
    if ffmpeg_path:
        return ffmpeg_path  # 使用用户指定的路径

    # 尝试使用默认路径
    default_paths = [
        r"D:\ffmpeg\bin\ffmpeg.exe",  # 用户自定义安装路径
        "ffmpeg"  # 环境变量中配置的路径
    ]

    for path in default_paths:
        try:
            subprocess.run([path, "-version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"找到 ffmpeg: {path}")
            return path
        except FileNotFoundError:
            continue

    raise FileNotFoundError("未找到 ffmpeg，请确保已正确安装并配置路径。")

def merge_videos_with_ffmpeg(video_files, output_file, ffmpeg_path):
    """
    使用 ffmpeg 合成视频
    """
    # 创建一个临时文件来存储视频文件列表
    with open("video_list.txt", "w", encoding="utf-8") as f:
        for file in video_files:
            # 使用正斜杠替换路径中的反斜杠
            file_path = file.replace("\\", "/")
            f.write(f"file '{file_path}'\n")

    # 调用 ffmpeg 合成视频
    command = [
        ffmpeg_path,
        "-f", "concat",
        "-safe", "0",
        "-i", "video_list.txt",
        "-c", "copy",
        output_file
    ]
    try:
        subprocess.run(command, check=True)
        print(f"视频合成完成，已保存为 {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"合成视频时出错：{e}")
    finally:
        os.remove("video_list.txt")  # 删除临时文件

if __name__ == "__main__":
    current_folder = os.getcwd()
    print(f"当前文件夹路径：{current_folder}")

    # 获取当前文件夹下的所有视频文件
    video_files = get_video_files(current_folder)

    if not video_files:
        print("当前文件夹下没有找到 .mp4 或 .mov 格式的视频文件。")
    else:
        print("\n找到以下视频文件，将按以下顺序合成：")
        for idx, file in enumerate(video_files, start=1):
            print(f"{idx}. {os.path.basename(file)}")

        user_input = input("\n是否继续合成？(y/n): ").strip().lower()
        if user_input == "y":
            # 检查 ffmpeg 是否可用
            ffmpeg_path = check_ffmpeg()

            # 合成视频
            output_file = os.path.join(current_folder, "merged_video.mp4")
            merge_videos_with_ffmpeg(video_files, output_file, ffmpeg_path)
        else:
            print("操作已取消。")
