import cv2
import numpy as np

def warpImages(img1, img2, H):
    rows1, cols1 = img1.shape[:2]
    rows2, cols2 = img2.shape[:2]

    list_of_points_1 = np.float32([[0,0], [0,rows1], [cols1,rows1], [cols1,0]]).reshape(-1,1,2)
    temp_points = np.float32([[0,0], [0,rows2], [cols2,rows2], [cols2,0]]).reshape(-1,1,2)
    list_of_points_2 = cv2.perspectiveTransform(temp_points, H)

    list_of_points = np.concatenate((list_of_points_1, list_of_points_2), axis=0)

    [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
    [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)

    translation_dist = [-x_min, -y_min]
    H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])

    output_img = cv2.warpPerspective(img2, H_translation.dot(H), (x_max-x_min, y_max-y_min))
    output_img[translation_dist[1]:rows1+translation_dist[1], translation_dist[0]:cols1+translation_dist[0]] = img1

    return output_img

def main(image_name):
    # 1. Choose two images 서로 중첩되는 영역이 있는 두 이미지 선택
    img1 = cv2.imread(f'data/{image_name}_1.jpg', cv2.IMREAD_COLOR)  # 이미지 읽기
    img2 = cv2.imread(f'data/{image_name}_2.jpg', cv2.IMREAD_COLOR)

    # 2. compute ORB keypoint and descriptors (opencv) ORB keypoint 및 descriptors 계산
    orb = cv2.ORB_create(nfeatures=2000)  # 웹사이트의 내용에 따라 nfeatures를 2000으로 설정
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    img_keypoints1 = cv2.drawKeypoints(img1, kp1, None, color=(0, 255, 0))
    img_keypoints2 = cv2.drawKeypoints(img2, kp2, None, color=(0, 255, 0))
    cv2.imwrite(f'keypoint/{image_name}_output_keypoints1.jpg', img_keypoints1)
    cv2.imwrite(f'keypoint/{image_name}_output_keypoints2.jpg', img_keypoints2)

    # 3. apply Bruteforce matching with Hamming distance (opencv) Hamming distance를 사용한 Bruteforce 매칭 적용
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(des1, des2, k=2)  # 웹사이트의 내용에 따라 knnMatch를 사용

    # Lowe's ratio test를 적용하여 좋은 매치만 선택
    good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]
    img_matches = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None)
    cv2.imwrite(f'result/{image_name}_output_matches.jpg', img_matches)

    # 4. implement RANSAC algorithm to compute the homography matrix. (DIY) RANSAC 알고리즘으로 homography matrix 계산
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # 5. prepare a panorama image of larger size (DIY) 더 큰 크기의 파노라마 이미지 준비
    h1, w1, _ = img1.shape
    h2, w2, _ = img2.shape
    panorama_w = w1 + w2
    panorama_h = max(h1, h2)

    # 6. warp two images to the panorama image using the homography matrix (DIY) homography matrix을 사용하여 이미지 왜곡
    panorama = warpImages(img2, img1, M)

    # 7. 결과 이미지 저장
    cv2.imwrite(f'result/{image_name}_result_panorama.jpg', panorama)

if __name__=='__main__':
    for i in range(1,9):
        main(f'image{i}')
