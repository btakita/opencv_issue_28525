from poethepoet_tasks import TaskCollection

tasks = TaskCollection()

tasks.add(
    "mkdir_include",
    task_config={
        "cmd": "mkdir -p ./include",
    },
)

tasks.add(
    "clear_include",
    task_config={
        "deps": ["mkdir_include"],
        "cmd": "rm -f ./include/*.so*",
    },
)

tasks.add(
    "link_libcublas_include",
    task_config={
        "deps": ["mkdir_include"],
        "cmd": """sh -c "ln -snf \\"$(readlink -f ./.venv/lib/python3.14/site-packages/nvidia/cublas/lib/libcublas.so.12)\\" ./include" $@""",
    },
)

tasks.add(
    "link_libcublasLt_include",
    task_config={
        "deps": ["mkdir_include"],
        "cmd": """sh -c "ln -snf \\"$(readlink -f ./.venv/lib/python3.14/site-packages/nvidia/cublas/lib/libcublasLt.so.12)\\" ./include" $@""",
    },
)

tasks.add(
    "link_libcuda_include",
    task_config={
        "deps": ["mkdir_include"],
        "cmd": """sh -c "ln -snf \\"$(find /usr -name 'libcuda.so*' 2>/dev/null | head -n1 | xargs readlink -f)\\" ./include/libcuda.so.1" $@""",
    },
)

tasks.add(
    "link_libcudart_include",
    task_config={
        "deps": ["mkdir_include"],
        "cmd": """sh -c "ln -snf \\"$(readlink -f ./.venv/lib/python3.14/site-packages/nvidia/cuda_runtime/lib/libcudart.so.12)\\" ./include" $@""",
    },
)

tasks.add(
    "link_libcufft_include",
    task_config={
        "deps": ["mkdir_include"],
        "cmd": """sh -c "ln -snf \\"$(readlink -f ./.venv/lib/python3.14/site-packages/nvidia/cufft/lib/libcufft.so.11)\\" ./include" $@""",
    },
)

tasks.add(
    "link_libnvcuvid_include",
    task_config={
        "deps": ["mkdir_include"],
        "cmd": """sh -c "ln -snf \\"$(find /usr -name 'libnvcuvid.so*' 2>/dev/null | head -n1 | readlink -f)\\" ./include" $@""",
    },
)

tasks.add(
    "link_opencv_include",
    task_config={
        "deps": ["mkdir_include"],
        "cmd": """bash -lc '
set -euo pipefail

SITE="./.venv/lib/python3.14/site-packages"

CANDIDATES=(
  "$SITE/cv2"
  "$SITE/opencv_contrib_python_headless.libs"
  "$SITE/opencv_contrib_python.libs"
  "$SITE/opencv_python_headless.libs"
  "$SITE/opencv_python.libs"
)

found=0
shopt -s nullglob

for LIBDIR in "${CANDIDATES[@]}"; do
  if [ -d "$LIBDIR" ]; then
    found=1
    for p in "$LIBDIR"/*.so*; do
      bn="$(basename "$p")"
      ln -snf "$(readlink -f "$p")" "./include/$bn"
    done
  fi
done

if [ "$found" -ne 1 ]; then
  echo "ERROR: No OpenCV shared objects found under site-packages." >&2
  echo "Looked for: ${CANDIDATES[*]} and $SITE/cv2/cv2*.so*" >&2
  exit 1
fi
'""",
    },
)

tasks.add(
    "link_include",
    task_config={
        "deps": [
            "clear_include",
            "link_libcublas_include",
            "link_libcublasLt_include",
            "link_libcuda_include",
            "link_libcudart_include",
            "link_libcufft_include",
            # "link_libnvcuvid_include",
            # "link_opencv_include",
        ],
        "cmd": """sh -c "echo Linking CUDA/OpenCV/FFmpeg shims into include directory completed successfully. Make sure that $(readlink -f ./include) is in LD_LIBRARY_PATH" $@""",
    },
)
