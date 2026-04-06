# 视频总结

将 B站、小红书或其他平台视频总结为结构化要点。

## 执行步骤

### 第零步：确认工具路径

运行以下命令，获取本机实际路径：

```bash
which yt-dlp || find ~/Library/Python -name yt-dlp 2>/dev/null | head -1
which ffmpeg || ls /opt/homebrew/bin/ffmpeg 2>/dev/null
python3 -c "import whisper; print('whisper ok')" 2>/dev/null || echo "whisper 未安装"
```

记录 yt-dlp 的实际路径，后续步骤替换 `<yt-dlp路径>`。

---

### 第一步：尝试提取字幕

```bash
<yt-dlp路径> \
  --write-subs --write-auto-subs \
  --sub-langs "zh-Hans,zh,zh-CN,en" \
  --skip-download -o "/tmp/video_sub" "$URL"
ls /tmp/video_sub* 2>/dev/null
```

- **有字幕文件** → 跳到第三步
- **无字幕** → 执行第二步

---

### 第二步：下载音频 + Whisper 转录

下载视频（yt-dlp 会输出 mp4，无需 ffmpeg 转换）：

```bash
<yt-dlp路径> \
  -f "bestaudio/best" \
  -o "/tmp/video_audio.%(ext)s" "$URL"
```

用 Whisper 转录（自动检测语言）：

```bash
PATH="/opt/homebrew/bin:$PATH" \
  python3 -m whisper /tmp/video_audio.* \
  --model small \
  --output_format txt \
  --output_dir /tmp/
```

读取结果：`cat /tmp/video_audio.txt`

---

### 第三步：清洗文本

VTT/SRT 字幕去除时间戳：

```bash
cat /tmp/video_sub*.vtt 2>/dev/null | \
  grep -v "^WEBVTT" | grep -v "^[0-9]" | \
  grep -v "^-->" | grep -v "^$" | sort -u
```

Whisper 输出的 txt 直接使用。

---

### 第四步：生成总结

基于文本内容，输出以下结构：

---

## 视频总结：[标题]

**核心主题**：一句话概括视频讲了什么

**主要内容**

1. **[要点标题]**
   - 具体细节

2. **[要点标题]**
   - ...

（根据内容列 3-6 个要点）

**关键结论**：最重要的 1-3 个结论或行动建议

**适合人群**：谁看这个视频收益最大

---

### 第五步：清理临时文件

```bash
rm -f /tmp/video_sub* /tmp/video_audio*
```

---

## 注意事项

- Whisper `small` 模型首次运行需下载约 460MB 缓存到本地，之后无需重复下载
- 视频超过 30 分钟可改用 `--model tiny` 加速
- 中文视频 Whisper 自动识别，无需指定语言
- 下载失败（版权限制）时提示用户手动提供文字内容

## 用法

```
/summarize-video https://www.bilibili.com/video/BVxxxxxxxx
/summarize-video http://xhslink.com/xxxxx
/summarize-video https://www.youtube.com/watch?v=xxxxx
```
