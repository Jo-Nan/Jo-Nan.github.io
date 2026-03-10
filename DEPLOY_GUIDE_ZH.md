# 部署 GitHub Pages 学术主页指南

这篇指南将教你如何将刚才生成的学术主页代码免费部署到 GitHub 上，使得任何人都可以通过域名访问你的主页。

## 第一步：准备 GitHub 仓库

1. 登录你的 [GitHub 账号](https://github.com/) 
2. 点击右上角的 `+` 号，选择 **New repository**
3. 在 **Repository name** 栏中，必须填写特定格式的仓库名：
   - 格式：`[你的用户名].github.io`
   - 例如，如果你的 GitHub 用户名是 `QiaoNan-Git`，那么仓库名**必须**是 `QiaoNan-Git.github.io`
4. 勾选 **Public** (公开)
5. 点击 **Create repository**

## 第二步：将代码推送到 GitHub

在你的电脑终端 (Terminal) 中，执行以下命令将代码上传：

```bash
# 进入你的代码目录
cd /Users/muzinan/NanMuZ/Code/cv

# 初始化 git 仓库 (如果还没初始化)
git init

# 将所有文件添加到追踪列表
git add .

# 提交代码
git commit -m "Initial commit: Add academic homepage"

# 关联你刚刚在 GitHub 上创建的仓库 (注意替换成你的用户名)
# 这里假设你的用户名是 QiaoNan-Git
git remote add origin https://github.com/QiaoNan-Git/QiaoNan-Git.github.io.git

# 将主分支从 master 改名为 main（可选，推荐）
git branch -M main

# 推送代码到远程仓库
git push -u origin main
```

## 第三步：等待部署并访问

1. 推送代码后，回到你的 GitHub 仓库页面
2. 点击顶部的 **Settings** 选项卡
3. 在左侧边栏找到 **Pages** 选项并点击
4. 在 **Build and deployment** 下，将 Source 设置为 `Deploy from a branch`。
5. 在 Branch 下，选择 `main` 分支，并将文件夹设置为 `/(root)`，然后点击 **Save**。
6. 等待约 1-3 分钟，页面顶部会显示一个通知你的站点已经部署，或者你可以直接在浏览器输入你的专属域名 `https://[你的用户名].github.io/` 查看效果。

### 部署后需要修改的地方 (个人定制)

在部署后或者部署前，你可能需要微调以下数据：
1. **替换照片**：把你自己的证件照重命名为 `profile.png` 然后覆盖掉项目里 `assets/profile.png`。
2. **替换地图 Tracker**：网站底部的 ClustrMaps 世界地图现在是占位符。你需要去 [ClustrMaps](https://clustrmaps.com/) 注册一个账号，输入你的网站地址，它会给你一段专属的 `<script>` 标签代码，把这段代码复制并替换掉 `index.html` 里第 346 行附近的占位 `<script>`。
3. **设置个人主页链接**：在 `index.html` 靠前的部分，更新真实的 Google Scholar 和 GitHub 链接。

**恭喜！你的专业学术主页现在上线了！**
