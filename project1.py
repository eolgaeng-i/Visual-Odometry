{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNbpoimnvWFLeDvTPjl3ya/",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/eolgaeng-i/Visual-Odometry/blob/main/project1.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "hxwnm5wsh32_"
      },
      "outputs": [],
      "source": [
        "import cv2\n",
        "\n",
        "img1 = cv2.imread('image1.jpg', 0)  # 흑백으로 이미지 읽기\n",
        "img2 = cv2.imread('image2.jpg', 0)\n",
        "\n",
        "orb = cv2.ORB_create()\n",
        "kp1, des1 = orb.detectAndCompute(img1, None)\n",
        "kp2, des2 = orb.detectAndCompute(img2, None)\n"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)\n",
        "matches = bf.match(des1, des2)\n",
        "matches = sorted(matches, key=lambda x: x.distance)  # 거리 기준으로 정렬\n"
      ],
      "metadata": {
        "id": "gX3rz61IlNlK"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)\n",
        "dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)\n",
        "\n",
        "M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)\n"
      ],
      "metadata": {
        "id": "5cB70YXZlODM"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}