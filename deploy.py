#!/usr/bin/env python3
"""
一键部署脚本：将当前 CV 目录推送到 GitHub Pages
用法：python deploy.py
"""

import subprocess
import sys
import getpass
from datetime import datetime
from urllib.parse import quote


REPO = "Jo-Nan/Jo-Nan.github.io"
BRANCH = "main"
USERNAME = "Jo-Nan"


def run(cmd_list, check=True):
    """执行命令（使用列表形式，避免 shell 注入/转义问题）"""
    result = subprocess.run(cmd_list, capture_output=True, text=True)
    if check and result.returncode != 0:
        # 打印错误时隐藏可能包含 token 的 URL
        stderr = result.stderr.replace(result.args[0] if isinstance(result.args, list) else "", "")
        print(f"❌ 命令失败: {' '.join(cmd_list[:3])}...")
        print(stderr)
        sys.exit(1)
    return result


def main():
    # 1. 检查是否有改动
    status = run(["git", "status", "--porcelain"]).stdout.strip()
    if not status:
        print("✅ 没有检测到任何改动，无需部署。")
        return

    # 2. 显示改动摘要
    print("📋 检测到以下改动：")
    print(status)
    print()

    # 3. 获取 commit message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    default_msg = f"Update homepage ({timestamp})"
    msg = input(f"请输入 commit 信息 (回车使用默认: {default_msg}): ").strip()
    if not msg:
        msg = default_msg

    # 4. 请求令牌
    token = input("请输入 GitHub Personal Access Token: ").strip()
    if not token:
        print("❌ 令牌不能为空")
        sys.exit(1)

    # 5. Git add + commit
    run(["git", "add", "-A"])
    run(["git", "commit", "-m", msg])
    print("✅ 已提交")

    # 6. 推送（使用 URL 编码的令牌，推送后恢复原 URL）
    encoded_token = quote(token, safe="")
    token_url = f"https://{USERNAME}:{encoded_token}@github.com/{REPO}.git"
    clean_url = f"https://github.com/{REPO}.git"

    try:
        run(["git", "remote", "set-url", "origin", token_url])
        run(["git", "push", "origin", BRANCH])
        print(f"🚀 部署成功！访问 https://jo-nan.github.io 查看")
    finally:
        # 无论成功失败，都清理令牌
        run(["git", "remote", "set-url", "origin", clean_url], check=False)


if __name__ == "__main__":
    main()
