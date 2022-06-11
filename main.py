import logging
import os
import os.path
import re
import pypandoc
import cn2an
import GUI  # 调用我们的GUI界面

# 当前版本号(常量)
VERSION = 3.2

logging.basicConfig(level=logging.INFO,
                    format=f'%(asctime)s - %(levelname)s- 当前版本-> V{VERSION} <- - %(message)s')

# 打印函数


def printToFile():
    # 打印次数
    counter = 0

    # 第一次打印封面
    booktitle = True

    # 获取当前文件夹的名字
    novel_title = os.path.basename(os.getcwd())

    for each_file in GUI.AllFileSortedList:
        # 把章节名字分离
        print(each_file)
        name = each_file[1].split('.txt')[0]

        # 打开文件来读取内容
        with open(name + '.txt', 'r', encoding='utf-8') as f:
            content = f.readlines()

            # 将每一章的内容写入到我们的大章
            with open(novel_title + ".txt", 'a+', encoding='utf-8') as f2:
                counter += 1

                # 使用笨方法来避免重复打印
                if booktitle == True:
                    # 封面页的简介
                    f2.write('% ' + novel_title + '\n')
                    f2.write('% ' + '该软件由\tBemake\t无偿编写\t请勿二手倒卖,联系邮箱:271374667@qq.com' + '\n\n')
                    booktitle = False

                f2.write(f'\n#  {name}\n\n')
                for contents in content:
                    
                    # 替换需要过滤的字符串
                    for i in GUI.filterWord:
                        contents = contents.replace(i,'')
                        
                    # 打印我们的内容
                    f2.write(contents)
                    
                    # 给我们的小说换行
                    for _ in range(int(GUI.spaceNumber)):
                        f2.write("<br> \n")

        logging.info(f'目前打印了{counter}次,正在打印\t{each_file}')

    logging.warning('打印结束，正在生成EPUB文件………………')

    # 打印最终的epub文件
    with open(novel_title + '.txt', 'r', encoding='utf-8') as f3:
        content = f3.readlines()
        Strcontent = ''.join(content)
        pypandoc.convert_text(Strcontent, 'epub', format='md',
                              outputfile=novel_title + '.epub')


def smartSortStart():
    # 提取我们文本中的数字(提取我们的第一个数字)
    for eachFile in GUI.currentDirAllFileNameList:
        
        # 使用守卫if单独处理我们的废话
        if eachFile.find('章') == -1 and eachFile.find('第') == -1:
            # 根据权重
            if GUI.Args.sideStory == '最后面':                 
                GUI.AllFileSortedList.append((GUI.sideStoryWeight, eachFile))
            
            else:
                GUI.AllFileSortedList.append((GUI.sideStoryWeight - 200000, eachFile))
            
            # 确保文件能够递增
            GUI.sideStoryWeight += 1
        
        
        # 将标题中所有的数字翻译成我们的阿拉伯数字
        title2number = cn2an.transform(eachFile,'cn2an')
        
        # 提取标题中的第一个数字,一直到章为止
        p = re.compile(r'第(\d+?)章.*?\.txt')
        title_index = re.findall(p, title2number)
        
        # 将提取之后的章节数字和文件的名称组成一个(章节数字，章节名称)元组，方便我们后期来排序
        if title_index != []:
            GUI.AllFileSortedList.append((title_index[0], eachFile))
        
            logging.debug(f"添加了一个新的数字编号 {title_index} 字")
                    
    # 对列表的内容进行排序
    GUI.AllFileSortedList = sorted(GUI.AllFileSortedList,key=lambda x: int(x[0]))
    
    # 调试
    logging.debug(GUI.AllFileSortedList)
    
    # 对数据内容进行打印并排版        
    printToFile()


def main():

    # 切换我们的工作路径到目标文件夹
    logging.info(GUI.Args)
    os.chdir(GUI.Args.opendir)

    # 获取当前文件夹下所有的文件
    GUI.currentDirAllFileNameList = os.listdir('.')

    # 进行选择我们要进行的是哪个操作
    if GUI.Args.RESULT == 'smartSort':
        logging.info('当前选择了 smart')
        
        # 调用我们的只能排序方法
        smartSortStart()

    if GUI.Args.RESULT == 'force':
        logging.info('当前选择了 force')

    if GUI.Args.RESULT == 'default':
        logging.info('当前选择了 default')


if __name__ == '__main__':
    GUI.GUI()
    main()
