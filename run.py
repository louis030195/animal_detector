from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Files stuff
import os
import sys
import shutil
from pathlib import Path

# Hack to use tensorflow/models/research/slim utils tools
sys.path.insert(0, './models/research/slim')


# Math / ML
import math
import numpy as np
import tensorflow as tf
from tensorflow.contrib import slim
from datasets import dataset_utils, imagenet
from nets import vgg
from preprocessing import vgg_preprocessing

# Misc
import argparse
import time
import cv2
import asyncio


url = "http://download.tensorflow.org/models/vgg_16_2016_08_28.tar.gz"

checkpoints_dir = '/tmp/checkpoints'

if not tf.gfile.Exists(checkpoints_dir):
    tf.gfile.MakeDirs(checkpoints_dir)
    dataset_utils.download_and_uncompress_tarball(url, checkpoints_dir)



async def process_image(image_path):
  image_size = vgg.vgg_16.default_image_size

  with tf.Graph().as_default():
      # Convert filepath string to string tensor
      #tf_filepath = tf.convert_to_tensor(image_path, dtype=tf.string)
      #tf_filepath = tf.convert_to_tensor(str(image_path), dtype=tf.string)
 
       # Read .JPEG image
      #tf_img_string = tf.read_file(tf_filepath)
      
      image = tf.image.decode_jpeg(tf.image.encode_jpeg(image_path), channels=3)
      tf_img_string = tf.read_file(str(image_path))
      image = tf.image.decode_jpeg(tf_img_string)#tf.image.encode_jpeg(tf_img_string), channels=3)

      processed_image = vgg_preprocessing.preprocess_image(image, image_size, image_size, is_training=False)
      processed_images  = tf.expand_dims(processed_image, 0)

      # Create the model, use the default arg scope to configure the batch norm parameters.
      with slim.arg_scope(vgg.vgg_arg_scope()):
          # 1000 classes instead of 1001.
          logits, _ = vgg.vgg_16(processed_images, num_classes=1000, is_training=False)
      probabilities = tf.nn.softmax(logits)

      init_fn = slim.assign_from_checkpoint_fn(
          os.path.join(checkpoints_dir, 'vgg_16.ckpt'),
          slim.get_model_variables('vgg_16'))

      with tf.Session() as sess:
          init_fn(sess)
          np_image, probabilities = sess.run([image, probabilities])
          probabilities = probabilities[0, 0:]
          sorted_inds = [i[0] for i in sorted(enumerate(-probabilities), key=lambda x:x[1])]

      names = imagenet.create_readable_names_for_imagenet_labels()
      animals_found = []
      for i in range(5):
          index = sorted_inds[i]
          # Shift the index of a class name by one. 
          # print('Probability %0.2f%% => [%s]' % (probabilities[index] * 100, names[index+1]))
          animals_found.append(names[index+1])
      return animals_found

async def find_animals(path):
  images = list(Path(path).rglob("*.[jJ][pP][gG]")) + list(Path(path).rglob("*.[pP][nN][gG]"))

  videos = list(Path(path).rglob("*.[aA][vV][iI]")) + list(Path(path).rglob("*.[mM][pP][4]"))
  #dir = 'img'
  #if os.path.exists(dir):
  #    shutil.rmtree(dir)
  #os.makedirs(dir)
  all_videos = {}
  all_images = {}
  for video in videos:
    print("Processing", str(video))
    vidcap = cv2.VideoCapture(str(video))
    success,image = vidcap.read()
    success = True
    frame_count = 0
    count_animal = {}
    while success:
      #cv2.imwrite("img/frame%d.jpg" % frame_count, image)     # save frame as JPEG file      
      #result = await process_image("img/frame%d.jpg" % count)
      result = await process_image(image)
      success,image = vidcap.read()
      for a in result:
        # If it's the first time we see this species in the dict
        if a not in count_animal:
          count_animal[a] = {}
          count_animal[a]['count'] = 0
          count_animal[a]['occurences'] = []
          
        # Increment the counter of times we saw this species
        count_animal[a]['count'] = count_animal[a]['count'] + 1
        
        # Set when we saw the species (at which frame in the video)
        count_animal[a]['occurences'].append(frame_count)
        
      frame_count += 1
    print("Found", count_animal)
    all_videos[video] = count_animal
  for image in images:
    print(image)
    try:
      result = await process_image(image)
    except:
      print('Failed')
    count_animal = {}
    for a in result:
        # If it's the first time we see this species in the dict
        if a not in count_animal:
          count_animal[a] = {}
          count_animal[a]['count'] = 0
          # Increment the counter of times we saw this species
        count_animal[a]['count'] = count_animal[a]['count'] + 1
    print("Found", count_animal)
    all_images[image] = count_animal
  print(all_videos)
print(all_images)
parser = argparse.ArgumentParser(description='Animal detector.')
parser.add_argument('path', type=str,
                   help='path to process videos',
                   default='.')

args = parser.parse_args()

loop = asyncio.new_event_loop()
loop.run_until_complete(find_animals(args.path))
