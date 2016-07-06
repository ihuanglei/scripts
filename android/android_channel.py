import zipfile
import shutil
import os

#######################################################
### 

###
VER = '0.0.1'

###
CHANNELS = ['360','qq','xiaomi']

#######################################################

EMPTY_FILE = 'empty'

CHANNEL_FILE = 'META-INF/channel_{ch}'

ORIGIN_FILE = 'release-{ver}.apk'.format(ver=VER)

print('ver='+VER)

print('check apk')

if not os.path.exists(ORIGIN_FILE):
	print(ORIGIN_FILE+' not found!!!')
	exit()

print(ORIGIN_FILE + ' found ')
	
if not os.path.exists(EMPTY_FILE):
	f = open(EMPTY_FILE,'w')
	f.close()

for ch in CHANNELS:

	print('create channel {ch}'.format(ch=ch))
	fileName = '{ch}-release-{ver}.apk'.format(ch=ch,ver=VER)
	shutil.copyfile(ORIGIN_FILE,fileName)
	
	print('file {fileName}'.format(fileName=fileName))
	
	with zipfile.ZipFile(fileName,'a',zipfile.ZIP_DEFLATED) as zf:
		zf.write(EMPTY_FILE,CHANNEL_FILE.format(ch=ch))
		zf.close()
		
		
print('end')