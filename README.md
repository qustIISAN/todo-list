# Todo & Pomodoro Desktop Widget Demo

This project is a minimal demo for a desktop-style widget that combines a Pomodoro timer with a checklist-style todo list.
It uses a small FastAPI backend (Python) and a Vite + React front-end (TypeScript). The two services run side-by-side during
development, and you can now bundle them inside a Python + WebView desktop window to get a more realistic widget experience.

> 💡 **我完全是小白，如何开始？** 现在有一个一键脚本，只要在 Windows 上双击即可完成环境安装并启动前后端。

## 0. Windows 一键启动（推荐）

如果你使用的是 Windows，可以直接双击仓库根目录下的 `run_demo.bat`：

1. 第一次运行脚本时会自动创建 Python 虚拟环境、安装后端依赖，并执行 `npm install` 下载前端依赖。
2. 安装完成后脚本会自动打开两个新的命令提示符窗口：一个运行 FastAPI 后端 (`http://127.0.0.1:8000`)，另一个运行 Vite 前端 (`http://127.0.0.1:5173`)。
3. 当两个窗口都显示运行成功后，直接在浏览器访问 `http://127.0.0.1:5173/` 即可看到番茄钟 + 待办组件。
4. 如果想要停止服务，只需在这两个新窗口中分别按下 `Ctrl + C`，或者直接关闭窗口。

> 📌 脚本会检查你的系统是否安装了 **Python 3.10+** 与 **Node.js 18+**。如果缺失，它会在命令行提示你去官网下载。

即使使用脚本，也推荐继续阅读下面的内容，了解项目结构以及在 macOS / Linux 上如何手动运行。

## 1. 准备工作（所有平台）

在开始之前，请先确认你的电脑已经安装了：

1. **Python 3.10+** – 可以在终端/命令提示符输入 `python --version` 查看。
2. **Node.js 18+ 和 npm** – 通过 `node --version` 和 `npm --version` 检查。如果没有，去 [nodejs.org](https://nodejs.org/) 下载 LTS 版本即可。

如果你之前没有使用过命令行，可以记住以下几点：
- Windows 用户可以使用 **PowerShell** 或者 **命令提示符 (cmd)**。
- macOS / Linux 用户使用系统自带的 **Terminal (终端)**。
- 每一条命令都需要按回车键执行。

## 2. 项目结构说明

```
.
├── backend/              # FastAPI 服务：处理番茄钟和待办逻辑
│   ├── app/
│   │   ├── main.py       # FastAPI 应用入口
│   │   ├── models.py     # Pydantic 数据模型
│   │   └── services.py   # 内存版的业务逻辑实现
│   └── requirements.txt  # 后端依赖列表
├── desktop/              # 使用 PyWebView 打包的桌面窗口启动器
│   ├── launch_widget.py  # 启动后端并打开原生窗口
│   └── requirements.txt  # 桌面模式需要的额外依赖
├── frontend/             # Vite + React 前端：展示界面并调用 API
│   ├── index.html
│   ├── package.json      # 前端依赖与脚本
│   └── src/
│       ├── App.tsx       # React 主组件
│       └── main.tsx      # 应用入口
└── README.md
```

## 3. 启动后端（FastAPI）

1. 打开一个终端窗口，进入项目的 `backend` 目录。
   ```bash
   cd backend
   ```
2. 创建并激活虚拟环境：
   ```bash
   python -m venv .venv
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   # Windows cmd
   .\.venv\Scripts\activate.bat
   # macOS / Linux
   source .venv/bin/activate
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
4. 运行开发服务器：
   ```bash
   uvicorn app.main:app --reload
   ```
5. 成功的话，你会在终端看到 `Uvicorn running on http://127.0.0.1:8000` 的提示。保持该终端窗口不要关闭。
6. 在浏览器访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 可以查看和测试 API。

## 4. 启动前端（Vite + React）

1. 再打开一个新的终端窗口，进入 `frontend` 目录：
   ```bash
   cd frontend
   ```
2. 安装依赖（第一次运行必须执行）：
   ```bash
   npm install
   ```
3. 启动前端开发服务器：
   ```bash
   npm run dev
   ```
4. 终端会显示一个访问地址（默认是 `http://127.0.0.1:5173/` 或 `http://localhost:5173/`）。
5. 在浏览器中打开这个地址，就能看到番茄钟 + 待办的小组件界面。前端会自动请求刚才启动的 FastAPI 后端。

### ✅ 如何自定义番茄钟时间？

界面中的 **Settings** 区块允许你直接输入专注、短休息、长休息的分钟数。填写完毕后点击 **Save settings**，后端会立即更新配置。
如果此时番茄钟正在运行，它会立刻按照新的设置重新计算剩余时间。

## 5. 停止服务

- 想要停止后端或前端，只需回到对应的终端窗口，按下 `Ctrl + C`。
- 关闭虚拟环境可以在终端输入 `deactivate`。

## 6. 将 Web 应用嵌入桌面窗口

想要更酷的“桌面小组件”体验，可以把前后端打包进一个原生窗口。

1. 在 `frontend` 目录执行一次构建，生成静态资源：
   ```bash
   cd frontend
   npm run build
   ```
2. 安装桌面模式所需的 Python 依赖（在项目根目录执行）：
   ```bash
   pip install -r desktop/requirements.txt
   ```
3. 运行启动脚本：
   ```bash
   python desktop/launch_widget.py
   ```
   该脚本会自动开启 FastAPI 后端，并在一个 PyWebView 窗口中加载刚才构建好的前端页面；关闭窗口时会自动停止后端。

## 7. 常见问题排查

| 问题 | 可能原因 | 解决方案 |
| --- | --- | --- |
| 浏览器访问前端时白屏或报错 | 后端服务没启动 | 确认第一个终端里 `uvicorn` 正在运行，没有报错。 |
| `pip install` 报错 | Python 版本太旧或网络问题 | 检查 Python 版本是否 ≥ 3.10；重试或切换网络。 |
| `npm run dev` 报错 | Node.js 版本过低或依赖安装失败 | 确保 Node.js ≥ 18；运行 `npm install` 重新安装依赖。 |
| 端口被占用 | 其他程序占用了 8000/5173 端口 | 关闭其他程序，或修改运行命令使用其他端口。 |

## 8. 下一步可以做什么？

- 将目前的 Web 前端和后端打包到桌面壳（Tauri / Electron）中，做出真正的桌面组件。
- 把目前的内存数据存储换成 SQLite 等持久化方案，加入用户登录、统计等高级功能。
- 编写自动化测试，构建 CI/CD 流程，让项目更加稳定。

有任何问题随时反馈，我们可以在 README 中继续补充操作指南。
