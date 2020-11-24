import numpy as np

width = 2
height = 2
img1 = np.array([[[1, 2, 3, 0], [4, 5, 6, 0]], [[7, 8, 9, 0], [10, 11, 12, 0]]])
img2 = np.array([[[12, 11, 10, 0], [9, 8, 7, 0]], [[6, 5, 4, 0], [3, 2, 1, 0]]])
# удаляем альфа-столбец
sliced_img1 = np.delete(img1, 3, axis=2)
sliced_img2 = np.delete(img2, 3, axis=2)
# разность между картинками
diff = sliced_img2 - sliced_img1
# возведение разности в степень
powered_diff = np.power(diff, 2)
print('diff')
print(diff)
print('powered diff')
print(powered_diff)
all_sum = np.sum(powered_diff)
print('all sum')
print(all_sum)
# вычисляем суммы r, g, b в каждой строке
sum1 = np.sum(powered_diff, axis=1)
print('sum 1')
print(sum1)
# суммируем r, g, b всех строк воедино
sum2 = np.sum(sum1, axis=0)
print('sum 2')
print(sum2)

psnr = 10 * np.log10(3 * 255 * 255 * width * height / all_sum)
psnr_r = 10 * np.log10(255 * 255 * width * height / sum2[0])
psnr_g = 10 * np.log10(255 * 255 * width * height / sum2[1])
psnr_b = 10 * np.log10(255 * 255 * width * height / sum2[2])
print(psnr, psnr_r, psnr_g, psnr_b)

