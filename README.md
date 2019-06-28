# WORK IN PROGRESS

The aim of this project is to make an extension of GCP CV tools with many parameters, easy installable and runnable in production as an API

**Output example of processing a video**

occurences is at which frame the animal is detected
>'white wolf, Arctic wolf, Canis lupus tundrarum': {'count': 33, 'occurences': [189, 190, 191, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 222, 223, 224, 225, 226, 227]

# Installation

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

If you want to run on GPU, you also need everything installed to handle [CUDA](https://www.tensorflow.org/install/gpu)

# Usage

```
python run.py [directory_that_contains_videos_and_photos]
```

# Roadmap
- [] Use Tensorflow serving / Pytorch serving ...
- [] Easy production setup (Docker ...)
- [] Option that store results in a database + setup API to query the database
- [] Web / mobile interface for the option above
- [] Offer production-ready custom models (pretrained on ImageNet + fine-tuned)