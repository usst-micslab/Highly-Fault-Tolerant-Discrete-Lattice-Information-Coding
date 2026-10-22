import cv2
import numpy as np


def apply_perspective_shape_change(image_path, points_src):
    """
    Apply a perspective transformation to change the shape of an image,
    making it look as if viewed from an angle.

    Parameters:
        image_path (str): The path to the image file.
        points_src (list of list of int): Source points for the transformation.

    Returns:
        The transformed image.
    """
    # 读取图像
    image = cv2.imread(image_path)
    h, w = image.shape[:2]

    # 定义目标点，以模拟从角度看图像的效果
    points_dst = [
        [w * 0.1, 0.09 * h],  # 左上角
        [w * 0.9, h * 0.2],  # 右上角
        [w * 0.9, h * 0.8],  # 右下角
        [w * 0.3, h * 0.96],
    ]

    # 将点转换为适合cv2.findHomography的格式
    pts_src = np.array(points_src, dtype="float32")
    pts_dst = np.array(points_dst, dtype="float32")

    # 计算透视变换矩阵
    matrix, _ = cv2.findHomography(pts_src, pts_dst)

    # 应用透视变换
    transformed_image = cv2.warpPerspective(image, matrix, (w, h))
    transformed_image = cv2.warpPerspective(image, matrix, (w, h), flags=cv2.INTER_LINEAR,
                                            borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))

    return transformed_image


# 示例使用
image_path = 'images/111_hidden.png'  # 图像路径

# 源点，通常是图像的四个角
points_src = [[0, 0], [400, 0], [400, 400], [0, 400]]  # 请根据你的图像尺寸替换w和h

# 应用透视变换以改变形状
transformed_image = apply_perspective_shape_change(image_path, points_src)

# 显示结果
cv2.imshow("Shape Changed Image", transformed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
output_path = 'transformed_image.jpg'  # 保存路径
cv2.imwrite(output_path, transformed_image)
