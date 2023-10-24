import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math

def calculate_ransac_iterations(p=0.99, sample_size=2, outlier_ratio=0.5):
    """RANSAC iteration 계산"""
    # math.log 함수의 인자가 음수가 되지 않도록 검사
    value = 1 - (1 - outlier_ratio)**sample_size
    if isinstance(value, complex) or value <= 0:
        return float('inf')  # 무한대 반환
    return math.ceil(math.log(1 - p) / math.log(value))

def compute_homography(src_pts, dst_pts):
    # DLT를 사용하여 homography 행렬 계산
    A = []
    for i in range(0, src_pts.shape[0]):
        x, y = src_pts[i]
        u, v = dst_pts[i]
        A.append([-x, -y, -1, 0, 0, 0, u*x, u*y, u])
        A.append([0, 0, 0, -x, -y, -1, v*x, v*y, v])
    A = np.asarray(A)
    U, S, Vh = np.linalg.svd(A)
    L = Vh[-1,:] / Vh[-1,-1]
    H = L.reshape(3, 3)
    return H

def apply_homography(H, src_pts):
    # Homography 행렬을 사용하여 포인트 변환
    src_pts_homogeneous = np.column_stack([src_pts, np.ones(src_pts.shape[0])])
    transformed_pts = np.dot(H, src_pts_homogeneous.T).T
    transformed_pts = transformed_pts[:, :2] / transformed_pts[:, 2:]
    return transformed_pts

def count_inliers(H, src_pts, dst_pts, threshold):
    transformed_pts = apply_homography(H, src_pts)
    distances = np.linalg.norm(transformed_pts - dst_pts, axis=1)
    return np.where(distances < threshold)[0]

def ransac_homography(data, max_iterations=100, threshold=1.0):
    best_model = None
    max_inliers = 0
    total_data = len(data)

    for i in range(max_iterations):
        subset = data[np.random.choice(total_data, 4, replace=False)]
        src_pts = subset[:, :2]
        dst_pts = subset[:, 2:]
        H = compute_homography(src_pts, dst_pts)
        inliers_idx = count_inliers(H, src_pts, dst_pts, threshold)
        if len(inliers_idx) > max_inliers:
            best_model = H
            max_inliers = len(inliers_idx)

    return best_model
