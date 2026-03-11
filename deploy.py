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

    # 2. 检查是否有改动
    status = run(["git", "status", "--porcelain"]).stdout.strip()
    if not status:
        print("✅ 没有检测到任何改动，无需部署。")
        return

    # 3. 显示改动摘要
    print("📋 检测到以下改动：")
    print(status)
    print()

    # 4. 获取 commit message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    default_msg = f"Update homepage ({timestamp})"
    msg = input(f"请输入 commit 信息 (回车使用默认: {default_msg}): ").strip()
    if not msg:
        msg = default_msg

    # 5. Git add + commit
    run(["git", "add", "-A"])
    run(["git", "commit", "-m", msg])
    print("✅ 已提交")

    # 6. 推送（通过 SSH）
    run(["git", "push", "origin", BRANCH])
    print(f"🚀 部署成功！访问 https://jo-nan.github.io 查看")


if __name__ == "__main__":
    main()
