clear, close, clc

data = h5read('bedrock.h5', '/data');
xsize = 30;
ysize = 100;
h = 0.1;
nx = xsize/h;
ny = ysize/h;
reshapeddata = reshape(data, [ny, nx]);
imagesc(reshapeddata)