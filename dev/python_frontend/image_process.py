import cv2
import numpy as np
import imutils


def pattern_to_image(_pattern, _pattern_size, rgb=(255, 255, 255), background=0,
                     size_im=500):
    """
    :param display_size: 화면 크기
    :param backgroundrgb: 배경 rgb값
    :param rgb: 색상 rgb 값
    :param _pattern: pattern 을 rgb 255로 변경, np.uint8로 변경, 1 혹은 -1인 1차 배열
    :param _pattern_size: 패턴 크기
    :return: 이미지 np 배열, 0~255
    """
    nptyped = np.array(_pattern)
    squared = nptyped.reshape((_pattern_size, _pattern_size))
    hadamard_pattern1 = cv2.resize(squared, (size_im, size_im), interpolation=cv2.INTER_NEAREST)
    hadamard_pattern_front = hadamard_pattern1==1
    hadamard_pattern_back = hadamard_pattern1==-1
    image = np.stack([rgb[0] * hadamard_pattern_front + background * hadamard_pattern_back,
                      rgb[1] * hadamard_pattern_front + background * hadamard_pattern_back,
                      rgb[2] * hadamard_pattern_front + background * hadamard_pattern_back],
                     axis=-1)
    return (image).astype(np.uint8)
    # return (hadamard_pattern1<127)*light + (hadamard_pattern1>=127)*background


def measured_pattern_to_image(_pattern: np.ndarray, _pattern_size, scale=3, sigma=2, rgb=(255, 255, 255),
                              display_size=(256, 256)):
    """
    :param display_size: 화면 크기
    :param backgroundrgb: 배경 rgb값
    :param rgb: 색상 rgb 값
    :param _pattern: 측정치 배열
    :param _pattern_size: 패턴 크기
    :return: 이미지 np 배열. -~255
    """
    scaled = _pattern * scale
    mean = scaled.mean()
    std = scaled.std()
    cliped = scaled.clip(min=mean - std * sigma, max=mean + std * sigma)
    normalized = (cliped - cliped.min())
    normalized = normalized / normalized.max()
    sized = cv2.resize(normalized.reshape((_pattern_size, _pattern_size)),
                       display_size,
                       interpolation=cv2.INTER_NEAREST)
    return np.stack([rgb[0] * sized,
                     rgb[1] * sized,
                     rgb[2] * sized],
                    axis=-1).astype(np.uint8)


def rotation(image, angle=135):
    return imutils.rotate_bound(image, angle=angle)
# if __name__ == "__main__" :


# cv2.imshow('title',
#            rotation(pattern_to_image(np.array([1, 0, 0, 1]), 2)))
# cv2.waitKey(1000)

