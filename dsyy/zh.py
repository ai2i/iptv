import os

directory = os.getcwd()  # 获取当前目录

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

        print(f"已转换文件：{filename}")

print('转换完成！')
