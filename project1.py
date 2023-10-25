import cv2
import numpy as np
import math
from ransac_homography import ransac_homography, calculate_ransac_iterations, apply_homography, find_best_threshold, count_inliers
from warpImage import warpImages
import os

def main(image_name):
    # 1. Choose two images 서로 중첩되는 영역이 있는 두 이미지 선택
    # 이미지 파일의 경로를 정의합니다.
    img1_path = f'data/{image_name}_1.jpg'
    img2_path = f'data/{image_name}_2.jpg'

    # 이미지 파일이 존재하는지 확인합니다.
    if not os.path.exists(img1_path) or not os.path.exists(img2_path):
        print(f"Images {img1_path} or {img2_path} not found. Skipping...")
        return

    # 이미지 파일이 존재하면 읽어옵니다.
    img1 = cv2.imread(img1_path, cv2.IMREAD_COLOR)
    img2 = cv2.imread(img2_path, cv2.IMREAD_COLOR)

    # 2. compute ORB keypoint and descriptors (opencv) ORB keypoint 및 descriptors 계산
    orb = cv2.ORB_create()  
    kp1, des1 = orb.detectAndCompute(img1, None) # keypoint(위치)와 descriptor(위치의 특징)반환 
    kp2, des2 = orb.detectAndCompute(img2, None)
    img_keypoints1 = cv2.drawKeypoints(img1, kp1, None, color=(0, 255, 0))
    img_keypoints2 = cv2.drawKeypoints(img2, kp2, None, color=(0, 255, 0))
    cv2.imwrite(f'keypoint/{image_name}_output_keypoints1.jpg', img_keypoints1)
    cv2.imwrite(f'keypoint/{image_name}_output_keypoints2.jpg', img_keypoints2)

    # 3. apply Bruteforce matching with Hamming distance (opencv) Hamming distance를 사용한 Bruteforce 매칭 적용
    bf = cv2.BFMatcher(cv2.NORM_HAMMING) # Brute-Force 매칭 수행, NORM_HAMMING : Hamming 거리를 사용한 매칭 수행
    matches = bf.knnMatch(des1, des2, k=2)  # 가장 가까운 두 개의 디스크립터 반환

    # Lowe's ratio test를 적용하여 좋은 매치만 선택 
    # 매치 간의 거리 비율을 사용하여 0.75보다 낮은 매치를 필터링
    good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]
    img_matches = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None)
    cv2.imwrite(f'keypoint_matches/{image_name}_output_matches.jpg', img_matches)

    # 좋은 매치 수 확인 특징점이 4개보다 적은 경우 해당 이미지를 건너뜀
    if len(good_matches) < 4:
        print(f"Not enough matches for image {image_name}. Skipping...")
        return

    # 4. implement RANSAC algorithm to compute the homography matrix. (DIY) RANSAC 알고리즘으로 homography matrix 계산
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches])
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches])

    # RANSAC을 사용하여 homography 행렬 계산
    outlier_ratio = np.arange(0.5, 10.0, 0.5) #outlier리스트

    data = np.hstack((src_pts, dst_pts)) #매칭 리스트
    max_iterations = calculate_ransac_iterations()
    M, best_threshold = find_best_threshold(image_name, data, outlier_ratio, max_iterations)
    print(f"Best threshold: {best_threshold}")

    # RANSAC을 사용하여 찾은 inliers를 기반으로 매칭 이미지 생성
    inliers_idx = count_inliers(M, src_pts, dst_pts, best_threshold)
    inlier_matches = [good_matches[i] for i in inliers_idx]
    img_inlier_matches = cv2.drawMatches(img1, kp1, img2, kp2, inlier_matches, None)
    cv2.imwrite(f'ransac_homography_result/{image_name}_output_inlier_matches.jpg', img_inlier_matches)

    # 5. prepare a panorama image of larger size (DIY) 더 큰 크기의 파노라마 이미지 준비
    # 6. warp two images to the panorama image using the homography matrix (DIY) homography matrix을 사용하여 이미지 왜곡
    panorama = warpImages(img2, img1, M)

    # 7. 결과 이미지 저장
    cv2.imwrite(f'result/{image_name}_result_panorama.jpg', panorama)
    print(f"{image_name} 처리 완료!")

if __name__=='__main__':
    image_number = input("이미지 번호를 입력하세요 (예: 1, 2, ...): ")
    main(f'image{image_number}')
    # for i in range(1,9):
    #     main(f'image{i}')