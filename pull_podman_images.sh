#!/bin/bash

OPENWRT_VERSION=${OPENWRT_VERSION:-24.10.0-rc5}
BASE_CONTAINER=${BASE_CONTAINER:-ghcr.io/openwrt/imagebuilder}

targets_all=($(curl -s "https://downloads.openwrt.org/releases/${OPENWRT_VERSION}/.targets.json" | sed 's|.*\"\(.*\)\"\:.*|\1|g' | tail -n +2 | head -n -1 | sort | sed 's|/|-|g'))
skip_targets=($(cat ./excluded_targets | sort | sed 's|/|-|g' ))

targets=()
for i in ${!targets_all[@]}; do 
	if printf '%s\0' "${skip_targets[@]}" | grep -Fxqz -- ${targets_all[$i]}; then echo "skip ${targets_all[$i]}" ; else targets+=(${targets_all[$i]}) ; fi
done

for i in ${!targets[@]}; do 
  echo "$(($i+1))/${#targets[@]} - Pulling ${targets[$i]} "
  
  IMAGE="${BASE_CONTAINER}:${targets[$i]}-v${OPENWRT_VERSION}"
  podman pull $IMAGE > /dev/null 2>&1
  
done
