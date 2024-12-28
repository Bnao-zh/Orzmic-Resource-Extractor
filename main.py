import os,sys
import UnityPy
import zipfile

file_apk = sys.argv[1]
DECRYPT_KEY = b"Big_True'sOrzmic"
UnityPy.set_assetbundle_decrypt_key(DECRYPT_KEY)

def createDirectory(directory: str):
    # 确保目录存在
    if not os.path.exists(directory):
        os.makedirs(directory)


def saveIll():
    with zipfile.ZipFile(file_apk) as apk:
        all_entries = apk.namelist()
        for entry in all_entries:
            if entry.startswith('assets/charts/'): 
                with apk.open(entry) as f:
                    # 加载Unity资源
                    env = UnityPy.load(f)
                    for obj in env.objects:
                        data = obj.read()

                        # 尝试导出曲绘文件
                        if obj.type.name == "Sprite":
                            directory = f"covers"
                            createDirectory(directory)
                            path = os.path.join(directory, f"{data.m_Name}.png")
                            print(f"导出曲绘 {data.m_Name}")
                            data.image.save(path)
                        
                        # 尝试导出谱面文件
                        if obj.type.name == "TextAsset":
                            directory = f"charts"
                            createDirectory(directory)
                            path = os.path.join(directory, f"{data.m_Name}.txt")
                            print(f"导出谱面 {data.m_Name}")
                            with open(path, "wb") as f:
                                f.write(data.m_Script.encode("utf-8", "surrogateescape"))
                            
              
def saveClips():
    directory = f"clips"
    createDirectory(directory)
    with zipfile.ZipFile(file_apk) as apk:
        all_entries = apk.namelist()
        for entry in all_entries:
            if entry.startswith('assets/clips/'):
                with apk.open(entry) as f:
                    env = UnityPy.load(f)
                    for obj in env.objects:
                        if obj.type.name in ["AudioClip"]:
                            clip = obj.read()

                            # 尝试导出音频文件
                            for name, data in clip.samples.items():
                                print(f"导出音频 {name}")
                                with open(f"{directory}/{name}", "wb") as f:
                                    f.write(data)
   
       
if __name__ == "__main__":
        print("Orzmic resource extractor v1")
        print("=====================================")
        print("开始提取Orzmic资源")
        print("=====================================")
        print("开始提取音频")
        saveClips()
        print("=====================================")
        print("开始提取谱面和曲绘")
        saveIll()
        print("=====================================")
        print("所有资源提取完成")
        print("=====================================")