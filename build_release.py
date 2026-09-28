#!/usr/bin/env python3
"""
Automated Portfolio Multi-Project Release Bundler & Checksum Generator
Author: Haris Zafar
"""

import hashlib
import shutil
import tarfile
from pathlib import Path
from tabulate import tabulate

ROOT_DIR = Path(__file__).parent.resolve()
DIST_DIR = ROOT_DIR / "dist"

SOLVERS = [
    ("power-systems-newton-raphson-solver", "v1.0.0"),
    ("solar-pv-mppt-dynamic-solver", "v1.0.0"),
    ("bess-soc-dynamics-solver", "v1.0.0"),
    ("inverter-grid-control-solver", "v1.0.0")
]

EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv"}
EXCLUDE_EXTS = {".pyc", ".prof"}

def compute_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def create_release_archive(repo_folder, version):
    repo_path = ROOT_DIR / repo_folder
    if not repo_path.exists():
        return None

    archive_name = f"{repo_folder}-{version}.tar.gz"
    archive_path = DIST_DIR / archive_name

    def filter_files(tarinfo):
        path_parts = Path(tarinfo.name).parts
        if any(part in EXCLUDE_DIRS for part in path_parts):
            return None
        if Path(tarinfo.name).suffix in EXCLUDE_EXTS:
            return None
        return tarinfo

    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(repo_path, arcname=repo_folder, filter=filter_files)

    file_size_kb = archive_path.stat().st_size / 1024.0
    sha256_hash = compute_sha256(archive_path)

    return [repo_folder, version, f"{file_size_kb:.1f} KB", sha256_hash[:20] + "..."]

def main():
    print("==========================================================================")
    print(" STARTING PORTFOLIO RELEASE BUNDLING & SHA-256 MANIFEST GENERATION")
    print("==========================================================================")

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    summary = []
    for repo, ver in SOLVERS:
        print(f"Packaging distribution archive for: {repo} ({ver})...")
        res = create_release_archive(repo, ver)
        if res:
            summary.append(res)

    print("\n" + tabulate(summary, headers=["Repository Module", "Version", "Archive Size", "SHA-256 Checksum"], tablefmt="github"))
    print(f"\nRelease tarballs successfully created in: {DIST_DIR}")

if __name__ == "__main__":
    main()
