filename='original.png';
noise=0.5;
im=imread(filename);
if size(im,3)==3
    im=rgb2gray(im);
end
noisy_im=imnoise(im,'salt & pepper',noise);
imwrite(noisy_im,'noisy.png');