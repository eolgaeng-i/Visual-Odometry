import numpy as np
from ransac_homography import apply_homography

def warpImages(img1, img2, H):
    # 이미지의 행과 열 크기를 가져옵니다.
    rows1, cols1 = img1.shape[:2]
    rows2, cols2 = img2.shape[:2]

    # 각 이미지의 모서리 좌표를 정의합니다.
    list_of_points_1 = np.float32([[0, 0], [0, rows1], [cols1, rows1], [cols1, 0]])
    temp_points = np.float32([[0, 0], [0, rows2], [cols2, rows2], [cols2, 0]])

    # Homography를 사용하여 img2의 모서리 좌표를 변환합니다.
    list_of_points_2 = apply_homography(H, temp_points)

    # 두 이미지의 모서리 좌표를 결합합니다.
    list_of_points = np.concatenate((list_of_points_1, list_of_points_2), axis=0)

    # 변환된 좌표의 최소 및 최대 값을 계산합니다.
    [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
    [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)

    # 출력 이미지 내에서 원본 이미지의 시작 위치를 계산합니다.
    translation_dist = [-x_min, -y_min]

    # 이동 행렬을 생성합니다.
    H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])
    H = np.dot(H_translation, H)

    # 5. prepare a panorama image of larger size (DIY) 더 큰 크기의 파노라마 이미지 준비
    # 출력 이미지의 크기를 설정하고 초기화합니다.
    h1, w1, _ = img1.shape
    h2, w2, _ = img2.shape
    # panorama_w = w1 + w2
    # panorama_h = max(h1, h2)
    output_shape = (y_max - y_min, x_max - x_min, 3)
    output_img = np.zeros(output_shape, dtype=img2.dtype)

    # 출력 이미지의 모든 좌표에 대한 그리드를 생성합니다.
    y, x = np.indices(output_shape[:2])
    homogeneous_coords = np.stack((x.ravel(), y.ravel(), np.ones(y.size)))

    # 역 Homography 행렬을 적용하여 원본 좌표를 계산합니다.
    transformed_coords = np.dot(np.linalg.inv(H), homogeneous_coords)
    transformed_coords /= transformed_coords[2]

    x_src, y_src = transformed_coords[0], transformed_coords[1]

    # 변환된 좌표가 img2 내에 있는지 확인하는 마스크를 생성합니다.
    mask = (0 <= x_src) & (x_src < cols2) & (0 <= y_src) & (y_src < rows2)

    # 추가적으로, 변환된 좌표가 유효한지 (NaN 또는 무한대 값이 아닌지) 확인하는 마스크를 생성합니다.
    valid_mask = ~np.isnan(x_src) & ~np.isnan(y_src) & ~np.isinf(x_src) & ~np.isinf(y_src)

    # 두 마스크를 결합합니다.
    final_mask = mask & valid_mask

    # 마스크를 사용하여 유효한 좌표만 정수로 변환합니다.
    x_src = x_src[final_mask].astype(int)
    y_src = y_src[final_mask].astype(int)

    # 마스크를 사용하여 유효한 좌표만 선택합니다.
    valid_x = x.ravel()[final_mask]
    valid_y = y.ravel()[final_mask]

    # img2에서 유효한 좌표를 출력 이미지로 매핑합니다.
    output_img[valid_y, valid_x] = img2[y_src, x_src]


    # img1을 출력 이미지에 오버레이합니다.
    output_img[translation_dist[1]:rows1 + translation_dist[1], translation_dist[0]:cols1 + translation_dist[0]] = img1

    return output_img
