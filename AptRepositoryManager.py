import sys
import os
import ModificationTimeComparison as TimeComp
import PackageBuilding as PkgBuild
import RepositoryUpdater as RepoUpdater

# Main function to handle arguments and build packages

def check_if_package_requires_build(package_name, source_dir, destination_dir):
    folder_in_destination_dir = os.path.join(destination_dir, package_name)
    package_path = os.path.join(source_dir, package_name)

    if (os.path.isdir(folder_in_destination_dir)):
        if(TimeComp.is_newer(folder_in_destination_dir, package_path)):
            
            return False
    
    return True

def main():
    # Define paths
    source_dir = "Source"
    build_dir = "Build"
    repository_dir = "Repository"

    # Ensure the destination directory exists
    os.makedirs(build_dir, exist_ok=True)

    # List all subdirectories in the source directory
    package_dirs = [
        d
        for d in os.listdir(source_dir)
        if os.path.isdir(os.path.join(source_dir, d))
    ]

    if len(sys.argv) < 2:
        print("Usage: python3 build_packages.py --all | --new |<package1> <package2> ...")
        sys.exit(1)

    if sys.argv[1] == "--all":
        if(len(package_dirs) > 0):
            print("Building all packages...")
            PkgBuild.build_packages_in_parallel(package_dirs, source_dir, build_dir)
            
    elif sys.argv[1] == "--new":
        new_package_list = []
        for package_name in package_dirs:
            if(check_if_package_requires_build(package_name, source_dir, build_dir)):
                new_package_list.append(package_name)

        if(len(new_package_list) > 0):
            print(f"Building new packages: {' '.join(new_package_list)}")
            PkgBuild.build_packages_in_parallel(new_package_list, source_dir, build_dir)
            print("Completed Build")
        else:
            print("Everything up to date ...")
      
    else:
        package_names = sys.argv[1:]
        for package_name in package_names:
            if package_name in package_dirs:
                print(f"Building package {package_name} ...")
                PkgBuild.build_package_and_run_scanpackages(package_name, source_dir, build_dir)
            else:
                print(f"Package {package_name} not found in {source_dir}.")

    RepoUpdater.updateRepository(package_dirs, build_dir, repository_dir)

    print("Finished Repository Management")

if __name__ == "__main__":
    main()
