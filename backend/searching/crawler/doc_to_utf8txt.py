import os
import comtypes.client

path = r'C:\Users\admin\Desktop\RAGBOT\ChatBot_Law\backend\searching\crawler\22_VBHN-VPQH_651354.doc'
out = r'C:\Users\admin\Desktop\RAGBOT\ChatBot_Law\backend\searching\crawler\22_VBHN-VPQH_651354.txt'

wd = comtypes.client.CreateObject('Word.Application')
wd.Visible = False
doc = wd.Documents.Open(path)
text = doc.Content.Text
doc.Close()
wd.Quit()

with open(out, 'w', encoding='utf-8') as f:
    f.writelines(line + '\n' for line in text.splitlines())

print(f"Wrote UTF8 text to: {out}")