import os
import numpy as np
import shutil
import click
        
@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--n", type=click.INT, default=2, show_default=True, help="number of batches to split the folder into")
@click.option("--include_root_dir", type=click.BOOL, default=False, show_default=True, help="whether to include the top-level input directory in all batch directories")
def split_folder(path, output, n, include_root_dir):
    """Splits files in a folder into n batches, preserving the underlying folder structure (i.e. all items in every subfolder will be uniformly distributed among the batches)."""

    batch_paths = [os.path.join(output, str(i)) for i in range(n)]
    if include_root_dir:
        root_folder_name = os.path.basename(path)
        batch_paths = [os.path.join(path, root_folder_name) for path in batch_paths]

    if not os.path.isdir(path):
        exit("'path' is not a directory")

    for root, dirs, files in os.walk(path):
        print(root)
        file_choices = np.random.choice(range(n), size=(len(files)))

        for i in range(len(files)):
            file_output_path = os.path.join(batch_paths[file_choices[i]], os.path.relpath(root, path))

            if not os.path.isdir(file_output_path):
                os.makedirs(file_output_path)

            shutil.copyfile(os.path.join(root, files[i]), os.path.join(file_output_path, files[i]))


if __name__ == '__main__':
    split_folder()
