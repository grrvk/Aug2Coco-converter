## Converter 

Module to convert augmented data from zip file to Coco dataset.

## Run 

### Folder input
Run with convert_withZip function from aug2coco.main.     
Load data from zip folder with images and coco.json file, which contains blocks data.

```python
from aug2coco.main import convert_withZip
from aug2coco.settings import setConvSettings

settings = setConvSettings(working_dir='LOAD_FROM_PATH', 
                           split_type='train/val', 
                           split_rate='0.6/0.4')
convert_withZip(settings)
```

Settings parameters for inputs from zip file:
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

### DataFrame input
Run with convert_withDf function from aug2coco.main.     
Load data from dataframe with data for blocks.

```python
from aug2coco.main import convert_withDf
from aug2coco.settings import setConvSettings

settings = setConvSettings(split_type='train/val', 
                           split_rate='0.6/0.4',
                           df_input=True)
convert_withDf(df, settings)
```

Settings parameters are similar to settings necessary for convert_withZip, however some changes:
* working_dir is not necessary - function loads data from DataFrame
* upload is not necessary 
* return_path [Optional] - default name if unset is 'df_generated'
* df_input - parameter **must** be set to True to set loading from df

     

