import os
from PIL import Image


def create_gif_with_fixed_size(folder_path, output_gif_name="optimized.gif", max_size_mb=5, duration_time=10,target_size=(1080, 960)):
    # 获取文件夹中的图片文件
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.png'))]
    files.sort()  # 按文件名排序
    images = []
    for file in files:
        img_path = os.path.join(folder_path, file)
        img = Image.open(img_path)
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        images.append(img.convert("P", palette=Image.Palette.ADAPTIVE, colors=64))  # 减少颜色数量
    output_path = os.path.join(folder_path, output_gif_name)
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=duration_time,
        loop=0,
        optimize=True
    )
    print(f"GIF 已保存到：{output_path}")
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"当前文件大小：{file_size_mb:.2f} MB")

# 使用示例
current_folder = "."  # 当前文件夹路径
create_gif_with_fixed_size(current_folder, output_gif_name="optimized2.gif", max_size_mb=5, duration_time=40,target_size=(400, 400))
