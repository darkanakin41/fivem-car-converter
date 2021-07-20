import datetime
import os
import shutil
import subprocess

from __init__ import open_iv_exe, vehicles_folder, files_folder


def get_car_name_from_folder(folder, root):
    return folder.replace(root, "").split('\\')[1]


def open_rpf(file):
    # print(f'[OpenIV] Processing {file}')
    os.popen(f'"{open_iv_exe}" "{file}" -core.game:Five').readlines()


def is_folder_ignored(folder):
    folders_ignored = ['lang']
    ignored = False

    for folder_ignored in folders_ignored:
        if f"\\{folder_ignored}" in folder:
            ignored = True

    return ignored


def process_vehicle_rpf(root, file):
    car_name = get_car_name_from_folder(root, vehicles_folder)
    print(f'[{car_name}] Processing {file}')
    vehicle_folder = os.path.join(files_folder, car_name)
    vehicle_input_folder = os.path.join(vehicle_folder, 'input')
    vehicle_output_folder = os.path.join(vehicle_folder, car_name.lower().replace(' ', '-'))
    if not os.path.exists(vehicle_input_folder):
        os.makedirs(vehicle_input_folder)
    if not os.path.exists(vehicle_output_folder):
        os.makedirs(vehicle_output_folder)
    subprocess.call(f'explorer "{vehicle_input_folder}"', shell=True)
    open_rpf(os.path.join(root, file))


def extract_vehicle_data(folder):
    car_name = get_car_name_from_folder(folder, files_folder)
    print(f'[{car_name}] Extracting Data')
    subprocess.call(f'explorer "{os.path.join(folder, "input")}"', shell=True)
    for root, dirs, files in os.walk(folder):
        if not is_folder_ignored(root):
            for file in files:
                if file.endswith('.rpf'):
                    open_rpf(os.path.join(root, file))


def create_fivem_files(folder):
    car_name = get_car_name_from_folder(folder, files_folder)
    print(f'[{car_name}] Generating FiveM files')

    input_folder = os.path.join(folder, 'input')
    fivem_folder = os.path.join(folder, car_name.lower().replace(' ', '-'))

    data_folder = os.path.join(fivem_folder, 'data')
    stream_folder = os.path.join(fivem_folder, 'stream')

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    if not os.path.exists(stream_folder):
        os.makedirs(stream_folder)

    files_mapping = {
        '.meta': data_folder,
        '.ytd': stream_folder,
        '.yft': stream_folder,
    }

    for root, dirs, files in os.walk(input_folder):
        if not is_folder_ignored(root):
            for file in files:
                for extension in files_mapping:
                    if file.endswith(extension):
                        shutil.copyfile(os.path.join(root, file), os.path.join(files_mapping[extension], file))

    with open(os.path.join(fivem_folder, '__resource.lua'), "w") as f:
        f.writelines("resource_manifest_version '77731fab-63ca-442c-a67b-abc70f28dfa5'\n")
        f.write("\n")
        f.write("{\n")
        for file in os.listdir(data_folder):
            f.write(f"\t'data/{file}',\n")
        f.write("}\n")
        f.write("\n")
        for file in os.listdir(data_folder):
            data = generate_data_file(f"data/{file}")
            if data is not None:
                f.write(f"{data}\n")
        f.write("\n")

    with open(os.path.join(vehicles_folder, car_name, 'done.txt'), "w") as f:
        f.write(f"{datetime.datetime.now()}")


def generate_data_file(file):
    if file.endswith('contentunlocks.meta') or file.endswith('contentunlock.meta'):
        return f"data_file 'CONTENT_UNLOCKING_META_FILE' 'data/{file}'"
    if file.endswith('vehiclelayouts.meta') or file.endswith('vehiclelayout.meta'):
        return f"data_file 'VEHICLE_LAYOUTS_FILE' 'data/{file}'"
    if file.endswith('carvariations.meta') or file.endswith('carvariation.meta'):
        return f"data_file 'VEHICLE_VARIATION_FILE' 'data/{file}'"
    if file.endswith('carcols.meta') or file.endswith('carcol.meta'):
        return f"data_file 'CARCOLS_FILE' 'data/{file}'"
    if file.endswith('dlctext.meta'):
        return f"data_file 'DLC_TEXT_FILE' 'data/{file}'"
    if file.endswith('shop_vehicle.meta'):
        return f"data_file 'VEHICLE_SHOP_DLC_FILE' 'data/{file}'"
    if file.endswith('handling.meta'):
        return f"data_file 'HANDLING_FILE' 'data/{file}'"
    if file.endswith('vehicles.meta') or file.endswith('vehicle.meta'):
        return f"data_file 'VEHICLE_METADATA_FILE' 'data/{file}'"

    print(f"Unhandled file '{file}'")
    return None


def main():
    for root, dirs, files in os.walk(vehicles_folder):
        if root == vehicles_folder:
            continue
        car_name = get_car_name_from_folder(root, vehicles_folder)
        if os.path.exists(os.path.join(vehicles_folder, car_name, "done.txt")):
            continue
        for file in files:
            if file.endswith('.rpf'):
                process_vehicle_rpf(root, file)

    for folder in os.listdir(files_folder):
        car_folder = os.path.join(files_folder, folder)
        car_name = get_car_name_from_folder(car_folder, files_folder)
        if os.path.exists(os.path.join(vehicles_folder, car_name, "done.txt")):
            continue
        extract_vehicle_data(car_folder)
        create_fivem_files(car_folder)


if __name__ == '__main__':
    main()
