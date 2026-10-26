# 本项目更新 GitHub：Windows CMD 教程

本地目录：`D:\Discrete-Lattice-Information-Coding-GitHub`。
远端：[usst-micslab/Highly-Fault-Tolerant-Discrete-Lattice-Information-Coding](https://github.com/usst-micslab/Highly-Fault-Tolerant-Discrete-Lattice-Information-Coding)。

本目录已有 Git 历史，已关联正确远端，分支为 `main`。**不需要重新执行 `git init`、新建仓库或重复 `git remote add origin`。** 以下说明以后修改后如何更新，保留已有提交历史。

终端使用 **CMD（命令提示符）**。只复制代码框内的命令，不复制 `D:\...>` 等提示符。

## 1. 进入目录并核对远端

```bat
cd /d "D:\Discrete-Lattice-Information-Coding-GitHub"
git status -sb
git remote -v
```

CMD 跨盘符需要 `cd /d`。远端必须是上面这个项目，不是 DoBMark。地址不同时先核对，不要直接覆盖。

## 2. 暂存并检查上传清单

```bat
git add .
git --no-pager diff --cached --stat
git --no-pager diff --cached --name-only
```

`git add .` 只是暂存，尚未提交或上传。`--no-pager` 避免进入分页界面；若已经进入，按 `q` 退出。

可以上传 README、教程、依赖说明、`codec.py`、测试、原始 Python/Vue/Flask 源码和小型说明图片。不应出现：

- 模型权重，如 `encoder1.pth`、`decoder1.pth`，以及其他 checkpoint。
- 完整数据集、实验生成图像全集、结果与日志。
- `.local/` 中的本机环境、安装包、验证结果和私有说明。
- `node_modules/`、缓存、密钥或凭据。

论文标题图、Vue 的小型示例图片、logo 和图标属于保留资源。`.gitignore` 不会自动移除已经跟踪的大文件。若清单出现权重或隐私内容，先停下核对，不要删除 E 盘原件或强制推送。

## 3. 提交，再推送

确认清单正确后：

```bat
git commit -m "Update project documentation"
git push origin main
```

提交说明按实际改动调整。若出现 `nothing to commit`，先确认目录正确、文件已保存；不要制造空提交。已有本地提交未上传时，仍可执行推送。

如果当前代理正在运行，而且端口仍为 **7897**，最后一条可替换成：

```bat
git -c http.proxy=http://127.0.0.1:7897 push origin main
```

单次 `-c` 不改变全局 Git 代理。端口变化时用实际端口；没有开启代理时不要套用。浏览器要求授权时按提示完成，不要把 token 写进聊天、README 或远端 URL。

## 4. 核实是否完成

```bat
git status -sb
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

需要代理查询远端时：

```bat
git -c http.proxy=http://127.0.0.1:7897 ls-remote origin refs/heads/main
```

本地 `HEAD` 和远端 `main` 的完整提交编号相同，且没有待提交改动，表示当前已提交版本一致。刷新 GitHub，检查 README、标题图和源码可见，权重、数据和 `.local/` 不在仓库内。

`Everything up-to-date` 仅表示没有新的提交需要推送，不表示未保存、未提交的文件也上传了。

## 常见报错

- **Author identity unknown**：先设置 Git 提交身份，然后重新执行 `git commit`。只配置姓名邮箱、没有重新提交，不能解决推送问题。
- **src refspec main does not match any**：用 `git status -sb` 和 `git log -1 --oneline` 确认分支及提交是否存在，不要重新初始化本项目。
- **remote origin already exists**：本项目已有远端，不用重复添加；用 `git remote -v` 核对即可。
- **remote unpack failed / index-pack failed**：保留本地文件和提交，核对远端状态及具体错误；服务端临时异常可确认后重试。不要删 `.git` 或使用 `--force`。
- **远端有别人新增的提交**：先比较双方历史，不要强制覆盖。

如果再次需要设置本仓库身份，你之前提供的署名和邮箱可用以下命令配置；没有 `--global`，不会改其他项目：

```bat
git config --local user.name "usst-micslab"
git config --local user.email "usst-micslab@163.com"
git commit -m "Update project documentation"
```

## 运行和上传是两回事

已验证的是已有权重下、小样本、无攻击的编码和解码，不代表完整训练、抗屏摄实验或网页服务通过。参见 [验证记录](docs/VALIDATION.md) 和 [已知问题](docs/KNOWN_ISSUES.md)。本机运行命令放在不上传的 `.local/LOCAL_RUN_GUIDE_zh.md`。
