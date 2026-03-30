# 📖 读书笔记 - Reading Notes App

一款帮助你记录阅读感悟的移动端优先 Web 应用，基于 Streamlit 构建，支持通过 Streamlit Cloud 一键部署。

## 技术栈

- **应用框架**：[Streamlit](https://streamlit.io/)（Python）
- **数据库 + 认证**：[Supabase](https://supabase.com/)（PostgreSQL + Auth + RLS）
- **AI 文案生成**：[DeepSeek API](https://platform.deepseek.com/)（deepseek-chat）
- **海报图片**：[Pillow](https://pillow.readthedocs.io/)
- **部署**：[Streamlit Cloud](https://streamlit.io/cloud)

## 功能

- **用户认证**：邮箱注册/登录（Supabase Auth）
- **笔记 CRUD**：添加、查看、删除读书笔记（书名、摘抄、想法、日期）
- **笔记列表**：按日期倒序展示，支持按书名筛选
- **AI 读书海报**：基于某本书的所有笔记，AI 生成文案 + Pillow 渲染精美海报图片
- **年度书单**：按年份统计读过的书和笔记数量
- **个人中心**：查看邮箱、退出登录
- **移动端适配**：最大宽度 512px，米色暖色调 UI

## 快速开始

### 1. 克隆仓库

```bash
git clone <repo-url>
cd reading-notes-streamlit
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 Supabase

1. 在 [Supabase](https://supabase.com) 创建项目。
2. 在 **SQL Editor** 中运行 `sql/init.sql` 初始化数据库表和 RLS 策略。
3. 在项目 Settings > API 中获取 **Project URL** 和 **anon public key**。

### 4. 配置 Secrets

复制 secrets 模板并填入你的密钥：

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

编辑 `.streamlit/secrets.toml`：

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
DEEPSEEK_API_KEY = "your-deepseek-api-key"
```

### 5. 本地运行

```bash
streamlit run app.py
```

访问 http://localhost:8501

## 部署到 Streamlit Cloud

1. 将代码推送到 GitHub 仓库。
2. 登录 [Streamlit Cloud](https://share.streamlit.io/)。
3. 点击 **New app**，选择你的 GitHub 仓库，主文件填 `app.py`。
4. 在 **Advanced settings > Secrets** 中添加：

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
DEEPSEEK_API_KEY = "your-deepseek-api-key"
```

5. 点击 **Deploy** 即可。

## 项目结构

```
├── app.py                           # 主应用（所有页面逻辑）
├── requirements.txt                 # Python 依赖
├── .streamlit/
│   ├── config.toml                  # Streamlit 主题配置
│   └── secrets.toml.example         # Secrets 模板
├── utils/
│   ├── __init__.py
│   ├── supabase_client.py           # Supabase 客户端
│   ├── auth.py                      # 认证逻辑
│   ├── database.py                  # 数据库操作
│   └── poster.py                    # AI 文案 + 海报图片生成
├── sql/
│   └── init.sql                     # 数据库初始化脚本（建表 + RLS）
├── .env.example                     # 环境变量模板
└── README.md
```

## 界面风格

- 主色调：米色（#faf7f2）+ 深灰色（#2c2c2c）
- 卡片：大圆角（16px），轻微阴影
- 移动端优先，最大宽度 512px 居中显示
- 侧边栏导航：首页、添加笔记、年度书单、个人中心

## 数据库设计

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | uuid | 主键，自动生成 |
| `user_id` | uuid | 关联 auth.users |
| `book_name` | text | 书名 |
| `sentence` | text | 摘抄句子 |
| `thought` | text | 个人想法 |
| `date` | date | 记录日期，默认当天 |
| `created_at` | timestamptz | 创建时间 |

RLS 策略确保每个用户只能访问自己的数据。
