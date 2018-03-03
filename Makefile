.PHONY: up retrain

IMAGE_SIZE = 224
ARCHITECTURE = "mobilenet_0.50_${IMAGE_SIZE}"
PATH_TO_TRAIN = "tf_files/train-data"
PATH_TO_RESULTS = "tf_files/results"
up:
	docker run -it --rm -p 6006:6006 -p 8888:8888 -v /home/ta7ona/projects/traffic-sign/:/home/tensor-flow -w /home/tensor-flow gcr.io/tensorflow/tensorflow:latest-devel /bin/bash

retrain:
	python -m scripts.retrain \
  --bottleneck_dir=tf_files/results/bottlenecks \
  --how_many_training_steps=500 \
  --model_dir=${PATH_TO_RESULTS}/models/ \
  --summaries_dir=${PATH_TO_RESULTS}}/training_summaries/${ARCHITECTURE} \
  --output_graph=${PATH_TO_RESULTS}/retrained_graph.pb \
  --output_labels=${PATH_TO_RESULTS}/retrained_labels.txt \
  --architecture=${ARCHITECTURE} \
  --image_dir=${PATH_TO_TRAIN}
