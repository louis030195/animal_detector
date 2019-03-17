# WORK IN PROGRESS

The goal is to make a generic API which take a path, read and process videos and give as output for each video:
 - For each animal species:
    - Number of frames this species has been detected
    - At which frame this species has been detected
    - More infos incoming ... 

This API is supposed to be used in production in the forests in France by the government to detect wolves

<img src="docs/images/wolfy.png">

# Usage

```
python run.py [directory_that_contains_videos]
```