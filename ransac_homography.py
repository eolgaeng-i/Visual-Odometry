import numpy as np
import matplotlib.pyplot as plt
import math

# 데이터 샘플 (keypoints간의 매칭)을 통해 두 이미지에서 동일한 물체나 장면의 특정 부분을 나타냄 
# RANSAC은 이러한 매칭을 사용하여 두 이미지 간의 관계(homography)를 추정함 

# RANSAC 알고리즘을 위한 필요한 반복 횟수를 계산하는 함수
def calculate_ransac_iterations(p=0.99, sample_size=2, outlier_ratio=0.5):
    """RANSAC iteration 계산"""
    # 내부 데이터 비율을 기반으로 필요한 반복 횟수 계산
    value = 1 - (1 - outlier_ratio)**sample_size
    if isinstance(value, complex) or value <= 0:
        return float('inf')  # 무한대 반환
    return math.ceil(math.log(1 - p) / math.log(value))

# 두 이미지 간의 homography 행렬을 계산하는 함수
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

# 주어진 homography 행렬을 사용하여 포인트를 변환하는 함수
def apply_homography(H, src_pts):
    # Homography 행렬을 사용하여 포인트 변환
    src_pts_homogeneous = np.column_stack([src_pts, np.ones(src_pts.shape[0])])
    transformed_pts = np.dot(H, src_pts_homogeneous.T).T
    transformed_pts = transformed_pts[:, :2] / transformed_pts[:, 2:]
    return transformed_pts

# 주어진 homography 행렬을 사용하여 내부 데이터의 수를 계산하는 함수
def count_inliers(H, src_pts, dst_pts, threshold):
    transformed_pts = apply_homography(H, src_pts)
    distances = np.linalg.norm(transformed_pts - dst_pts, axis=1)
    return np.where(distances < threshold)[0]

def find_best_threshold(data, thresholds, max_iterations=100):
    best_threshold = None
    best_model = None
    max_inliers_count = 0

    for threshold in thresholds:
        model = ransac_homography(data, max_iterations, threshold)
        src_pts = data[:, :2]
        dst_pts = data[:, 2:]
        inliers_idx = count_inliers(model, src_pts, dst_pts, threshold)
        
        # 각 threshold에 대한 inlier 개수 출력
        print(f"Threshold: {threshold}, Inliers: {len(inliers_idx)}")
        
        if len(inliers_idx) > max_inliers_count:
            max_inliers_count = len(inliers_idx)
            best_model = model
            best_threshold = threshold

    return best_model, best_threshold

# RANSAC 알고리즘을 사용하여 최적의 homography 행렬을 찾는 함수
def ransac_homography(data, max_iterations=100, threshold=1.0):
    # 최적의 모델 초기화
    best_model = None
    # 최대 내부 데이터 수 초기화
    max_inliers = 0
    # 전체 데이터 수
    total_data = len(data)

    # RANSAC 반복
    for i in range(max_iterations):
        # 데이터 집합에서 무작위로 4개의 데이터 샘플 선택
        subset = data[np.random.choice(total_data, 4, replace=False)]
        src_pts = subset[:, :2]
        dst_pts = subset[:, 2:]
        
        # 선택한 샘플로 homography 계산
        H = compute_homography(src_pts, dst_pts)
        
        # 모델 오차 계산
        inliers_idx = count_inliers(H, src_pts, dst_pts, threshold)
        
        # 내부 데이터 수가 이전의 최대값보다 큰 경우 모델 업데이트
        if len(inliers_idx) > max_inliers:
            best_model = H
            max_inliers = len(inliers_idx)

    return best_model
