import cv2
import numpy as np

def main(image_name):
  # 1. Choose two images 서로 중첩되는 영역이 있는 두 이미지 선택
  img1 = cv2.imread(f'data/{image_name}_1.jpg', cv2.IMREAD_COLOR)  # 이미지 읽기
  img2 = cv2.imread(f'data/{image_name}_2.jpg', cv2.IMREAD_COLOR)

  # 2. compute ORB keypoint and descriptors (opencv) ORB keypoint 및 descriptors 계산
  orb = cv2.ORB_create()
  kp1, des1 = orb.detectAndCompute(img1, None)
  kp2, des2 = orb.detectAndCompute(img2, None)
  img_keypoints1 = cv2.drawKeypoints(img1, kp1, None, color=(0, 255, 0))
  img_keypoints2 = cv2.drawKeypoints(img2, kp2, None, color=(0, 255, 0))
  cv2.imwrite(f'keypoint/{image_name}_output_keypoints1.jpg', img_keypoints1)
  cv2.imwrite(f'keypoint/{image_name}_output_keypoints2.jpg', img_keypoints2)

  # 3. apply Bruteforce matching with Hamming distance (opencv) Hamming distance를 사용한 Bruteforce 매칭 적용
  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
  matches = bf.match(des1, des2)
  matches = sorted(matches, key=lambda x: x.distance)  # 거리 기준으로 정렬
  img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None)  # 상위 50개 매치만 표시
  cv2.imwrite(f'result/{image_name}_output_matches.jpg', img_matches)

  # 4. implement RANSAC algorithm to compute the homography matrix. (DIY) RANSAC 알고리즘으로 homography matrix 계산
  src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
  dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

  M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

  # 5. prepare a panorama image of larger size (DIY) 더 큰 크기의 파노라마 이미지 준비
  h1, w1, _ = img1.shape
  h2, w2, _ = img2.shape
  panorama_w = w1 + w2
  panorama_h = max(h1, h2)

  panorama = np.zeros((panorama_h, panorama_w, 3), dtype=img1.dtype)

  # 6. warp two images to the panorama image using the homography matrix (DIY) homography matrix을 사용하여 이미지 왜곡
  panorama = cv2.warpPerspective(panorama, M, (panorama_w, panorama_h), dst=img2, borderMode=cv2.BORDER_TRANSPARENT)
  panorama[0:h1, 0:w1, :] = img1
  panorama[0:h2, 0:w2] = img2
  
  # 7. 결과 이미지 저장
  cv2.imwrite(f'result/{image_name}_result_panorama.jpg', panorama)

if __name__=='__main__':
  for i in range(8,9):
    main(f'image{i}')