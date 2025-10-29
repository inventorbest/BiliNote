import os
import subprocess
from typing import List, Sequence, Tuple

from dotenv import load_dotenv

from app.utils.logger import get_logger
logger = get_logger(__name__)

load_dotenv()


FFMPEG_ENABLE_CUDA = os.getenv("FFMPEG_ENABLE_CUDA", "false").lower() in {"1", "true", "yes", "on"}
def check_ffmpeg_exists() -> bool:
    """
    检查 ffmpeg 是否可用。优先使用 FFMPEG_BIN_PATH 环境变量指定的路径。
    """
    ffmpeg_bin_path = os.getenv("FFMPEG_BIN_PATH")
    logger.info(f"FFMPEG_BIN_PATH: {ffmpeg_bin_path}")
    if ffmpeg_bin_path and os.path.isdir(ffmpeg_bin_path):
        os.environ["PATH"] = ffmpeg_bin_path + os.pathsep + os.environ.get("PATH", "")
        logger.info(f"ffmpeg 未配置路径，尝试使用系统路径PATH: {os.environ.get('PATH')}")
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        logger.info("ffmpeg 已安装")
        return True
    except (FileNotFoundError, OSError, subprocess.CalledProcessError):
        logger.info("ffmpeg 未安装")
        return False


def make_ffmpeg_command(args: Sequence[str], prefer_cuda: bool = True) -> Tuple[List[str], bool]:
    """Return an ffmpeg command list and whether CUDA hwaccel is included."""
    use_cuda = prefer_cuda and FFMPEG_ENABLE_CUDA
    if use_cuda:
        return ["ffmpeg", "-hwaccel", "cuda", *args], True
    return ["ffmpeg", *args], False


def ffmpeg_cuda_enabled() -> bool:
    """Expose whether CUDA acceleration is globally enabled via env."""
    return FFMPEG_ENABLE_CUDA


def ensure_ffmpeg_or_raise():
    """
    校验 ffmpeg 是否可用，否则抛出异常并提示安装方式。
    """
    if not check_ffmpeg_exists():
        logger.error("未检测到 ffmpeg，请先安装后再使用本功能。")
        raise EnvironmentError(
            " 未检测到 ffmpeg，请先安装后再使用本功能。\n"
            "👉 下载地址：https://ffmpeg.org/download.html\n"
            "🪟 Windows 推荐：https://www.gyan.dev/ffmpeg/builds/\n"
            "💡 如果你已安装，请将其路径写入 `.env` 文件，例如：\n"
            "FFMPEG_BIN_PATH=/your/custom/ffmpeg/bin"
        )