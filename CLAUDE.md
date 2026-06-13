```markdown
# CLAUDE.md - PetConnect (暖爪救助)

## 语言要求
请始终使用简体中文回答。代码和术语可以保留英文，但解释、建议、提问全部用中文。

## 项目定位
- 大学课程原型项目：宠物救助全栈平台（Django REST API + React SPA）
- 核心模块：领养申请与审核、救助追踪、报失寻主、社区互动、CMS
- 技术栈：Python 3.11 + Django + DRF + JWT，前端 React (CRA) + Bootstrap 5

## 目录结构（关键）
```
backend/
  accounts/       # 用户、JWT、profile、封禁
  pets/           # 宠物档案、领养申请、问卷、附件、线下核验
  rescue/         # 救助案例、状态流水、状态机
  lostfound/      # 报失/寻主（含经纬度）
  community/      # 帖子、评论、点赞、收藏
  cms/            # 科普/公告/法规文章、分类
  portal/         # 首页轮播
  common/         # 共享：文件上传、品种识别(CNN)、LLM客户端、权限
  system/         # 管理后台、用户/内容处置、操作日志、AI调用日志
  api/            # 仅路由聚合，无models/views
frontend/
  src/api/        # Axios实例 + 按模块拆分的API调用
```
- 测试与源码同目录：`test_*.py`

## 常用命令
```bash
# 后端（先 cd backend）
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver

# 前端（先 cd frontend）
npm install
npm start
npm test
```

## 关键约定
- **提交规范**：Conventional Commits（`feat:` / `fix:` / `docs:` / `chore:`）
- **数据库**：SQLite 默认，表名自定义，主键 `BigAutoField`
- **权限三层**：公开 → 登录 → 管理员（检查 `profile.role` 或 `is_superuser`）
- **状态机**：救助状态流转由 `RescueStatusMachine` 校验，禁止跳跃或回退
- **封禁机制**：`profile.status == 1` 被 `IsActiveUser` 拒绝
- **管理员模式前端**：`AdminRoute` 校验 `role === 'admin'`，状态存 `localStorage`

## 踩坑记录
- Django 项目包名就是 `backend`，不要重命名
- `accounts` 必须先迁移，直接 `migrate` 不要按 app 手跑
- `api` app 只是路由聚合，无 models/views
- 品种识别权重 `.pt` 需单独下载，不在 git
- Windows 中文乱码用 `scripts/ensure_utf8.py` 修复
- 生产环境 S3 需手动安装 `django-storages[boto3]`

## 项目特有约束
- 领养问卷答案存 JSON，不用 EAV
- 救助状态流水必须记录 `remark`
- 审核拒绝/核验失败必须填写原因
- 平台配置存 `platform_config` 表
- LLM 调用用原生 `urllib`，环境变量 `LLM_API_KEY` / `LLM_API_BASE` / `LLM_MODEL`

## 自我维护
- 发现规则与代码不符时主动提出
- 已被 linter/CI 覆盖的规则建议删除
```