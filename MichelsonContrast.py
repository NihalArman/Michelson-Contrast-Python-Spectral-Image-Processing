import matplotlib.pyplot as plt
import numpy

#Read Spectral Image
path = r'F:\PHD\UEF Thesis\image set\card photogrammetry\Green paper photogrametry spectral images set\409\capture'

#Read HDR Content
hdr_path = r'F:\PHD\UEF Thesis\image set\card photogrammetry\Green paper photogrametry spectral images set\409\capture\409.hdr'

SpectralSample = 0
SpectralBand = 0
SpectralLine = 0

def read_hdr(hdr_path):
    f=open(hdr_path, "r")
    filelines = f.readlines()

    # This reads everything from hdr file
#     for fileline in filelines:
#         print(fileline)
# read_hdr(hdr_path)
    f.close()
    bands = ''
    for fileline in filelines:
        if 'samples' in fileline.lower():
            samples = int(fileline.replace('samples = ',''))
            #print("print sample: ", end ='')
            #print(samples)

            #saving the value globally
            global SpectralSample
            SpectralSample = samples
        if bands == '' and 'bands' in fileline.lower():
            bands = int(fileline.replace('bands = ',''))
            #print(bands)

            # saving the value globally
            global SpectralBand
            SpectralBand = bands
        if 'lines' in fileline.lower():
            lines = int(fileline.replace('lines = ',''))
            # saving the value globally
            global SpectralLine
            SpectralLine = lines

#run function
read_hdr(hdr_path)
#print
print("print spectral sample: ", end ='')
print(SpectralSample)

print("print spectral band: ", end ='')
print(SpectralBand)

print("print spectral lines: ", end ='')
print(SpectralLine)

#Read Waves
n = 0

f=open(hdr_path, "r")
filelines = f.readlines()
bands = ''
n1 = filelines.index('wavelength = {\n')+1
n2 = n1 + SpectralBand

waves = numpy.zeros(n2-n1,)
for i in range(n1,n2):
    waves[n] = float(filelines[i].replace(',\n', ''))
    n=n+1


#selecting an area
spatial_pixels = 512
sample_lines = 512
spectral_bands = 204
open_path = r'F:\PHD\UEF Thesis\image set\card photogrammetry\Green paper photogrametry spectral images set\409\capture\409.raw'
fopen = open(open_path, "rb")
u = numpy.fromfile(fopen, dtype=numpy.uint16) #uint16 float32 #count=spatial_pixels*sample_lines*spectral_bands
print(u.shape)
print(spatial_pixels*sample_lines*spectral_bands)
spectral_image = numpy.reshape(u, (sample_lines, spectral_bands, spatial_pixels))
print(spectral_image.shape)


# Both tape and paper area for finding contrast

w = 115

##This is a small area from paper with no pencil. contrast 0.01382
# x1 = 140
# x2 = 145
# y1 = 140
# y2 = 145

x1 = 135 #up dowm
x2 = 200
y1 = 135
y2 = 200

count = 1
michelsonContrast = []
for w in range(len(waves)):
    print('band no: ', count)
    print('wave no: ', waves[w])
    maxx = numpy.amax(spectral_image[x1:x2, w, y1:y2])
    minn = numpy.amin(spectral_image[x1:x2, w, y1:y2])
    print('max is:', maxx)
    print('mix is:', minn)
    average = (maxx - minn) / (maxx + minn)
    print('max-min/max+min :', average)
    michelsonContrast.append(average)
    # spectral_image[x1:x2,w,y1:y2]=1000
    #plt.imshow(spectral_image[:, w, :], cmap="gray")
    plt.show()
    count = count+1
    print('--------------------')

print('printing michelsoncontrast:')
for m in michelsonContrast:
    print(m)

plt.plot(michelsonContrast)
plt.xlabel('waves/band')
plt.ylabel('contrast')
plt.show()


# count = 1
# maxx = numpy.amax(spectral_image[x1:x2, w, y1:y2])
# minn = numpy.amin(spectral_image[x1:x2, w, y1:y2])
# print('max is:', maxx)
# print('mix is:', minn)
# print('band no: ', count)
# print('wave no: ', w)
# print('max-min/max+min :', (maxx - minn) / (maxx + minn))
# # spectral_image[x1:x2,w,y1:y2]=1000
# plt.imshow(spectral_image[:, w, :], cmap="gray")
# plt.show()



