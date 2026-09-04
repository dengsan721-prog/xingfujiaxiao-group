# 董事长（孩子）长成记 群发助手

这是一个静态网页 demo，用来把 5 个主题、每个主题 14 天的群发内容整理成可复制的群运营工具。

## 使用

直接打开 `demo/index.html`。

页面支持：

- 选择 5 个主题
- 选择第 1 到 14 天
- 复制当天全文
- 单独复制每个小模块，包括今日小角色、签到、1 分钟内容、话题、小游戏、小作业、教练收口
- 使用幸福驿站 logo

## 重新生成

```bash
python scripts/generate_demo.py
python -m unittest tests.test_demo_generation
```

## 发布

这个项目是纯静态页面，可以直接发布到 GitHub Pages、Gitee Pages 或任意静态网站托管服务。
