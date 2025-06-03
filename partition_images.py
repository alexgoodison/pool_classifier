from splitfolders import ratio
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser(description="Partitions an image dataset.")
    parser.add_argument("path", metavar="P", type=str, help="The path to the folder of images, e.g. downloads")
    parser.add_argument("train", metavar="T", type=float, help="The proportion of images for the training set, e.g. 0.8")
    parser.add_argument("val", metavar="V", type=float, help="The proportion of images for the validation set, e.g. 0.1")
    args = parser.parse_args()
    
    if args.train + args.val > 1.0:
        print("Training set size plus validation set size are too big")
    else:
        if args.train + args.val == 1.0:
            print("Warning: test set will be empty")
        ratio(args.path, output=".", seed=1337, ratio=(args.train, args.val, 1.0 - args.train - args.val), group_prefix=None)


