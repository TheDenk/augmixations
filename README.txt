Some augmentation for object detection.  
Current augmentations:  
* cutmix

In progress:  
* mozaic  
* gridmask  

Getting Started
pip install augmixations

Example with default parameters

Import:  

```
from augmixations import cutmix  
```

Using:  

```
#bg_img - The image into which a rectangle will be inserted
```

```
#fg_img - The image from which a random rectangle will be cut 
```

```
img, boxes, labels = cutmix(bg_img, bg_boxes, bg_labels, fg_img, fg_boxes, fg_labels)  
```

Done.

 
  
  
