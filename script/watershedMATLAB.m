% get the nucleus channel of any image
% Example taken :  a01s06
 
[infile,path] = uigetfile('*.*');
filePath = strcat(path,infile);
C = imread(filePath);

% get the cytoplasm channel
[infile,path] = uigetfile('*.*');
filePath = strcat(path,infile);
E = imread(filePath);
%%
% Get the cell centers  using nucleus channel
[labeledImage, numberOfObject] = bwlabel(imbinarize(C));
numberOfObject
rv = zeros(numberOfObject,2);
stats = regionprops(labeledImage, 'centroid');
for i=1:numberOfObject
    stats_struct = stats(i);
    centroid = stats_struct.Centroid;
    rv(i,:) = centroid;
end
%%
% Fuse these both to get the good quality image
P = (imfuse(C, E,'blend','Scaling','joint'));
%P = imfuse(C,E);
%P = imclearborder(((P)),4);
figure, imshow(P)
%%

th =  graythresh(P)
%figure(2); imshowpair(P,im2bw(P,0.06),'montage');hold on;
figure; imshowpair(C,P,'blend'); hold on;
imshow(imadjust(C));hold on;
plot(rv(:,1),rv(:,2),'r*');
rvI = round(rv);

%% Convert to binary image for watershed
temp = P;
Ppp =  im2bw(temp, graythresh(P));
figure; imshow(Ppp);
imwrite(double(Ppp), 'tempImage.tiff');
% Compute distance transform
%%
Q = -bwdist(~Ppp);
imshow(Q,[])
%%
% compute watershed
Ld = watershed(Q);
figure; imshow(label2rgb(Ld))
%%
Ppp2 = P%Ppp;
Ppp2(Ld == 0) = 0;
figure; imshow(Ppp2)
%%
% Watershed is known for oversegmenting. % Enforce minima
%mask = imextendedmin(Q,2,8);

% Create a mask of minimas 
u = 5;
mask = false(size(Q));
for i = 1:size(rvI,1)
    l = max(rvI(i,1)-u,1)
    m = min(rvI(i,1),rvI(i,1)+u)
    n = max(1,rvI(i,2)-u)
    o = min(rvI(i,2),rvI(i,2)+u)
    mask(n:o,l:m) = true;
    %mask(rvI(i,1),rvI(i,2)) = true;
end
%mask(rvI) = true;
imshow(mask)
  %%

figure; imshowpair(Ppp, mask, 'blend')

% Now compute watershed again
Q2 = imimposemin(Q,mask);
%%
Ld2 = watershed(Q2);%figure; imshow(label2rgb(Ld2))
Ppp3 = Ppp;
Ppp3(Ld2 == 0) = 0;
figure; imshow(Ppp3);
figure;imshow(label2rgb(Ppp3));
temp2 = imfuse(C,E);
temp2(Ld2==0)=0;
figure, imshow(temp2);
temp2 = P;
temp2(Ld2==0)=0;
figure, imshow(temp2);
%% For active contour 
mask = ones(size(P));
figure, imshow(P);
[~,threshold] = edge(P,'sobel');
fudgeFactor = 0.5;
BWs = edge(Q,'sobel',threshold * fudgeFactor);
figure, imshow(BWs)
se90 = strel('line',3,90);
se0 = strel('line',3,0);

BWs = imdilate(BWs,[se90 se0]);
imshow(BWs)
title('Dilated Gradient Mask')
BWs = imfill(BWs,'holes');
figure, imshow(BWs)

Qb = activecontour(BWs, mask, 500, 'Chan-Vese');
figure, imshow(Qb)