# EPIC-KITCHENS VISOR Semi-Supervised Video Object Segmentation Challenge

This repository contains the code and steps to participate in [EPIC-KITCHENS VISOR Semi-Supervised Video Object Segmentation Challenge](https://codalab.lisn.upsaclay.fr/competitions/9767). It contains the steps to get the baseline results and converting them into the required sumbission format.
<br>

## EPIC-KITCHENS VISOR Semi-Supervised VOS on Codalab platform
To participate and submit to this VISOR Semi-Supervised VOS challenge, register at the [VISOR Semi-Supervised VOS Challenge](https://codalab.lisn.upsaclay.fr/competitions/9767)

## Data Download
Please Go to the download section of [EPIC-KITCHENS VISOR](https://epic-kitchens.github.io/VISOR/) official webpage to download the whole dataset, providing RGB frames for train/val/test and masks for train/val splits. If you are interested in our data generation pipeline, please also check our [VISOR paper](https://arxiv.org/abs/2209.13064). 

#### VISOR to DAVIS-like format
Since most methods follow [DAVIS](https://davischallenge.org/) format, we provide a script to convert our dataset to DAVIS style easily. Please refer to [VISOR to DAVIS-like](https://github.com/epic-kitchens/VISOR-VOS#visor-to-davis-like-format) for the needed steps and the conversion script.


#### Dataset Structure
Once the dataset is converted to DAVIS-like format, the dataset structure would be as follows:
```

|- VISOR_2022
  |- JPEGImages
  |- Annotations
  |- ImageSets
     |- 2022
        |- train.txt
        |- val.txt
        |- val_unseen.txt
```
Where `val.txt` contains the set of seqeunces that belongs to the validation split and `val_unseen.txt` contains the subset of the validation split for the unseen kitchens.

## Baseline and Evaluation
We use the official [DAVIS evaluation code](https://github.com/davisvideochallenge/davis2017-evaluation) in our benchmark, we adjusted the code to include the last frame of each sequence as part of the final score.

Moreover, we used [STM](https://github.com/seoungwugoh/STM) as a baseline for this challange, please refer to [STM inference and evaluation](https://github.com/epic-kitchens/VISOR-VOS#evaluation) for the details on how to evaluate on the baseline with the provided weights.

## Codalab Evaluation
If you want to participate and evaluate on our [Codalab](https://codalab.lisn.upsaclay.fr/competitions/9767). Then you can use `pngs_to_visor.py` script that would convert the PNGs prediction into VISOR-like JSON file, the script takes these arguments:
`masks_path`: path to where the PNGs(predictions) are stored, by default it's `../predictions`. They path sould follow this structure: 
```
|- masks_path
   |- P01_107_seq_xxxx
      |- P01_107_frame_xxxxxxxxxx.png
   |- PXX_XXX_seq_xxxx
      |- PXX_(X)XX_frame_xxxxxxxxxx.png
```

`mapping_file`: the mapping file of your data, this would be saved when you did [VISOR to DAVIS-like](https://github.com/epic-kitchens/VISOR-VOS#visor-to-davis-like-format) step. by default it's `../VISOR_2022/val_data_mapping.json`<br>
`out_json_name`: the file name of the output JSON. by default it's `val.json`<br>

Once the `val.json`, you can compress it by 'zip -j val.zip val.json'.

## Acknowledgement

When use this repo, any of our models or dataset, you need to cite the VISOR paper

## Citing VISOR
```
@inproceedings{VISOR2022,
  title = {EPIC-KITCHENS VISOR Benchmark: VIdeo Segmentations and Object Relations},
  author = {Darkhalil, Ahmad and Shan, Dandan and Zhu, Bin and Ma, Jian and Kar, Amlan and Higgins, Richard and Fidler, Sanja and Fouhey, David and Damen, Dima},
  booktitle = {Proceedings of the Neural Information Processing Systems (NeurIPS) Track on Datasets and Benchmarks},
  year = {2022}
}
```


# License

The code is published under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License, found [here](https://creativecommons.org/licenses/by-nc-sa/4.0/).
