import argparse
import os

from python_research.experiments.band_selection_algorithms.icm.improved_class_map import \
    generate_pseudo_ground_truth_map
from python_research.experiments.band_selection_algorithms.icm.select_bands import select_bands


def arg_parser() -> argparse.Namespace:
    """
    Parse arguments for ICM band selection algorithm.

    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Arguments for ICM band selection algorithm.")
    parser.add_argument("--data_path", dest="data_path", type=str, help="Path to data.")
    parser.add_argument("--ref_map_path", dest="ref_map_path", type=str, help="Path to ground truth map.")
    parser.add_argument("--dest_path", dest="dest_path", type=str, help="Destination path.")
    parser.add_argument("--radius_size", dest="radius_size", type=int, default=5, help="Radius of the square window.")
    parser.add_argument("--training_patch", dest="training_patch", type=float, default=0.1,
                        help="Size of the training patch for SVM classifier.")
    parser.add_argument("--bands_num", dest="bands_num", type=int, help="Number of bands to select.")
    return parser.parse_args()


def main(args: argparse.Namespace):
    """
    Main method designed for running the ICM band selection algorithm.

    :param args Parsed arguments.
    :return: None.
    """
    os.makedirs(args.dest_path, exist_ok=True)
    generate_pseudo_ground_truth_map(args=args)
    select_bands(args=args)


if __name__ == "__main__":
    main(args=arg_parser())
