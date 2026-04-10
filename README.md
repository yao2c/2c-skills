# 2c-skills

收录我制作的 Claude Code 自定义 Skills（斜杠命令），可直接复制使用。

## 安装方法

将对应的 `.md` 文件放入 Claude Code 用户命令目录：

```bash
cp <skill-name>.md ~/.claude/commands/
```

## Skills 列表

| Skill | 功能 |
|-------|------|
| [summarize-video](./summarize-video/) | 总结 B站、小红书、YouTube 等平台视频，无字幕时自动 Whisper 转录 |
| [xiaohongshu-posting](./xiaohongshu-posting/) | 根据书桌/学习照片生成小红书标题、正文、标签，支持趋势扫描与迭代修改 |
