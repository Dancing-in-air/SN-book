from scrapy.cmdline import execute
import os
import sys


def main():
    # 将当前文件的父目录路径添加到sys.path中,sys.path中的所有路径都会被添加到环境变量中去
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(["scrapy", "crawl", "book"])


if __name__ == '__main__':
    main()
