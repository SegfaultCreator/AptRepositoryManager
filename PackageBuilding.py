import os
import subprocess
import concurrent.futures

# Parallel building of multiple packages
def build_packages_in_parallel(package_list, source_dir, destination_dir):    
    # Use ProcessPoolExecutor for parallel execution
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit all tasks to the pool
        future_to_package = {executor.submit(build_package_and_run_scanpackages, pkg, source_dir, destination_dir): pkg for pkg in package_list}

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_package):
            package_name = future_to_package[future]
            try:
                future.result()  # Wait for the task to complete
            except Exception as e:
                print(f"Error building package {package_name}: {e}")

# Function to build a package and run scanpackages
def build_package_and_run_scanpackages(package_name, source_dir, destination_dir):
    source_path = os.path.join(source_dir, package_name)
        
    folder_in_destination_dir = os.path.join(destination_dir, package_name)
    os.makedirs(folder_in_destination_dir, exist_ok=True)
    
    package_file_name = package_name + ".deb"
    deb_output_path = os.path.join(folder_in_destination_dir, package_file_name)

    build_package(source_path, deb_output_path)
    
    run_scanpackages(folder_in_destination_dir, package_name)

def build_package(source_path, deb_output_path):
    try:
        subprocess.run(
        ["dpkg-deb", "--build", source_path, deb_output_path],
        check=True
    )
        print(f"Succesfully build Package {source_path} into: {deb_output_path}")

    except subprocess.CalledProcessError as e:
        print(f"Error building package {package_path}: {e}")

def run_scanpackages(folder_in_destination_dir, package_name):
    try:
        packages_file_name = open(os.path.join(folder_in_destination_dir, "Packages.gz"), "w")
        with packages_file_name as packages_file:
            subprocess.run(
                ["dpkg-scanpackages", "."],
                cwd = folder_in_destination_dir,
                stdout=packages_file,
                check=True
            )
        print(f"Succesfully created Packages.gz for {package_name}")

    except subprocess.CalledProcessError as e:
        print(f"Error Running dpkg-scanpackages on directory {folder_in_destination_dir}: {e}")

