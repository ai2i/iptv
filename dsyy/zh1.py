import os
import requests
import xml.etree.ElementTree as ET

# 获取当前目录
directory = os.getcwd()

# 下载并解析 EPG 文件
epg_url = "https://live.fanmingming.com/e.xml"
response = requests.get(epg_url)
epg_root = ET.fromstring(response.content)

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        input_file = os.path.join(directory, filename)
        output_file = os.path.join(directory, f"{os.path.splitext(filename)[0]}.m3u")

        with open(input_file, 'r', encoding='utf-8', errors='ignore') as input_file:
            with open(output_file, 'w', encoding='utf-8') as output_file:
                output_file.write('#EXTM3U\n')
                for line in input_file:
                    line = line.strip()
                    if line and not line.startswith('#') and ',#genre#' not in line:
                        channel_name, channel_link = line.split(',', 1)
                        output_file.write(f'#EXTINF:-1,{channel_name}\n')
                        output_file.write(f'{channel_link}\n')

                        # 匹配频道名称与 EPG 信息
                        for channel in epg_root.iter('channel'):
                            display_name = channel.find('display-name').text
                            if channel_name == display_name:
                                icon_element = channel.find('icon')
                                if icon_element is not None:
                                    icon_url = icon_element.attrib.get('src')
                                    if icon_url:
                                        output_file.write(f'#EXTIMG:{icon_url}\n')
                                programmes = channel.findall('programme')
                                if programmes:
                                    programme = programmes[0]
                                    epg_info = programme.attrib.get('title')
                                    output_file.write(f'#EXTGRP:{epg_info}\n')
                                break

        print(f"已转换文件：{filename}")

print('转换完成！')
