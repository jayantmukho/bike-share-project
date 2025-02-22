# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Example code for TensorFlow Wide & Deep Tutorial using TF.Learn API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import shutil
import sys

import tensorflow as tf

_CSV_COLUMNS = [
        'station_distance', 'mean_humidity', 'mean_visibility_miles',
        'mean_wind_speed_mph', 'precipitation_inches', 'cloud_cover', 'events',
        'day_week', 'start_time', 'mean_temp', 'duration'

]

_CSV_COLUMN_DEFAULTS = [[0.0], [0], [0], [0], [0.0], [0], [0], [''], [0.0], [0], [0]]

parser = argparse.ArgumentParser()

parser.add_argument(
    '--model_dir', type=str, default='model',
    help='Base directory for the model.')

parser.add_argument(
    '--model_type', type=str, default='deep',
    help="Valid model types: {'wide', 'deep', 'wide_deep'}.")

parser.add_argument(
    '--train_epochs', type=int, default=100, help='Number of training epochs.')

parser.add_argument(
    '--epochs_per_eval', type=int, default=2,
    help='The number of training epochs to run between evaluations.')

parser.add_argument(
    '--batch_size', type=int, default=40, help='Number of examples per batch.')

parser.add_argument(
    '--train_data', type=str, default='nnData_undersample.csv',
    help='Path to the training data.')

parser.add_argument(
    '--test_data', type=str, default='nnTestSet.csv',
    help='Path to the test data.')

_NUM_EXAMPLES = {
    'train': 289786,
    'validation': 10000,
}


def build_model_columns():
  """Builds a set of wide and deep feature columns."""
  # Continuous columns
  station_dist = tf.feature_column.numeric_column('station_distance')
  humidity = tf.feature_column.numeric_column('mean_humidity')
  visibility = tf.feature_column.numeric_column('mean_visibility_miles')
  wind = tf.feature_column.numeric_column('mean_wind_speed_mph')
  precip = tf.feature_column.numeric_column('precipitation_inches')
  cloud = tf.feature_column.numeric_column('cloud_cover')
  events = tf.feature_column.numeric_column('events')
  start_time = tf.feature_column.numeric_column('start_time')
  temp = tf.feature_column.numeric_column('mean_temp')
  
  day_week = tf.feature_column.categorical_column_with_vocabulary_list(
      'day_week', [
          'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])


  # Wide columns and deep columns.

  deep_columns = [
      station_dist,
      humidity ,
      visibility,
      wind,
      precip,
      cloud,
      events,
      start_time,
      temp,
      tf.feature_column.indicator_column(day_week),
  ]

  return deep_columns


def build_estimator(model_dir, model_type):
  """Build an estimator appropriate for the given model type."""
  deep_columns = build_model_columns()
  hidden_units = [500,400,300,100]
  
  # Create a tf.estimator.RunConfig to ensure the model is run on CPU, which
  # trains faster than GPU for this model.
  run_config = tf.estimator.RunConfig().replace(
      session_config=tf.ConfigProto(device_count={'GPU': 0}))

  if model_type == 'wide':
    return tf.estimator.LinearClassifier(
        model_dir=model_dir,
        feature_columns=wide_columns,
        config=run_config)
  elif model_type == 'deep':
    return tf.estimator.DNNClassifier(
        model_dir=model_dir,
        n_classes = 11,
        feature_columns=deep_columns,
        hidden_units=hidden_units,
        config=run_config)
  else:
    return tf.estimator.DNNLinearCombinedClassifier(
        model_dir=model_dir,
        linear_feature_columns=wide_columns,
        dnn_feature_columns=deep_columns,
        dnn_hidden_units=hidden_units,
        config=run_config)

    

def input_fn(data_file, num_epochs, shuffle, batch_size):
  """Generate an input function for the Estimator."""
  assert tf.gfile.Exists(data_file), (
      '%s not found. Please make sure you have either run data_download.py or '
      'set both arguments --train_data and --test_data.' % data_file)

  def parse_csv(value):
    print('Parsing', data_file)
    columns = tf.decode_csv(value, record_defaults=_CSV_COLUMN_DEFAULTS)
    features = dict(zip(_CSV_COLUMNS, columns))
    labels = features.pop('duration')
    return features, labels

  # Extract lines from input files using the Dataset API.
  dataset = tf.data.TextLineDataset(data_file)

  if shuffle:
    dataset = dataset.shuffle(buffer_size=_NUM_EXAMPLES['train'])

  dataset = dataset.map(parse_csv, num_parallel_calls=5)

  # We call repeat after shuffling, rather than before, to prevent separate
  # epochs from blending together.
  dataset = dataset.repeat(num_epochs)
  dataset = dataset.batch(batch_size)

  iterator = dataset.make_one_shot_iterator()
  features, labels = iterator.get_next()
  return features, labels


def main(unused_argv):
  # Clean up the model directory if present
  shutil.rmtree(FLAGS.model_dir, ignore_errors=True)
  model = build_estimator(FLAGS.model_dir, FLAGS.model_type)

  # Train and evaluate the model every `FLAGS.epochs_per_eval` epochs.
  for n in range(FLAGS.train_epochs // FLAGS.epochs_per_eval):
    model.train(input_fn=lambda: input_fn(
        FLAGS.train_data, FLAGS.epochs_per_eval, True, FLAGS.batch_size))

    results = model.evaluate(input_fn=lambda: input_fn(
        FLAGS.test_data, 1, False, FLAGS.batch_size))
       
    
    # Display evaluation metrics
    print('Results at epoch', (n + 1) * FLAGS.epochs_per_eval)
    print('-' * 60)
    
    
    
    # loss is mean squared error for regression, CE for classification
    for key in sorted(results):
      print('%s: %s' % (key, results[key]))
      


if __name__ == '__main__':
  tf.logging.set_verbosity(tf.logging.INFO)
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)