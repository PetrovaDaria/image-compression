import numpy as np
import math


def calculate_psnr(img1, img2):
    width = img1.shape[0]
    height = img1.shape[1]

    # удаляем альфа-столбец
    sliced_img1 = np.delete(img1, 3, axis=2)
    sliced_img2 = np.delete(img2, 3, axis=2)

    # разность между картинками
    diff = sliced_img2 - sliced_img1

    # возведение разности в степень
    powered_diff = np.power(diff, 2)

    # сумма всех пикселей по всем каналам
    all_mse = np.sum(powered_diff)

    # вычисляем суммы значений r, g, b в каждой строке
    rgb_mse_by_line = np.sum(powered_diff, axis=1)

    # суммируем r, g, b всех строк воедино
    rgb_mse = np.sum(rgb_mse_by_line, axis=0)

    r_mse = rgb_mse[0]
    g_mse = rgb_mse[1]
    b_mse = rgb_mse[2]

    # вычисляем psnr с учетом возможного нуля в знаменателе
    psnr = 10 * np.log10(3 * 255 * 255 * width * height / all_mse) if all_mse != 0 else math.inf
    psnr_r = 10 * np.log10(255 * 255 * width * height / r_mse) if r_mse != 0 else math.inf
    psnr_g = 10 * np.log10(255 * 255 * width * height / g_mse) if g_mse != 0 else math.inf
    psnr_b = 10 * np.log10(255 * 255 * width * height / b_mse) if b_mse != 0 else math.inf

    print(psnr, psnr_r, psnr_g, psnr_b)
    return psnr, psnr_r, psnr_g, psnr_b
