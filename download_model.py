
import os

# 设置环境变量
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
from huggingface_hub import snapshot_download

snapshot_download(repo_id="valurank/News_Articles_Categorization", repo_type="dataset",local_dir="model\\",resume_download=True)