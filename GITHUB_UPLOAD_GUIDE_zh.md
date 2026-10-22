# 本项目上传 GitHub：Windows CMD 教程

整理目录：`D:\Discrete-Lattice-Information-Coding-GitHub`。

下面使用你前面操作过的 **CMD（命令提示符）**。只复制代码框里的命令，不复制 `D:\...>` 等提示符。本文只是操作说明；整理过程没有替你创建远端仓库、提交或推送。

## 1. 进入正确的目录

```bat
cd /d "D:\Discrete-Lattice-Information-Coding-GitHub"
git --version
```

CMD 中跨盘符必须用 `cd /d`。单独 `cd D:\...` 可能仍停留在 C 盘。

## 2. 初始化并检查上传清单

本次整理没有在这个文件夹里初始化 Git。首次上传时执行：

```bat
git init -b main
git add .
git --no-pager diff --cached --stat
git --no-pager diff --cached --name-only
```

如果你已经初始化过，就不必重复 `git init`。`--no-pager` 可以避免进入前面遇到的分页浏览界面；如果已经进入，按 `q` 退出。

清单里应当是 README、教程、依赖说明、`codec.py`、测试、原始 Python/Vue/Flask 源码和小型说明图片。

以下内容不应出现：

- `encoder1.pth`、`decoder1.pth` 等模型权重。
- 数据集、实验输出和日志。
- `.local/` 内的验证环境、安装包、运行结果和本机说明。
- `node_modules/`、缓存、IDE 配置、密钥或凭据。

`assets/paper_header.png`、Vue 的小型示例图片、logo 和图标需要保留，不是待排除的大型实验结果。`.gitignore` 只阻止未跟踪文件进入 Git；已经跟踪的大文件不会因此自动退出。若发现这类文件，先停下核对，不要删除原始权重或强制推送。

## 3. 设置本仓库的作者身份，再提交

将下面的 `YOUR_NAME` 和 `YOUR_EMAIL` 替换为你的 Git 提交署名、邮箱。可以使用 GitHub 账户中显示的隐私邮箱，但不要把示例占位符当作真实身份。

```bat
git config --local user.name "YOUR_NAME"
git config --local user.email "YOUR_EMAIL"
git commit -m "Prepare discrete lattice coding lab code for release"
```

这里没有 `--global`，因此不会修改其他项目的 Git 身份。如果之前提示 `Author identity unknown`，配置后重新执行 `git commit` 即可，不需要重新整理文件。

## 4. 在 GitHub 创建空仓库

登录 GitHub，选择 **New repository**。仓库名可用 `Discrete-Lattice-Information-Coding`，账号或组织按你实际要发布的位置选择。确认实验室允许公开后再选 Public；授权未确认时先用 Private。

创建时不要勾选添加 README、`.gitignore` 或 License，因为本地已经有文档，且原代码没有提供可直接套用的项目许可证。

复制新仓库的 HTTPS 地址。下面的 `OWNER` 是你实际选择的账号/组织，`REPOSITORY` 是实际仓库名，**整条地址必须换成你刚创建的仓库地址**：

```bat
git remote add origin https://github.com/OWNER/REPOSITORY.git
git remote -v
git push -u origin main
```

核对 `git remote -v` 指向的是本项目，不是前一个 DoBMark 项目。若提示 `remote origin already exists`，先查看现有地址，不要盲目删除或覆盖。浏览器出现登录授权时，按浏览器提示完成；不要在聊天、README 或远端 URL 中填写 token。

## 5. 网络不通时：仅本次命令使用代理

你上一个项目使用过 `127.0.0.1:7897`。**只有当前代理仍在运行、端口也仍为 7897 时**，才用：

```bat
git -c http.proxy=http://127.0.0.1:7897 push -u origin main
```

它只影响这一条 Git 命令，不改变全局代理设置。端口变了就改成软件当前显示的端口；没有开启代理时不要套用这条命令。

## 6. 怎么判断上传完成

推送成功后，刷新 GitHub 仓库，确认能看到本项目的 README、论文标题图片、`codec.py` 和 `train code/` 源码，而没有权重和数据。

可以再执行：

```bat
git status -sb
git log -1 --oneline
git ls-remote origin refs/heads/main
```

最后一条显示的远端提交应与本地最新提交一致。需要代理时可同样在 `git` 后加 `-c http.proxy=http://127.0.0.1:7897`。`Everything up-to-date` 表示当前分支没有待推送的新提交，不等于电脑里所有未提交修改都上传了；还要看 `git status`。

若再次遇到前面的 `remote unpack failed` / `index-pack failed`，先保留本地文件和提交，检查远端状态后再重试。不要用 `--force`，也不需要删掉 `.git` 重新来。其他拒绝信息应按实际错误处理。

## 7. 以后更新这个项目

已关联正确远端、分支为 `main` 时：

```bat
cd /d "D:\Discrete-Lattice-Information-Coding-GitHub"
git status --short
git add .
git --no-pager diff --cached --stat
git --no-pager diff --cached --name-only
git commit -m "Update project documentation"
git push
```

提交说明按实际修改调整。如果网络需要前述代理，最后一条改为同样的单次代理推送命令。提示 `nothing to commit` 时，先确认文件已保存、目录正确；不要为了推送制造空提交。

## 运行与上传是两件事

本项目已经验证的是已有权重下的小样本数字图像编码、解码，不代表完整训练、抗屏摄实验或网页服务已经通过。具体见 `docs/VALIDATION.md` 和 `docs/KNOWN_ISSUES.md`。本机直接运行方法放在不上传的 `.local/LOCAL_RUN_GUIDE_zh.md`。
