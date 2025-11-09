# 使用指南 (Usage Guide in Chinese)

## CloudDrive2 媒体流应用使用说明

本应用为 CloudDrive2 挂载的 Google Drive 文件提供稳定的流媒体服务，支持断点续传和大文件传输。

---

## 快速开始

### 方法一：使用 Docker（推荐）

**1. 编辑 `docker-compose.yml` 文件**

找到以下行并修改为你的 CloudDrive2 挂载路径：
```yaml
volumes:
  - /path/to/your/clouddrive:/mnt/clouddrive:ro
```

例如：
```yaml
volumes:
  - /mnt/clouddrive2:/mnt/clouddrive:ro
```

**2. 启动服务**
```bash
docker-compose up -d
```

**3. 访问应用**

在浏览器中打开：
```
http://localhost:8000
```

你会看到一个网页界面，可以浏览和播放文件。

---

### 方法二：本地运行

**1. 安装依赖**
```bash
pip install -r requirements.txt
```

**2. 配置设置**
```bash
# 复制配置文件模板
cp .env.example .env

# 编辑 .env 文件，设置你的 CloudDrive2 挂载路径
nano .env  # 或使用其他编辑器
```

在 `.env` 中修改：
```ini
CLOUDDRIVE_MOUNT_PATH=/你的/clouddrive2/挂载路径
```

**3. 启动应用**
```bash
# 使用启动脚本
./start.sh

# 或手动启动
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**4. 访问应用**

浏览器打开：`http://localhost:8000`

---

## 主要功能使用

### 1. 网页界面

访问 `http://localhost:8000`，你可以：
- 浏览 CloudDrive2 中的文件和文件夹
- 点击 "Stream" 直接播放视频/音频
- 点击 "Info" 查看文件详细信息

### 2. 直接播放视频

在浏览器地址栏输入：
```
http://localhost:8000/api/stream/视频文件路径
```

例如：
```
http://localhost:8000/api/stream/movies/movie.mp4
```

大多数浏览器和播放器（如 VLC）可以直接播放。

### 3. 下载文件（支持断点续传）

使用 curl 或 wget：

```bash
# 下载完整文件
curl http://localhost:8000/api/stream/file.mp4 -o file.mp4

# 断点续传下载
curl -C - http://localhost:8000/api/stream/file.mp4 -o file.mp4
```

### 4. 在其他应用中使用

**VLC 播放器：**
```
文件 -> 打开网络串流 -> 输入：
http://localhost:8000/api/stream/你的视频路径
```

**PotPlayer：**
```
右键 -> 打开 -> 打开链接 -> 输入：
http://localhost:8000/api/stream/你的视频路径
```

---

## API 使用示例

### 列出文件
```bash
# 列出根目录
curl http://localhost:8000/api/files/list

# 列出指定目录
curl http://localhost:8000/api/files/list/movies
```

### 获取文件信息
```bash
curl http://localhost:8000/api/files/info/movies/movie.mp4
```

### 获取视频元数据
```bash
curl http://localhost:8000/api/stream/movies/movie.mp4/metadata
```

---

## 启用认证（可选）

如果需要保护你的文件，可以启用认证：

**1. 编辑 `.env` 或 `docker-compose.yml`**

添加或修改：
```ini
AUTH_USERNAME=你的用户名
AUTH_PASSWORD=你的密码
```

**2. 重启服务**
```bash
# Docker
docker-compose restart

# 本地
# 按 Ctrl+C 停止，然后重新运行 ./start.sh
```

**3. 使用认证访问**

在浏览器中会提示输入用户名和密码，或在 curl 中使用：
```bash
curl -u 用户名:密码 http://localhost:8000/api/files/list
```

---

## 常见用途

### 1. 家庭媒体服务器
- 将 CloudDrive2 挂载的 Google Drive 作为媒体库
- 通过本应用在局域网内流式播放视频
- 支持多设备同时访问

### 2. 远程文件访问
- 配合 Nginx 反向代理，添加 HTTPS
- 在外网访问家中的 CloudDrive2 文件
- 支持断点续传，适合大文件下载

### 3. API 集成
- 使用 API 端点集成到其他应用
- 参考 `examples/` 目录中的示例代码
- Python、JavaScript、Shell 脚本示例都有

---

## 查看更多文档

- **详细部署指南**：查看 `DEPLOYMENT.md`
- **API 完整文档**：查看 `API.md` 或访问 `http://localhost:8000/docs`
- **客户端示例**：查看 `examples/` 目录

---

## 停止服务

**Docker：**
```bash
docker-compose down
```

**本地：**
按 `Ctrl+C` 停止服务

---

## 常见问题

### 1. 无法访问文件

**检查 CloudDrive2 挂载路径是否正确：**
```bash
ls /你的/clouddrive2/路径
```

**确认 `.env` 或 docker-compose.yml 中的路径配置正确。**

### 2. 端口被占用

修改端口（默认 8000）：

在 `docker-compose.yml` 中：
```yaml
ports:
  - "8080:8000"  # 改用 8080 端口
```

或在 `.env` 中：
```ini
PORT=8080
```

### 3. 播放卡顿

调整缓冲块大小，在 `.env` 中：
```ini
CHUNK_SIZE=2097152  # 增加到 2MB
```

---

## 需要帮助？

如有问题，可以：
1. 查看日志：`docker-compose logs -f`（Docker）或终端输出（本地）
2. 查看详细文档：`DEPLOYMENT.md` 和 `API.md`
3. 提交 Issue：https://github.com/lyjlyjn/lynx/issues

---

**祝使用愉快！🎉**
