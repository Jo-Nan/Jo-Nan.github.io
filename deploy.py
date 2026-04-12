#!/usr/bin/env python3
"""
一键部署脚本：将当前 CV 目录推送到 GitHub Pages（使用 SSH）
用法：python deploy.py
"""

import subprocess
import sys
from datetime import datetime


REPO = "Jo-Nan/Jo-Nan.github.io"
BRANCH = "main"
SSH_URL = f"git@github.com:{REPO}.git"
DEPLOY_PATHS = [
    "index.html",
    "style.css",
    "script.js",
    "CV.pdf",
    "cv-latex/cv.pdf",
    "assets",
    "paper",
]


def run(cmd_list, check=True):
    """执行命令"""
    result = subprocess.run(cmd_list, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ 命令失败: {' '.join(cmd_list)}")
        print(result.stderr)
        sys.exit(1)
    return result


def main():
    # 1. 确保 remote 使用 SSH URL
    run(["git", "remote", "set-url", "origin", SSH_URL], check=False)

    # 2. 检查是否有未推送提交
    ahead_result = run(["git", "rev-list", "--count", f"origin/{BRANCH}..HEAD"], check=False)
    ahead_count = 0
    if ahead_result.returncode == 0:
        try:
            ahead_count = int(ahead_result.stdout.strip() or "0")
        except ValueError:
            ahead_count = 0

    # 3. 仅检查部署范围内是否有改动
    status = run(["git", "status", "--porcelain", "--", *DEPLOY_PATHS]).stdout.strip()
    if not status and ahead_count == 0:
        print("✅ 网页、paper 与 CV PDF 没有改动，无需部署。")
        return

    # 4. 有新改动时，执行提交
    if status:
        print("📋 检测到以下可部署改动（网页 + paper + CV PDF）：")
        print(status)
        print()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        default_msg = f"Update homepage ({timestamp})"
        msg = input(f"请输入 commit 信息 (回车使用默认: {default_msg}): ").strip()
        if not msg:
            msg = default_msg

        run(["git", "add", "-A", "--", *DEPLOY_PATHS])
        staged = run(["git", "diff", "--cached", "--name-status", "--", *DEPLOY_PATHS]).stdout.strip()
        if staged:
            print("🧾 本次将提交：")
            print(staged)
            print()
            # 用 pathspec 限定 commit 范围，避免把其它已暂存文件一并提交
            run(["git", "commit", "-m", msg, "--", *DEPLOY_PATHS])
            print("✅ 已提交")
        elif ahead_count == 0:
            print("✅ 部署范围内没有可提交内容。")
            return

    # 5. 无新改动但有未推送提交时，直接推送
    if not status and ahead_count > 0:
        print(f"📦 检测到 {ahead_count} 个未推送提交，将直接推送。")

    # 6. 推送（通过 SSH）
    run(["git", "push", "origin", BRANCH])
    print(f"🚀 部署成功！访问 https://jo-nan.github.io 查看")


if __name__ == "__main__":
    main()
