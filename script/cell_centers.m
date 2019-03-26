function rv = cell_centers(fp)
  arr = imread(fp);
  bw = imbinarize(arr);
  [L, num] = bwlabel(bw);
  rv = zeros(num);
  stats = regionprops(L, 'centroid');
  for i=1:num
    stats_struct = stats(i);
    centroid = stats_struct('centroid')
    rv(i) = centroid;
  end
end
