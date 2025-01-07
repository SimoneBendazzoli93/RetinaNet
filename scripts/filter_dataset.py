import json
import sys
from pathlib import Path
import argparse



def main(dataset_file, filtered_dataset_file, total_segmentator=False, total_segmentator_pred_folder=None, total_segmentator_suffix=None):
    parser = argparse.ArgumentParser(description='Filter the dataset to remove empty boxes and update the paths of the instance segmentation and the total segmentator')
    parser.add_argument('--dataset-file', type=str, help='Path to the dataset file')
    parser.add_argument('--filtered-dataset-file', type=str, help='Path to the filtered dataset file')
    parser.add_argument('--total-segmentator', action='store_true', help='If Total Segmentator segmentation mask is included in the dataset')
    parser.add_argument('--total-segmentator-pred-folder', type=str, required=False, default=None, help='Path to the folder containing the Total Segmentator segmentation masks')
    parser.add_argument('--total-segmentator-suffix', required=False,default=None, type=str, help='Suffix of the Total Segmentator segmentation masks')
    
    args = parser.parse_args()
    remove_empty_boxes( args.dataset_file, args.filtered_dataset_file, args.total_segmentator, args.total_segmentator_pred_folder, args.total_segmentator_suffix)


def remove_empty_boxes(dataset_file, filtered_dataset_file,total_segmentator=False,total_segmentator_pred_folder=None, total_segmentator_suffix=None):
    filtered_dataset = {}
    with open(dataset_file) as f:
        dataset = json.load(f)

    for phase in dataset:
        filtered_dataset[phase] = []
        for data in dataset[phase]:
            boxes = data['box']
            if len(boxes) != 0 :
                filtered_dataset[phase].append(data)
            inst_seg_name = data['inst_seg']
            data['inst_seg'] = str(Path("..").joinpath("labelsInstTr",inst_seg_name.split("/")[-1])) # Path relative to the datadir/imagesTr/ folder
            if total_segmentator:
                data["seg"] = str(Path(total_segmentator_pred_folder).joinpath(inst_seg_name.split("/")[-1][:-len(".nii.gz")]+total_segmentator_suffix))
    with open(filtered_dataset_file, "w") as f:
        json.dump(filtered_dataset, f, indent=4)

if __name__ == "__main__":
    main()
    #True
    #"../../TotalSegmentator" Path relative to the datadir/imagesTr/ folder
    # "_TS_TOTAL.nii.gz"
