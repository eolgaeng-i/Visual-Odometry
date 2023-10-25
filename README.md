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
  <p align="center"><img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/0a181a6a-132d-459f-b790-6261923f5208" align="center" width="64%"></p>
  3-4. prepare a panorama image of larger size (DIY)
  3-5. warp two images to the panorama image using the homography matrix (DIY)
  <p align="center"><img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/00de2a55-2758-4d3b-a92a-2571071f050d" align="center" width="64%"></p>
4. apply the algorithm to get a result.

5. take another set of two views in Sogang University
     <p align="center">
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/08dfe77b-56b7-4f5c-b3be-7d4e8e6600d0" align="center" width="32%">
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/fd80c0b4-d30c-4126-b358-20a6d9cc6837" align="center" width="32%">
    </p>
    <p align="center"><img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/f1c088d4-14fb-400e-8a44-54085ce9b84a" align="center" width="64%"></p>
    <p align="center"><img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/80820f20-e0f7-4ff8-b052-6d188a7ba7d5" align="center" width="64%"></p>
7. produce output
<table align="center">
  <tr>
    <td align="center"> input </td>
    <td align="center"> output </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/67e39811-0171-40ff-8f9d-7898e0dcd121" align="center" width="32%">
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/e2ceb70e-49ff-4fbf-933f-92e328964d74" align="center" width="32%">
    </td>
    <td>
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/36e71868-7139-4455-9c35-47e23defe2ef" align="center" width="64%">
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/ab219292-2981-4351-ac21-0be2f28bad09" align="center" width="32%">
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/19caf6e0-7e66-4235-aa36-292a96997a55" align="center" width="32%">
    </td>
    <td>
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/3d56492b-31a0-426c-8818-203e3ee97226" align="center" width="64%">
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/87f9bf64-6c0f-4c34-a2d9-9fe37a89f54b" align="center" width="32%">
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/31cca7fa-a1b5-4d30-9fbf-72735d2631ed" align="center" width="32%">
    </td>
    <td>
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/1f98619f-b800-4b18-83b5-026a656e9ebc" align="center" width="64%">
    </td>
  </tr>
</table>


# OpenCV를 사용한 결과와 비교
<table align="center">
  <tr>
    <td align="center"> OpenCV </td>
    <td align="center"> DIY </td>
  </tr>
    <tr>
    <td>
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/0f774cfc-307a-4688-a851-eda205394e3a" align="center" width="64%">
    </td>
    <td>
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/00de2a55-2758-4d3b-a92a-2571071f050d" align="center" width="64%">
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/cbbe07d7-b86c-46a2-9444-71f3938c0ac4" align="center" width="64%">  
    </td>
    <td>
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/80820f20-e0f7-4ff8-b052-6d188a7ba7d5" align="center" width="64%">
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/72f670c9-4cc8-4c79-b857-46610c00e22f" align="center" width="64%">
    </td>
    <td>
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/36e71868-7139-4455-9c35-47e23defe2ef" align="center" width="64%">
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/38ebc432-a029-48c3-a978-fe0f6aec6517" align="center" width="64%">
    </td>
    <td>
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/3d56492b-31a0-426c-8818-203e3ee97226" align="center" width="64%">
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/d13dcf57-e345-4ed3-840f-380d840c4c17" align="center" width="64%">  
    </td>
    <td>
      <img src="https://github.com/eolgaeng-i/Visual-Odometry/assets/46189116/1f98619f-b800-4b18-83b5-026a656e9ebc" align="center" width="64%">
    </td>
  </tr>
</table>
