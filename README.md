# EPIC-KITCHENS VISOR Semi-Supervised Video Object Segmentation Challenge

This repository contains the code and steps to participate in [EPIC-KITCHENS VISOR Semi-Supervised Video Object Segmentation Challenge](https://codalab.lisn.upsaclay.fr/competitions/9767). It contains the steps to get the baseline results and converting them into the required sumbission format.
<br>

## EPIC-KITCHENS VISOR Semi-Supervised VOS on Codalab platform
To participate and submit to this VISOR Semi-Supervised VOS challenge, register at the [VISOR Semi-Supervised VOS Challenge](https://codalab.lisn.upsaclay.fr/competitions/9767)

## Data Download
Please Go to the download section of [EPIC-KITCHENS VISOR](https://epic-kitchens.github.io/VISOR/) official webpage to download the whole dataset, providing RGB frames for train/val/test and masks for train/val splits. If you are interested in our data generation pipeline, please also check our [VISOR paper](https://arxiv.org/abs/2209.13064). 

### VISOR to DAVIS-like format
Since most methods follow [DAVIS](https://davischallenge.org/) format, we provide a script to convert our dataset to DAVIS style easily. Please refer to [VISOR to DAVIS-like](https://github.com/epic-kitchens/VISOR-VOS#visor-to-davis-like-format) for the needed steps and the conversion script.


### Dataset Structure
Once the dataset is converted to DAVIS-like format, the dataset structure would be as follows:
```

|- VISOR_2022
  |- val_data_mapping.json
  |- train_data_mapping.json
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

Moreover, we used [STM](https://github.com/seoungwugoh/STM) as a baseline for this challange, please refer to [STM inference and evaluation](https://github.com/epic-kitchens/VISOR-VOS#evaluation) for the details on how to evaluate on the baseline with the provided [pre-trained weights](https://github.com/epic-kitchens/VISOR-VOS#download-pre-trained-models).

## Codalab Evaluation (validation set)
If you want to participate and evaluate on our [Codalab](https://codalab.lisn.upsaclay.fr/competitions/9767). Then you can use `pngs_to_visor.py` script that would convert the PNGs val prediction into VISOR-like JSON file, the script takes these arguments:
`masks_path`: path to where the PNGs(predictions) are stored, by default it's `../predictions`. They path sould follow this structure: 
```
|- masks_path
   |- P01_107_seq_xxxx
      |- P01_107_frame_xxxxxxxxxx.png
   |- PXX_XXX_seq_xxxx
      |- PXX_(X)XX_frame_xxxxxxxxxx.png
```

`mapping_file`: the mapping file of your data, this would be saved when you did [VISOR to DAVIS-like](https://github.com/epic-kitchens/C6-SemiVOS#visor-to-davis-like-format) step. by default it's `../VISOR_2022/val_data_mapping.json`<br>
`out_json_name`: the file name of the output JSON. by default it's `val.json`<br>

Once the `val.json`, you can compress it by running `zip -j val.zip val.json` command.


## Instructions to evaluate on the test set
We invite the highest-performing teams from the validation set to evaluate their methods on the VISOR test set. Since the annotations for the test set are not disclosed, we provide instructions on packaging your code and model into a Docker image. This enables us to evaluate your solution on our servers and provide you with the performance metrics on the test set.

A starter Dockerfile is provided with a basic environment. You are required to build it by customizing it with your specific Python packages and versions. Upon cloning the current repository, you will obtain the following file structure:
```
|- C6-SemiVOS
  |- Dockerfile
  |- codes
     |- your inference codes and model should be there
  |- requirements
     |- requirements.txt
```
By following these instructions, you can build and run the VISOR VOS Docker image, allowing you to evaluate the test set within the container.

1. Prepare your code and requirements:
   - Place your model and inference code in the `./codes` directory.
   - In `./requirements/requirements.txt` file, list all the Python packages required for your code, along with their version. For example: 
     ```
     numpy==1.19.5
     opencv-python==4.5.3
     # Add more packages as needed
     ```

2. Update the Dockerfile:
   - In the Dockerfile, update the first line to match your desired Python version. For example, if you want to use Python 3.8, modify the line to: `FROM python:3.8-slim-buster`.
   - The Dockerfile also includes some basic environments such as installing some essential tools such as libgl1-mesa-dev and libglib2.0-0 which are important to run OpenCV in most of the time.
   - In the last line of the Dockerfile, put the running command for your inference code (instead of the current dummy one) supposing that VISOR dataset is placed in `/app/data` path in the docker (will be loaded to that path in step 4 when we create the docker container). The output predictions should be stored in **`/app/data/results`**, this is critical since when we want to evaluate, we'll be checking  `/app/data/results` for evaluating your predictions. This an example inference run:
    ```
      CMD python Training-Code-of-STM/eval.py -g '0' -s test  -y 22 -p /app/codes/davis_weights/coco_lr_fix_skip_0_1_release_resnet50_400000_32_399999.pth -D /app/data/
     ```
     - **IMPORTANT NOTE**: Don't forget to run the inference on the **test** set rather than the validation set. The test sequences would be located in the same structure as the val set. This is what to expect when you put the parameters of the test set:
   ```
   |- VISOR_2022
     |- val_data_mapping.json
     |- train_data_mapping.json
     |- JPEGImages
           |- 480p
              |- all train,val and test sequences            
     |- Annotations
           |- 480p
              |- all train,val and test sequences         
     |- ImageSets
        |- 2022
           |- train.txt
           |- val.txt
           |- val_unseen.txt
           |- test.txt
      ```
   Where **test.txt** contains the sequences for the test set
     - **IMPORTANT NOTE**: Don't include any evaluation scripts in the inference code, keep as lightweight as generating output PNGs based on your latest model weights.
3. Build the Docker image:
   - Open a terminal or command prompt.
   - Change your current directory to the provided Docker directory
   - Build the Docker image using the following command:
     ```shell
     docker build -t visor_vos .
     ```
      where visor_vos is a sample name for the docker image, you can use any image name.
4. Export the Docker image: Once you have built the image, you can export it to a file using the docker save command. This command saves the image as a tar archive. Specify the repository you want to export. For example:
     ```shell
     docker save -o <output_file>.tar visor_vos
     ```
5. Upload the generated tar file and send a **link** to [uob-epic-kitchens@bristol.ac.uk](mailto:uob-epic-kitchens@bristol.ac.uk)  and CC [ahmad.darkhalil@bristol.ac.uk](mailto:ahmad.darkhalil@bristol.ac.uk)  using your **registrered Codalab** email. We'll reply to you with the test set performance.

7. [optional] Run the Docker container on the **validation set**: 
   If you'd like to use verify the docker on the validation dataset as a way to make sure that it's working proberly, it would be as **simple as changing the  `test.txt` to  `val.txt`**.
   - Change the last line in the Dockerfile to use the **val data instead of test** (as you have the GT for the val data). Then rebuild the docker image for the validation data (step 3) 
   - With the docker image successfully built, you can now run the container using the following command (I assume the image name is visor_vos):
     ```shell
     docker run --gpus all -it visor_vos -v /path/on/host/to/visor/dataset:/app/data
     ```
     If you figured out any problem, you can enter the docker with an interactive session by:
     ```shell
     docker run --gpus all -it visor_vos -v /path/on/host/to/visor/dataset:/app/data
     ```
      - The `-v` mount the data (VISOR root directory) from your machine to the countainer, this would be saved in `/app/data`, your code should read it from there.
      - The `--gpus all` flag ensures that the container can access all available GPUs on the host machine.
      - The `-it` flag enables an interactive terminal session within the container, allowing you to interact with it.
      - Once the container is running, you can execute your inference script. Make sure that the necessary data and configuration files are accessible within the container.
   - The results would be stored in your local mounted directory, i.e. the path of the provided dataset, then you can evlauate them using [evaluation code](https://github.com/epic-kitchens/VISOR-VOS#evaluation)
   
As the result you'd have a image tar file to share with us, we're going to use it to run your code as the test set is private.


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
