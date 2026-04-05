# summarize-video — Claude Code Skill

一个 Claude Code 自定义 skill，支持对 **B站、小红书、YouTube** 等平台的视频生成结构化摘要。

无字幕时自动下载音频并通过 **Whisper** 本地转录，全程离线，无需付费 API。

## 效果示例

```
/summarize-video http://xhslink.com/xxxxx
```

输出：

> **核心主题**：介绍 Claude Code Unpacked 可视化网站
>
> **主要内容**
> 1. **背景**：Claude Code 源码泄露后，有开发者做成了可视化交互指南
> 2. **网站内容**：消息流转、Agent 运行机制、内部工具、斜杠命令、隐藏实验功能
>
> **关键结论**：构建 Agent 或研究 AI 架构的开发者的最直观参考

## 安装依赖

### 1. yt-dlp（视频下载）

```bash
pip3 install yt-dlp
```

### 2. ffmpeg（音频处理）

```bash
# macOS（推荐）
brew install ffmpeg

# 或下载预编译包：https://ffmpeg.org/download.html
```

### 3. Whisper（语音转录）

```bash
pip3 install openai-whisper
```

> 首次转录时会自动下载 `small` 模型（约 460MB），缓存在本地，之后无需重复下载。

## 安装 Skill

将 `summarize-video.md` 放入 Claude Code 的用户命令目录：

```bash
mkdir -p ~/.claude/commands
cp summarize-video.md ~/.claude/commands/
```

## 使用方法

在任意 Claude Code 对话中输入���

```
/summarize-video <视频链接>
```

支持平台举例：

| 平台 | 示例 |
|------|------|
| B站 | `https://www.bilibili.com/video/BVxxxxxxxx` |
| 小红书 | `http://xhslink.com/xxxxx` |
| YouTube | `https://www.youtube.com/watch?v=xxxxx` |

## 工作原理

```
输入 URL
  ↓
尝试提取字幕（yt-dlp）
  ├─ 有字幕 ──→ 清洗时间戳 ──→ Claude 总结
  └─ 无字幕 ──→ 下载音频 ──→ Whisper 转录 ──→ Claude 总结
```

## 常见问题

**Q：转录速度很慢？**
将 skill 中 `--model small` 改为 `--model tiny`，速度提升约 3 倍，精度略降。

**Q：下载失败？**
部分平台有版权保护，yt-dlp 无法下载。可手动粘贴视频文字内容让 Claude 直接总结。

**Q：支持英文视频吗？**
支持，Whisper 自动检测语言。

## License

MIT
