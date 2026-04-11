#!/bin/sh
set -e

case "$1" in
  single)
    exec python3 regulus_optuna_optimizer.py
    ;;
  sequential)
    exec python3 regulus_optuna_optimizer_sequential.py
    ;;
  *)
    echo "Usage: docker run <image> {single|sequential}"
    echo ""
    echo "  single       Single-moment model (redness × imminence × visibility × az_proximity)"
    echo "  sequential   Sequential morning-arc model (stageA × stageB)"
    exit 1
    ;;
esac
