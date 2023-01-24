import glob
import numpy as np
from PIL import Image
import time
import os
import json
import cv2 as cv
import json
from tqdm import tqdm
import argparse

def find_segments(binary_image):
    """
    find_segments converts a binary mask into it's polygons (segments)
    :param binary_image: a binary mask
    :return: list of polygons of the binary mask
    """ 
    polygons=[] # to save row polygons
    reshaped_polygons=[] # to save the formatted polygons to be saved
    #find the countours of the mask
    contours, hierarchy = cv.findContours(binary_image, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    #go through the countours
    for contour in contours:
        #if it's empty countour, add zero polygon
        if len(contour) == 0:
            ploygon = [[0.0, 0.0]]
        else:
            ploygon = contour
        #save the polgyon 
        polygons.append(np.array(ploygon, dtype=np.int32))
        
    # go through the segments to reshape them to save them in a proper format later on
    for polygon in polygons:
        polygon = polygon.reshape(polygon.shape[0],polygon.shape[2])
        reshaped_polygons.append(polygon.tolist())

    return reshaped_polygons
    
def sequence_of_pngs_to_visor(sequence_path, mapping):
    """
    sequence_of_pngs_to_json converts a sequence (folder) that contains set of png images into a VISOR-like format to be saved as a json
    :param sequence_path: a path where the sequence is located
    :param mapping: a dict of the mappings of the objects
    :return: list of visor-like style objects and as well as frame and mask stats of the processed sequence
    """ 
    objects_with_polygons= [] # to store all objects
    all_masks_count=0 # to count masks
    frame_count = 0 # to count frames
    sequence_frames= sorted(glob.glob(sequence_path + "/*.png")) # set all frames in the sequence
    for frame in sequence_frames:
        frame_data = {"image":{"image_path":"", "name":"","video":""},"annotations":[]} # to store relevent into of each object in that frame
        frame_info = np.array(Image.open(frame, 'r'))
        object_codes=np.unique(frame_info)
        
        #fill the relevent information into the frame data according to VISOR format
        frame_data["image"]["image_path"] = '_'.join(os.path.basename(sequence_path).split('_')[:2]) + '/'+os.path.basename(frame)
        frame_data["image"]["name"] = os.path.basename(frame)
        frame_data["image"]["subsequence"] = os.path.basename(sequence_path)
        frame_data["image"]["video"] = '_'.join(os.path.basename(sequence_path).split('_')[:2])
        objects = []
        #go through the object codes
        for object_code in object_codes:
            if object_code !=0: 
                all_masks_count+=1
                #keep the current object code only
                temp_frame_info=np.where(frame_info == object_code,frame_info,0)
                #find the polygons for the current object code
                segments = find_segments(temp_frame_info)
                #define VISOR-like dict and add the object info to it
                object_info = {"name":"","segments":[]}
                object_info["name"] = mapping[str(object_code)]
                object_info["segments"] = segments
                objects.append(object_info)
        #save all objects of the frame
        frame_data['annotations'] = objects

        #add the current frame to frame of the sequence
        objects_with_polygons.append(frame_data)

        frame_count +=1

    #return polgyons and some stats of the sequence
    return objects_with_polygons, frame_count, all_masks_count

def pngs_to_visor(masks_path, mapping_file,out_json_name):
    """
    pngs_to_visor converts a folder that contains set sequences into a VISOR-like format to be saved as a json
    :param masks_path: a path where the folder of masks is located
    :param mapping_file: a dict of the mappings of the objects
    """ 
    #get all sequences
    sequences = glob.glob(os.path.join(masks_path,"*"))
    #read the mappings
    json_file_handler = open(mapping_file)
    json_data_mapping = json.load(json_file_handler)
    #this is fixed for the currnt version of VISOR (0.1) so keep it fixed unless the version has changed
    all_json_data = {"info": {"Dataset Name": "VISOR","Challenge":"semi_supervised_vos","Version":"0.1","Resolution":"854x480", "Release Date":"Aug 2022", "URL": "https://epic-kitchens.github.io/VISOR", "Details": "This is a VISOR VOS submission file. All annotations must have 854x480 resolution"}, "video_annotations":[]}
    #count for frames and masks
    data_mask_count = 0
    data_frame_count = 0
    #go through all sequences
    for sequence in  tqdm(sequences):
        if os.path.isdir(sequence):
            #get plygon and VISOR-like data for the sequence
            sequence_polygons, sequence_frame_count, sequence_masks_count = sequence_of_pngs_to_visor(sequence,json_data_mapping[os.path.basename(sequence)])
            #add it into the list of data
            all_json_data['video_annotations'].append(sequence_polygons[0])
            #update frame and mask counts
            data_frame_count += sequence_frame_count
            data_mask_count += sequence_masks_count

    #display the stats
    print('Total number of frames is: ', data_frame_count) 
    print('Total number of masks is: ', data_mask_count)
    print('Done! saving the JSON file . . .')
    #save the final version of the JSON
    with open(out_json_name, 'w') as f:
        json.dump(all_json_data, f)

if __name__ == "__main__":
    def get_arguments():
        parser = argparse.ArgumentParser(description="parameters for VISOR to DAVIS conversion")
        parser.add_argument("-masks_path", type=str, help="path to where the PNGs(predictions) are stored", default='../predictions')
        parser.add_argument("-mapping_file", type=str, help="path where the mapping file of your data, this would be saved when you run visor_to_davis.py script", default='../VISOR_2022/val_data_mapping.json')
        parser.add_argument("-out_json_name", type=str, help="the file name of the output JSON",default='val.json')
        return parser.parse_args()
    args = get_arguments()
    masks_path = args.masks_path
    mapping_file = args.mapping_file
    out_json_name = args.out_json_name

    print('Converting PNGs into a JSON file:')
    pngs_to_visor(masks_path=masks_path,mapping_file=mapping_file,out_json_name=out_json_name)
    print('Done!')
