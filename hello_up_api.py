import requests
import json
from pathlib import Path
from loguru import logger
url = "https://www.helloimg.com/api/v1/upload"

hello_token = '你的token'
headers = {
    "Authorization": f"Bearer {hello_token}",
    "Accept": "application/json",
}

def upload_image(image_path, album_id):
    """
    上传图片并获取URL
    
    Args:
        image_path: 图片文件路径
        album_id: 相册ID

    Returns:
        dict: 包含上传结果的字典,包括url、markdown等
        
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
                raise Exception(f"上传失败: {result.get('message', '未知错误')}")
                
            # 获取返回数据
            image_data = result["data"]["links"]
            return {
                "url": image_data["url"],
                "markdown": image_data["markdown"],
                "html": image_data["html"],
                "delete_url": image_data["delete_url"]
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

if __name__ == "__main__":
    try:
        # 图片路径
        image_path = r"vx_images\89688729441702.png"
        # 相册ID 未选择相册ID为0
        album_id = 0
        # 上传图片
        result = upload_image(image_path, album_id)
        logger.info("上传成功!")
        logger.info(f"图片URL: {result['url']}")
        logger.info(f"Markdown: {result['markdown']}")
        logger.info(f"HTML: {result['html']}")
        logger.info(f"删除URL: {result['delete_url']}")
    except Exception as e:
        logger.error(f"错误: {str(e)}")
