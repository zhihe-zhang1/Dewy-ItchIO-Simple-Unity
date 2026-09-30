from pathlib import Path
from playwright.sync_api import sync_playwright
import json, hashlib, shutil, os
from PIL import Image

source=Path(__file__).resolve().parents[1] / 'SourceReference' / 'index.html'
root=Path(__file__).resolve().parents[1]
(root/'Assets/Resources/Pages').mkdir(parents=True,exist_ok=True)
html=source.read_text(encoding='utf8')
nav={}
with sync_playwright() as p:
 browser_args={'headless': True, 'args': ['--no-sandbox','--disable-dev-shm-usage']}
 chrome=os.environ.get('CHROME_PATH') or shutil.which('chromium') or shutil.which('google-chrome')
 if chrome: browser_args['executable_path']=chrome
 browser=p.chromium.launch(**browser_args)
 page=browser.new_page(viewport={'width':900,'height':896}, device_scale_factor=2)
 page.set_content(html,wait_until='load')
 page.locator('.book').wait_for()
 for i in range(6):
  page.evaluate('(i)=>document.querySelectorAll(".page").forEach((p,j)=>p.classList.toggle("active",i===j))',i)
  page.wait_for_timeout(100)
  book=page.locator('.book')
  bounds=book.bounding_box()
  buttons=page.locator('.page.active button[data-go]')
  nav[i]=[]
  for j in range(buttons.count()):
   b=buttons.nth(j)
   bb=b.bounding_box()
   dest=int(b.get_attribute('data-go'))
   nav[i].append({'label':b.inner_text(),'go':dest,'x':round(bb['x']-bounds['x'],3),'y':round(bb['y']-bounds['y'],3),'w':round(bb['width'],3),'h':round(bb['height'],3)})
  fn=root/f'Assets/Resources/Pages/Page{i}.png'
  book.screenshot(path=str(fn),animations='disabled',scale='css')
  im=Image.open(fn)
  assert im.size==(430,862), (fn,im.size)
  # high fidelity full-resolution capture, lossless PNG (not quantized)
  print(i, im.size, fn.stat().st_size, nav[i])
 browser.close()
(root/'SourceReference/navigation.json').write_text(json.dumps(nav,indent=2),encoding='utf8')
print('HTML SHA256',hashlib.sha256(source.read_bytes()).hexdigest())
