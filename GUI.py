'''
Author: Bemake
Date: 2022-06-10 17:23:57
LastEditTime: 2022-06-11 17:27:57
Description: 如果代码出现问题请联系本人邮箱:271374667@qq.com
'''
import logging
from gooey import Gooey, GooeyParser

# 当前版本号(常量)
VERSION = 3.2

logging.basicConfig(level= logging.INFO, format=f'%(asctime)s - %(levelname)s- 当前版本-> V{VERSION} <- - %(message)s')

@Gooey(language='chinese',navigation="TABBED",clear_brfore_run=True)
def GUI():
    # 新建一个大的parser容器
    parser = GooeyParser(description='请选择一项排序的方式来进行下一步的操作')
    
    # 为分类方式创建一个容器
    sub = parser.add_subparsers(help='选择你的分类',dest="RESULT")
    
    # 智能排序================================================================
    smartSortTabbed = sub.add_parser('smartSort')
            
    # 打开文件夹
    smartSortTabbed.add_argument('opendir',metavar='打开文件夹目录',help='请在这里选择你需要转换成EPUB的小说目录',widget='DirChooser')
    
    # 增加说明类
    
            
    # 在互斥分组内添加选项
    # smartSortTabbed.add_argument('--smart',metavar="智能排序（推荐）",help='使用智能转换，将小说前面自带的章节数字转换成阿拉伯数字再进行排序',action='store_true')
    # smartSortTabbed.add_argument('--force',metavar="强制排序（稳定）",help='使用自带的爬虫进行爬取的小说，会在小说章节前有█的标志（如果没有标志请不要选择该项）',action='store_true')
    # smartSortTabbed.add_argument('--default',metavar="系统默认（不推荐）",help='使用系统默认的排序方法，章节的顺序可能会发生错乱\n如果不做选择默认将会选择系统默认',action='store_true')
    
    # 增加更多可选项
    more = smartSortTabbed.add_argument_group('更多可定制的选项',gooey_options={
        'show_border': True
    })
    
    # 我们的番外放在哪里
    more.add_argument('--sideStory',metavar='番外权重',help="我们的番外(作者杂谈之类的)放在哪里?",choices=['最前面','最后面'],default='最后面')
    
    # 我们每一行需要换几次空格
    more.add_argument('--space',metavar='空格数量',help='小说每一行之间都会有空行,你可以在这里设置空行的大小, \
                        如果发现空行过大可以适当调小该值',choices=['0','1','2','3'],default='1')
    
    # 对于某些广告或者特殊元素的屏蔽
    more.add_argument('--filter',metavar="过滤字符串",help="如果你在元素里面发现一些特殊的字符串，并且他们大量出现在你的小说里面 \
                        那么你可以尝试在这里输入他们来屏蔽这些字符串,比如 <欢迎来到XX小说网> 你也可以同时输入多个值,他们之间用 \\n 隔开",widget="Textarea",
                        gooey_options={
                            'height': 100,
                            'show_label': True,
                            'show_help': True,
                        })
    
    # 最终显示我们的图形化界面
    args = parser.parse_args()
    
    # 将我们的参数返回
    return args


# 调用GUI的同时返回变量，方便我们主程序引用
# Args我们GUI的输出
Args = GUI()
#print(Args) 

# 番外的权重(默认为10W)
sideStoryWeight = 100000

# 空格的数量(默认为1)
spaceNumber = Args.space

# 过滤的关键词(默认为无,默认的分割符为\n)
filterWord = list(Args.filter.split("\\n")) if Args.filter != None else None
#logging.info(filterWord)

# 新建当前文件夹下所有的文件名
currentDirAllFileNameList = []

# 新建一个排序过后的文件名字列表
AllFileSortedList = []

