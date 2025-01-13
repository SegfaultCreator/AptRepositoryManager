import os

import ModificationTimeComparison as TimeComp

def updateRepository(package_dirs, package_build_dir, repository_dir):
    anyChangesMade = copy_any_new_package_to_repository(package_dirs, package_build_dir, repository_dir)

    if anyChangesMade:
        create_Packages_gz(package_dirs, package_build_dir, repository_dir)

def copy_any_new_package_to_repository(package_dirs, package_build_dir, repository_dir):
    anyChangesMade = False

    for package_name in package_dirs:
        deb_file_build = os.path.join(package_build_dir, package_name, package_name + ".deb")
        deb_file_repository = os.path.join(repository_dir, package_name + ".deb")

        if(package_needs_to_be_copied(deb_file_build, deb_file_repository)):
            print(f'Copying {deb_file_build} to {deb_file_repository} ... ')
            os.system(f'cp {deb_file_build} {deb_file_repository}')  
            print("Done")

            anyChangesMade = True
    
    return anyChangesMade

def package_needs_to_be_copied(deb_file_build, deb_file_repository):
    if(os.path.exists(deb_file_repository)):
        file_in_build_folder_is_newer = os.path.getmtime(deb_file_build) > os.path.getmtime(deb_file_repository)
        if(not file_in_build_folder_is_newer):
            return False

    return True

def create_Packages_gz(package_dirs, package_build_dir, repository_dir):
    packages_gz_for_repository = os.path.join(repository_dir, "Packages.gz")

    with open(packages_gz_for_repository, "w") as packages_gz_file:
        for package_name in package_dirs:
            packages_gz_for_pkg = os.path.join(package_build_dir, package_name, "Packages.gz")
            if(os.path.isfile(packages_gz_for_pkg)):
                with open(packages_gz_for_pkg, "r") as infile:
                        packages_gz_file.write(infile.read())
                        packages_gz_file.write("\n")  # Add a newline between files for separation

    print("Created Packages GZ")