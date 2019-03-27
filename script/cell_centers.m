function rv = cell_centers(infile, outfile)
  % todo switch to python
  arr = imread(infile);
  bw = imbinarize(arr);
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
