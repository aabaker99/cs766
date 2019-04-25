#!/usr/bin/env python
import sys, argparse
import os, os.path
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from sklearn.utils.fixes import signature

def plot_pr_curve(y_true, y_score, drug, outdir):
  precision, recall, _ = precision_recall_curve(y_true, y_score)

  # In matplotlib < 1.5, plt.fill_between does not have a 'step' argument
  #step_kwargs = ({'step': 'post'}
  #               if 'step' in signature(plt.fill_between).parameters
  #               else {})
  step_kwargs = {'step': 'post'}
  plt.step(recall, precision, color='b', alpha=0.2, where='post')
  plt.fill_between(recall, precision, alpha=0.2, color='b', **step_kwargs)

  plt.xlabel('Recall')
  plt.ylabel('Precision')
  plt.ylim([0.0, 1.05])
  plt.xlim([0.0, 1.0])
  average_precision = average_precision_score(y_true, y_score)
  plt.title('{}: Average Precision={:0.2f}'.format(drug, average_precision))
  ofp = os.path.join(outdir, 'drug_pr_curve.png')
  plt.savefig(ofp)
  return average_precision

def read_treatments(treatments_fp):
  """
  Map (plate, well) tuples to integer labels
  """
  rv = {}
  with open(treatments_fp, 'r') as fh:
    for line in fh:
      line = line.rstrip()
      plate, well, drug_id, drug_int = line.split(',')
      rv[(plate, well.upper())] = drug_int
  return rv
      

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--data', required=True)
  parser.add_argument('--treatments', required=True)
  parser.add_argument('--outdir', required=True)
  parser.add_argument('--seed')
  args = parser.parse_args()

  meta_to_label = read_treatments(args.treatments)

  df = pd.read_csv(args.data)
  n_row, n_col = df.shape
  X = np.array(df.iloc[:, 2:])
  y = np.zeros((n_row,)).astype('int')
  for i in range(n_row):
    meta_tpl = (str(df.iloc[i,0]), str(df.iloc[i,1]).upper())
    y[i] = meta_to_label[meta_tpl]

  # perform classification one by one: compare one treatment against untreated - {{
  label_set = set(y)
  label_set.remove(0)
  label_list = list(label_set)

  X_control = X[y == 0,:]
  y_control = y[y == 0]
  for i in range(len(label_list)):
    label = label_list[i]
    X_case = X[y == label]
    y_case = y[y == label]

    np.random.seed(args.seed)
    X_in = np.concatenate((X_control, X_case), axis=0)
    y_in = np.concatenate((y_control, y_case), axis=0)
    n_row_in = y_in.shape[0]
    y_in = y_in.reshape(n_row_in, 1)
    X_y_in = np.concatenate((X_in, y_in), axis=1)
    np.random.shuffle(X_y_in)
    X_in = X_y_in[:,:-1]
    y_in = X_y_in[:,-1]

    # TODO cross validation (currently does train and test on the whole dataset)

    clf = LogisticRegression(random_state=args.seed, solver='lbfgs')
    clf.fit(X_in, y_in)

    # n_obs x n_class
    probas = clf.predict_proba(X)
    # plot_pr_curve needs binary data
    y_true = np.copy(y_in)
    y_true[y_true != 0] = 1
    y_score = probas[:,1]
    average_precision = plot_pr_curve(y_true, y_score, label, args.outdir)
    print(average_precision)
  # }} - one by one classification

if __name__ == "__main__":
  main()
