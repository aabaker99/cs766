[infile,path] = uigetfile('*.*')
filePath = strcat(path,infile);
% arr = imread(infile);
arr = imread(filePath);
bw = imbinarize(arr);
% figure(3);
% imshow(bw);
[L, num] = bwlabel(bw);
BW2 = bwperim(bw);
% figure(4);
% imshow(BW2);

% % -----------------
% adjudting the intensity histogram.
[infile2,path2] = uigetfile('*.*');
filePath2 = strcat(path2,infile2);
arr2 = imread(filePath2);

J = histeq(arr);
H = histeq(arr2);
figure(6); 
imshowpair(J,H,'montage');
%imshowpair(adapthisteq(arr),J,'montage');
% % -----------------
rv = zeros(num,2);
stats = regionprops(L, 'centroid');
for i=1:num
    stats_struct = stats(i);
    centroid = stats_struct.Centroid;
    rv(i,:) = centroid;
end

%%

[infile,path] = uigetfile('*.*');
filePath = strcat(path,infile);
A = imread(filePath);
[infile,path] = uigetfile('*.*');
filePath = strcat(path,infile);
B = imread(filePath);
[infile,path] = uigetfile('*.*');
filePath = strcat(path,infile);
C = imread(filePath);
[infile,path] = uigetfile('*.*');
filePath = strcat(path,infile);
D = imread(filePath);
[infile,path] = uigetfile('*.*');
filePath = strcat(path,infile);
E = imread(filePath);
%%
imshow(((adapthisteq(C))));
[labeledImage, numberOfObject] = bwlabel(imbinarize(C));
numberOfObject
rv = zeros(numberOfObject,2);
  stats = regionprops(labeledImage, 'centroid');
  for i=1:numberOfObject
    stats_struct = stats(i);
    centroid = stats_struct.Centroid;
    rv(i,:) = centroid;
  end
%imshowpair(histeq(C),histeq(E),'blend');
%%
P = imfuse(C, E,'blend','Scaling','joint');
figure; imshow(P);hold on;
%figure; imshowpair(C,P,'montage');
%pts = csvread('centers.csv');
plot(rv(:,1),rv(:,2),'r*'); 
%imshow(imfuse(C,E,'blend','Scaling','joint'));
%% % watershed algorithm
Pp = (adapthisteq(P));
figure; imshow(Pp);
%imshowpair(P,Pp,'montage');
% 
% rng(1); % For reproducibility
% [idx,C] = kmeans(Pp,3);
%%
bw  = im2bw(Pp, graythresh(Pp));
figure;imshow(bw);
%%
Q = bwdist(~bw);
figure;
imshow(Q);
% Complement distance transform
Q = -Q;
Q(~bw) = Inf;

bw3 = imopen(bw, strel('disk',2));
figure;imshow(bw3);

bw4 = bwareaopen(bw3, 100);
bw4_perim = bwperim(bw4);
overlay1 = imoverlay(Q, bw4_perim, [1 .3 .3]);
imshow(overlay1)

maxs = imextendedmax(Q,  5);
maxs = imclose(maxs, strel('disk',3));
maxs = imfill(maxs, 'holes');
maxs = bwareaopen(maxs, 2);
overlay2 = imoverlay(Q, bw4_perim | maxs, [1 .3 .3]);

Jc = imcomplement(Q);
I_mod = imimposemin(Jc, ~bw4 | maxs);

L = watershed(I_mod);
labeledImage = label2rgb(L);
[L, num] = bwlabel(L);
%%
I = rgb2gray(imread('fusedCE+hist.jpg'));
I = adapthisteq(I);
im = im2bw(I, graythresh(I));
figure; imshow(im)
[L, num] = bwlabel(im);
num
%%
subplot(1,2,1);imshow(Pp);
mask = ones(size(Pp));
iter = 2000
bw = activecontour(Pp, mask, iter, 'Chan-Vese','ContractionBias',0);
subplot(1,2,2)
imshow(bw)
title(strcat('Segmented Image ( # Iterations = ',num2str(iter),' )'));
