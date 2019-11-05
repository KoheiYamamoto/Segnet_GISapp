# 1. get all the filenames of images in test (after renamed) dir
# 2. overwrite test.txt
# 3. duplicate random testannot file(0001TP_008550.png), the no. of file is corresponding the length of the above filenames

import glob
import shutil

path2dir = './CamVid/'

def getfilenames():
	paths = glob.glob(path2dir + 'test/*')
	names = []
	for path in paths:
		names.append(path.lstrip('./CamVid/test/'))
	return names

def rewritetxt(imagenames):
	l = []
	for name in imagenames:
		# Attention!! specified 'Segnet' below
		l.append('/SegNet/CamVid/test/' + name + ' ' + '/SegNet/CamVid/testannot/' + name)

	with open(path2dir + 'test.txt', mode='w') as f:
		f.write('\n'.join(l))
		f.write("\n")

def duplicate_testannot_img(imagenames):
	originalImg = path2dir + '0001TP_008550.png'
	for name in imagenames:
		print(name)
		shutil.copy(originalImg, path2dir + 'testannot/' + name)

def main():
	names = getfilenames()
	rewritetxt(names)
	duplicate_testannot_img(names)

if __name__ == '__main__':
    main()