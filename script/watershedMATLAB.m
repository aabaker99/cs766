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
imshow(P)
%%

th =  graythresh(P)
%figure(2); imshowpair(P,im2bw(P,0.06),'montage');hold on;
figure; imshowpair(C,P,'montage'); hold on;
plot(rv(:,1),rv(:,2),'r*');

% impose the minima on nuclei centers so that watershed can work -- TODO
% mask = false(size(P));
% mask(uint8(rv)) = true;

%K = imimposemin(P,mask);
% figure;
% imshow(K);
%% Convert to binary image for watershed
temp = P;
Ppp =  im2bw(temp, graythresh(P));
figure; imshow(Ppp);
imwrite(double(Ppp), 'tempImage.tiff');
%% Compute distance transform

Q = -bwdist(~Ppp);
imshow(Q,[])

% compute watershed
Ld = watershed(Q);
figure; imshow(label2rgb(Ld))

Ppp2 = Ppp;
Ppp2(Ld == 0) = 0;
figure; imshow(Ppp2)

% Watershed is known for oversegmenting. % Enforce minima
mask = imextendedmin(Q,1,8);
figure; imshowpair(Ppp, mask, 'blend')

% Now compute watershed again
Q2 = imimposemin(Q,mask);
Ld2 = watershed(Q2);%figure; imshow(label2rgb(Ld2))
Ppp3 = Ppp;
Ppp3(Ld2 == 0) = 0;
figure; imshow(Ppp3);
figure;
imshow(label2rgb(Ppp3))
%% Using cell centers do k means clustering
imshowpair(Ppp3, label2rgb(Ppp3),'montage')
