from pathlib import Path
from typing import Union

from pydantic_settings import BaseSettings, SettingsConfigDict

# Adding a new entry to `package_changes_list` requires determining
# the revision at which the package appears, is removed or has been
# renamed/replaced.  To find the revision number:
#
# 1) Look up the date of the commit for the package change,
#    - either in the package repo itself (say, when auc was deleted); or
#    - in the openwrt repo where the package swap occurred (firewall4
#      in include/target.mk is a good example of this one).
#
# 2) Use 'scripts/getver.sh yyyy-mm-dd' in buildroot to get the revision.
#    See https://github.com/openwrt/openwrt/commit/e56845fae3c0
#
# Clients should interpret the table as follows:
#
#   rename/replace = if 'source' and 'target' both specified
#   added          = if only 'source' is specified
#   deleted        = if only 'target' is specified
#
# If 'mandatory' is true, this package must be added or deleted (probably
# because the default package list has changed).

package_changes_list = [
    {"source": "firewall", "target": "firewall4", "revision": 18611},
    {"source": "kmod-nft-nat6", "revision": 20282, "mandatory": True},
    {"source": "libustream-wolfssl", "target": "libustream-mbedtls", "revision": 21994},
    {"source": "px5g-wolfssl", "target": "px5g-mbedtls", "revision": 21994},
    {"source": "wpad-basic-wolfssl", "target": "wpad-basic-mbedtls", "revision": 21994},
    {"source": "luci-app-diag-core", "revision": 25984, "mandatory": True},
    {"source": "auc", "target": "owut", "revision": 26792},
    {
        "source": "luci-app-opkg",
        "target": "luci-app-package-manager",
        "revision": 27897,
    },
    {"source": "opkg", "target": "apk-mbedtls", "revision": 28056},
]


def package_changes(before=None):
    changes = []
    for change in package_changes_list:
        if before is None or change["revision"] <= before:
            changes.append(change)
    return changes


def release(branch_off_rev, enabled=True):
    return {
        "path": "releases/{version}",
        "enabled": enabled,
        "snapshot": False,
        "path_packages": "DEPRECATED",
        "branch_off_rev": branch_off_rev,
        "package_changes": package_changes(branch_off_rev),
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    public_path: Path = Path.cwd() / "public"
    redis_url: str = "redis://localhost:6379"
    upstream_url: str = "https://downloads.openwrt.org"
    allow_defaults: bool = False
    async_queue: bool = True
    branches_file: Union[str, Path, None] = None
    max_custom_rootfs_size_mb: int = 1024
    max_defaults_length: int = 20480
    repository_allow_list: list = [
        "http://downloads.openwrt.org",
        "https://downloads.openwrt.org",
        "http://feed.libremesh.org",
        "https://feed.libremesh.org",
    ]
    base_container: str = "docker.io/agave0/openwrt-imagebuilder"
    container_socket_path: str = ""
    container_identity: str = ""
    branches: dict = {
        "SNAPSHOT": {
            "path": "snapshots",
            "enabled": True,
            "snapshot": True,
            "path_packages": "DEPRECATED",
            "package_changes": package_changes(),
            "versions": ["SNAPSHOT"],
        },
        "25.12": {
            "path": "releases/{version}",
            "enabled": True,
            "snapshot": True,
            "path_packages": "DEPRECATED",
            "branch_off_rev": 32295,
            "package_changes": package_changes(32295),
            "versions": ["25-12-SNAPSHOT"],
        },
        "24.10": {
            "path": "releases/{version}",
            "enabled": True,
            "snapshot": True,
            "path_packages": "DEPRECATED",
            "branch_off_rev": 27990,
            "package_changes": package_changes(27990),
            "versions": ["24.10.5", "24.10.4", "24.10-SNAPSHOT"],
        },
        "23.05": {
            "path": "releases/{version}",
            "enabled": True,
            "snapshot": True,
            "path_packages": "DEPRECATED",
            "branch_off_rev": 23069,
            "package_changes": package_changes(23069),
            "versions": ["23.05.6", "23.05.5", "23.05-SNAPSHOT"],
        },
        # "22.03": release(19160, enabled=False),
        # "21.02": release(15812, enabled=False),  # Enabled for now...
    }
    server_stats: str = ""
    log_level: str = "INFO"
    squid_cache: bool = False
    build_ttl: str = "3h"
    build_defaults_ttl: str = "30m"
    build_failure_ttl: str = "10m"
    max_pending_jobs: int = 200
    job_timeout: str = "10m"
    configs_allowed: list = [
        "CONFIG_VERSION_DIST",
        "CONFIG_VERSION_NUMBER",
        "CONFIG_TARGET_ROOTFS_TARGZ",
        # 'CONFIG_TARGET_ROOTFS_JFFS2',
        # 'CONFIG_TARGET_ROOTFS_SQUASHFS'
    ]
    file_host: str = "openwrt.mirror.garr.it/openwrt"
    allow_instruction_build_packages: bool = False
    allow_pull_container_images: bool = True


settings = Settings()
