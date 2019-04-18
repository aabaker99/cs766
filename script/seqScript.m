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
P = imfuse(C, E,'blend','Scaling','joint');
figure(2); imshow(P);hold on;
%figure; imshowpair(C,P,'montage');
%pts = csvread('centers.csv');
plot(rv(:,1),rv(:,2),'r*');

%% Using cell centers do k means clustering
imwrite(P, 'tmp.tif', 'TIFF');
