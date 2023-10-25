# Visual-Odometry
비주얼오도메트리와증강현실(AIE6660-01)

# 중간시험과제: automatic stitching of two images
1. take two views in Sogang University.
<p align="center">
  <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/95f1f285-a947-460f-a31e-0c00d1e7d1df" align="center" width="32%">
  <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/24da1ed4-f71c-4671-bc94-bf6b6bf12782" align="center" width="32%">
</p>
3. develop a ORB + Ransac + homography algorithm to create a panorama image from the two inputs.
  3-1. compute ORB keypoint and descriptors (opencv)
  <p align="center">
   <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/d4590ba2-dde2-49dc-839a-bd58db9b8db3" align="center" width="32%">
   <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/5a664a58-9fbf-4b90-9553-5aa538d0bcbf" align="center" width="32%">
  </p>
  3-2. apply Bruteforce matching with Hamming distance (opencv)
  <p align="center">
   <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/6692d4a0-14dd-48b4-b0f6-2ac9a6a2dd17" align="center" width="64%">
  </p>
  3-3. implement RANSAC algorithm to compute the homography matrix. (DIY)
  <p><img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/0a181a6a-132d-459f-b790-6261923f5208" align="center" width="64%"></p>
  3-4. prepare a panorama image of larger size (DIY)
  3-5. warp two images to the panorama image using the homography matrix (DIY)
  <p><img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/80820f20-e0f7-4ff8-b052-6d188a7ba7d5" align="center" width="64%"></p>
4. apply the algorithm to get a result.

5. take another set of two views in Sogang University
   <p align="center">
    <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/08dfe77b-56b7-4f5c-b3be-7d4e8e6600d0" align="center" width="32%">
    <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/fd80c0b4-d30c-4126-b358-20a6d9cc6837" align="center" width="32%">
  </p>
![image3_1](![image2_result_panorama](https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/00de2a55-2758-4d3b-a92a-2571071f050d))

<p align="center"><img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/f1c088d4-14fb-400e-8a44-54085ce9b84a" align="center" width="32%"></p>
7. produce output

Submit: link to your github repository 
- it must contain a pdf report describint the problem, algorithm, experimental results
- and the source code
- Readme.md file must be presented. It should be a short version of the report.

Some students will be presenting the report during the class.

# OpenCV를 사용한 코드와 비교
  #TODO
# 순서도
  #TODO
