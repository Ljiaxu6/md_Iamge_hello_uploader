# Hello图床 Markdown图片上传工具

## 项目概述
这是一个用于将Markdown文档中的本地图片自动上传到Hello图床并替换链接的工具。支持命令行和非命令行两种使用方式。

### 主要功能
- 上传单个图片到Hello图床
- 批量处理Markdown文档中的本地图片 
- 目前只支持图片样式`![]()`
- 自动替换图片链接，可重复上传，自动跳过上传后的照片
- 保留原文档，生成新的处理后文档

### 文件结构
- `hello_up_api.py`: 单文件上传工具
- `Cli_md_Iamge_hello_uploader.py`: 命令行版本的Markdown处理工具
- `NoCli_md_Iamge_hello_uploader.py`: 非命令行版本的Markdown处理工具

### 依赖库
```bash
pip install requests
pip install loguru
pip install pathlib
```

## 详细说明

### 1. hello_up_api.py
单个图片上传工具，用于测试token和上传功能。

#### 使用方法
```python
# 直接运行
python hello_up_api.py

# 作为模块导入
from hello_up_api import upload_image
result = upload_image("path/to/image.png", "album_id")
```

### 2. Cli_md_Iamge_hello_uploader.py
命令行版本，适合批处理或脚本调用。

#### 使用方法
```bash
# 基本用法
python Cli_md_Iamge_hello_uploader.py <markdown文件路径> <相册ID>

# 示例
python Cli_md_Iamge_hello_uploader.py 测试笔记.md 1353

# 使用绝对路径
python Cli_md_Iamge_hello_uploader.py "D:\Documents\测试笔记.md" 1353

# 查看帮助
python Cli_md_Iamge_hello_uploader.py --help
```

### 3. NoCli_md_Iamge_hello_uploader.py
非命令行版本，适合在IDE中使用或快速处理单个文件。

#### 使用方法
1. 打开文件，修改配置部分:
```python
def main():
    # 配置
    md_file = r"测试笔记.md"  # 修改为你的Markdown文件路径
    album_id = "1353"  # 修改为你的相册ID 
```

2. 直接运行:
```bash
python NoCli_md_Iamge_hello_uploader.py
```

## 配置说明

### 1. Token配置
在使用前需要配置Hello图床的API Token:
1. 登录 [Hello图床](https://www.helloimg.com/)
2. 进入个人设置 -> API令牌
3. 创建新的令牌
4. 将令牌替换到代码中的headers部分:
```python
headers = {
    "Authorization": "Bearer your_token_here",
    "Accept": "application/json",
}
```

### 2. 相册ID获取
1. 登录Hello图床
2. 进入相册页面
3. 在URL中可以看到相册ID
4. 或在相册设置中查看相册ID
5. 未选择相册ID为0

## 注意事项

1. **文件路径**
   - 支持相对路径和绝对路径
   - 包含空格的路径需要用引号包裹
   - 建议使用原始字符串(r"path")处理Windows路径

2. **图片处理**
   - 只处理本地图片，网络图片会保持原样
   - 支持各种图片格式(PNG, JPG, GIF等)
   - 图片必须存在且可访问

3. **文件保存**
   - 处理后的文件会自动添加"_uploaded"后缀
   - 原文件不会被修改
   - 新文件保存在原文件相同目录下

## 常见问题

1. **401错误**
   - 检查token是否正确
   - 确认token未过期
   - 验证token权限是否足够

2. **图片上传失败**
   - 检查网络连接
   - 确认图片文件存在
   - 验证图片格式是否支持
   - 检查相册ID是否正确

3. **文件路径问题**
   - 使用原始字符串(r"path")处理Windows路径
   - 确保有文件读写权限
   - 检查路径是否包含特殊字符

## 使用建议

1. 首次使用时:
   - 先用`hello_up_api.py`测试token是否有效
   - 用小文件测试功能是否正常

2. 批量处理时:
   - 建议使用命令行版本
   - 做好文件备份
   - 检查处理后的文件

3. 日常使用:
   - 非命令行版本更方便单文件处理
   - 可以创建批处理文件(.bat)简化使用

## 更新日志

- 2024-12-29: 初始版本发布
  - 支持基本的图片上传功能
  - 添加命令行和非命令行版本
  - 完善错误处理和日志记录
