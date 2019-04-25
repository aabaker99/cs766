function rv = cell_centers(infile, outfile)
  arr = imread(infile);
  thresh = graythresh(arr);
  if thresh == 0
    % then otsu's method failed, increase contrast
    arr = imadjust(arr);
    thresh = graythresh(arr);
  end
  bw = imbinarize(arr, thresh);
  [L, num] = bwlabel(bw);
  rv = zeros(num,2);
  stats = regionprops(L, 'centroid');
  for i=1:num
    stats_struct = stats(i);
    centroid = stats_struct.Centroid;
    rv(i,:) = centroid;
  end
  csvwrite(outfile, rv);
end
