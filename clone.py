# clone.py
import os
from git import Repo

REPO_URL = "https://github.com/MohammadHeydari/Telecom-Events-Analysis.git"
LOCAL_REPO_PATH = "./repo"

def clone_repo():
    if os.path.exists(LOCAL_REPO_PATH):
        os.system(f"rm -rf {LOCAL_REPO_PATH}")

    print(f"Cloning {REPO_URL}...")
    Repo.clone_from(REPO_URL, LOCAL_REPO_PATH)
    print("Repository cloned!")

if __name__ == "__main__":
    clone_repo()