import numpy as np
from PIL import Image
import os

SIZE = 512

def convert_logo_to_matrix(image_path, output_npy_path=None):
    """
    将校徽图片转换为128x128的0-1矩阵
    
    参数:
    image_path: 输入校徽图片路径
    output_npy_path: 输出.npy文件路径（可选）
    
    返回:
    binary_matrix: 128x128的0-1矩阵
    """
    # 定义红色和白色的RGB值
    RED = np.array([202, 43, 47])
    WHITE = np.array([255, 255, 255])
    
    # 打开图片并转换为RGB模式
    img = Image.open(image_path).convert('RGB')
    
    # 调整大小为128x128
    img_resized = img.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    
    # 转换为numpy数组
    img_array = np.array(img_resized)
    
    # 计算每个像素到红色和白色的欧氏距离（二阶范数）的平方
    # 注意：为了效率，我们计算平方距离，因为平方根是单调递增的
    diff_red = img_array - RED
    diff_white = img_array - WHITE
    
    # 计算平方距离
    dist_red_sq = np.sum(diff_red ** 2, axis=2)
    dist_white_sq = np.sum(diff_white ** 2, axis=2)
    
    # 比较距离：更接近红色记为1，否则记为0
    binary_matrix = (dist_red_sq <= dist_white_sq).astype(np.uint8)
    
    # 如果需要保存为.npy文件
    if output_npy_path:
        np.save(output_npy_path, binary_matrix)
        print(f"矩阵已保存到: {output_npy_path}")
    
    return binary_matrix

def visualize_matrix(matrix, output_image_path=None):
    """
    可视化二值矩阵（可选功能）
    
    参数:
    matrix: 二值矩阵
    output_image_path: 输出图片路径（可选）
    """
    # 将0-1矩阵转换为0-255的灰度图像
    # 为了更直观地查看，我们将1（红色部分）显示为黑色，0（白色背景）显示为白色
    visualization = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
    # 1（红色区域）设为黑色，0（白色背景）设为白色
    visualization[matrix == 1] = [0, 0, 0]      # 黑色
    visualization[matrix == 0] = [255, 255, 255] # 白色
    
    # 转换为PIL图像
    img_vis = Image.fromarray(visualization)
    
    if output_image_path:
        img_vis.save(output_image_path)
        print(f"可视化图片已保存到: {output_image_path}")
    
    return img_vis

def batch_process_logos(input_folder, output_folder):
    """
    批量处理文件夹中的校徽图片
    
    参数:
    input_folder: 输入图片文件夹
    output_folder: 输出文件夹
    """
    os.makedirs(output_folder, exist_ok=True)
    
    # 支持的图片格式
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    
    for filename in os.listdir(input_folder):
        # 检查文件扩展名
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            input_path = os.path.join(input_folder, filename)
            
            # 生成输出文件名
            base_name = os.path.splitext(filename)[0]
            npy_output = os.path.join(output_folder, f"{base_name}_matrix.npy")
            img_output = os.path.join(output_folder, f"{base_name}_visualization.png")
            
            try:
                print(f"处理文件: {filename}")
                # 转换图片为矩阵
                matrix = convert_logo_to_matrix(input_path, npy_output)
                
                # 生成可视化图片
                visualize_matrix(matrix, img_output)
                
                print(f"成功处理: {filename}")
                print(f"  - 矩阵形状: {matrix.shape}")
                print(f"  - 红色像素比例: {np.sum(matrix) / (SIZE*SIZE):.2%}")
                print()
                
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {e}")

# 使用示例
if __name__ == "__main__":
    # 示例1: 处理单个图片
    input_image = "xjtulogo.jpg"  # 替换为你的校徽图片路径
    
    if os.path.exists(input_image):
        # 转换并保存矩阵
        binary_matrix = convert_logo_to_matrix(
            image_path=input_image,
            output_npy_path="logo_matrix.npy"
        )
        
        # 生成可视化图片
        visualize_matrix(binary_matrix, "logo_visualization.png")
        
        # 打印一些统计信息
        print(f"矩阵形状: {binary_matrix.shape}")
        print(f"红色像素数量: {np.sum(binary_matrix)}")
        print(f"白色像素数量: {SIZE*SIZE - np.sum(binary_matrix)}")
        print(f"红色像素比例: {np.sum(binary_matrix) / (SIZE*SIZE):.2%}")
        
        # 显示前几行数据示例
        print("\n矩阵前10行前10列示例:")
        for i in range(min(10, binary_matrix.shape[0])):
            print(' '.join(str(binary_matrix[i, j]) for j in range(min(10, binary_matrix.shape[1]))))
    else:
        print(f"文件 {input_image} 不存在，请替换为你的校徽图片路径")
    
    # 示例2: 批量处理（如果需要）
    # batch_process_logos("input_logos", "output_matrices")