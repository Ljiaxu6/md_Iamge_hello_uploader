import re
import requests
import json
from pathlib import Path
from loguru import logger
import argparse

# Hello图床API URL和请求头
url = "https://www.helloimg.com/api/v1/upload"
hello_token = '你的token'
headers = {
    "Authorization": f"Bearer {hello_token}",
    "Accept": "application/json",
}

def upload_image(image_path, album_id):
    """
    上传图片到Hello图床并获取URL
    
    Args:
        image_path: 图片文件路径
        album_id: 相册ID

    Returns:
        dict: 包含上传结果的字典,包括url
        
    Raises:
        Exception: 上传失败时抛出异常
    """
    try:
        # 检查文件是否存在
        if not Path(image_path).exists():
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
            
        files = {
            "file": open(image_path, "rb")
        }
        
        data = {
            "album_id": album_id,
            "permission": "0",
            "strategy_id": "1",
        }
        
        try:
            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()  # 检查HTTP状态码
            
            result = response.json()
            
            # 检查上传状态
            if not result.get("status"):
                raise Exception(f"上传失败: {result}")
                
            # 获取返回数据
            image_data = result["data"]["links"]
            return {
                "url": image_data["url"]
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求失败: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("解析响应数据失败")
            
    except Exception as e:
        raise Exception(f"上传图片失败: {str(e)}")
        
    finally:
        # 确保关闭文件
        if "files" in locals() and "file" in files:
            files["file"].close()

def process_markdown(md_file_path, album_id):
    """
    处理markdown文件,上传图片并替换链接
    
    Args:
        md_file_path: markdown文件路径
        album_id: hello图床相册ID
        
    Returns:
        str: 处理后的markdown内容
    """
    # 读取md文件
    md_path = Path(md_file_path)
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown文件不存在: {md_file_path}")
        
    content = md_path.read_text(encoding='utf-8')
    
    # 匹配图片语法 ![任意文本](图片路径)
    img_pattern = r'!\[(.*?)\]\((.*?)\)'
    
    def replace_image(match):
        alt_text = match.group(1)  # 图片描述文本
        img_path = match.group(2)  # 图片路径
        
        # 如果是网络图片则跳过
        if img_path.startswith(('http://', 'https://')):
            return match.group(0)
            
        # 构建完整的图片路径
        full_img_path = md_path.parent / img_path
        
        try:
            # 上传图片
            result = upload_image(str(full_img_path), album_id)
            logger.info(f"图片 {img_path} 上传成功: {result}")
            # 返回新的markdown图片语法
            return f'![{alt_text}]({result["url"]})'
        except Exception as e:
            logger.warning(f"警告: 图片 {img_path} 上传失败: {str(e)}")
            return match.group(0)  # 保持原样
    
    # 替换所有图片
    new_content = re.sub(img_pattern, replace_image, content)
    
    return new_content

def save_new_markdown(original_path, new_content):
    """保存新的markdown文件"""
    original_path = Path(original_path)
    new_path = original_path.parent / f"{original_path.stem}_uploaded{original_path.suffix}"
    new_path.write_text(new_content, encoding='utf-8')
    return new_path

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description="上传Markdown文档中的图片到Hello图床")
    parser.add_argument("md_file", help="Markdown文件路径")
    parser.add_argument("album_id", help="Hello图床相册ID")
    args = parser.parse_args()
    
    try:
        # 处理markdown文件
        logger.info("开始处理markdown文件...")
        new_content = process_markdown(args.md_file, args.album_id)
        
        # 保存新文件
        new_file = save_new_markdown(args.md_file, new_content)
        logger.info(f"处理完成! 新文件已保存为: {new_file}")
        
    except Exception as e:
        logger.error(f"错误: {str(e)}")

if __name__ == "__main__":
    main()