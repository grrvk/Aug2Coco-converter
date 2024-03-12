## Converter 

Module to convert augmented data from zip file to Coco dataset.

## Run 
Run with convert function in converter main.py folder.

```python
from data2coco.main import convert

convert(
  working_directory_path='LOAD_FROM',
  return_path='CONVERT_TO',
  split_type='train/val',
  split_rate='0.8/0.2',
  upload=True
)
```

Parameters:
* working_dir - path to zip with data to convert
* split_type - x or x/x or x/x/x where x in [train, val, test]
* split_rate - rates to split (x or x/x or x/x/x)
    * x is number from 0 to 1
    * must be in the same form as *split_type* (split type is x/x - split rate is x/x)
    * sum of numbers must be 1
* return_path [Optional] - path to folder with dataset to load to.
    * if unset - return_path is created in the same place as working_dir is with same name + '_CocoFormat' 
* upload [Optional] - default False, set ***True*** to upload data from working dir to already present Coco dataset 
    * If set True - *return_path* must be passed

     

