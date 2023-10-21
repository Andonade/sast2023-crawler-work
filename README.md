## 清华大学教参平台爬虫

本项目为清华大学计算机系科协2023暑培爬虫课程作业

爬取网站: [清华大学教参平台](http://reserves.lib.tsinghua.edu.cn/)

By: [Andonade](https://github.com/Andonade)

### 环境配置

使用Python 3.10.12

安装依赖：

```zsh
pip install -r requirements.txt
```

### 使用说明

请在**config.json**中对应处填入你访问教参网站的Cookie以及想要爬取教材的BookId[^1]。

[^1]: BookId可以在教参网站上教材详情页的url中找到，如[《大学物理学. 力学、热学（第4版》](http://reserves.lib.tsinghua.edu.cn/Search/BookDetail?bookId=ca0dfa6c-339e-4d95-8be4-769d8578164c)，其中"bookId="后内容即为BookId

然后使用以下命令运行：

```zsh
python main.py
```

### 实现功能

✅ 以图片形式爬取教材内容

✅ 将爬取图片转换为PDF

✅ PDF文件名为教材名

✅ 手动选择爬取的章节
