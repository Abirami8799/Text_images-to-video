import os
from PIL import Image
import pandas as pd
import cairocffi
import pangocffi
import pangocairocffi
import pangocffi as pango
from moviepy.editor import *


def imagewidth(oldsize):    
  if oldsize[0]>300:
       return(300)
  else:
      return(oldsize[0])

def imageheight(oldsize):
   if oldsize[1]>200:
      return(200)
   else:
      return(oldsize[1])


def imageresize(oldim):
    old_size = oldim.size
    width=imagewidth(old_size)
    height=imageheight(old_size)
    resize_im= old_im.resize(((width), (height)))
    return resize_im


def imageside(newimage,number):
    new_size=newimage.size
    if (number%2)==0:
       new_width=430+((300-new_size[0])//2)
       new_height=120+((200-new_size[1])//2)
       return(new_width,new_height)
    else:
       new_width=50+((300-new_size[0])//2)
       new_height=120+((200-new_size[1])//2)
       return(new_width,new_height)
       
def rendering(n):
    if (n%2)==0:
       return context.translate(60,100)
    else:
       return context.translate(430,120)


col_list = ["S.no", "filename","content"]
df=pd.read_csv('demo.csv',usecols=col_list)
new=df.dropna()
#paste the old images in left,right side combination

for i,j in zip(new['S.no'], new['filename']):
    for root, dirs, files in os.walk("data", topdown=False):
        for name in files:
            if j == name:
               img=os.path.join(root,j)
               bg_size = (800, 400)
               bg_im = Image.new("RGB",bg_size,"white")
               old_im = Image.open(img)
               new_im=imageresize(old_im)  
               new_size=imageside(new_im,i)
               bg_im.paste(new_im, (new_size))
               bg_im.save("/home/abirami/Documents/python/imagetovideo/newdata/"+name)


#adding text on image
for i,j,k in zip(new['filename'],new['content'],new['S.no']):
    for root, dirs, files in os.walk("newdata", topdown=False):
        for name in files:
            if i == name:
               filename = os.path.join(root,i)
               surface = cairocffi.ImageSurface.create_from_png(filename)
               context = cairocffi.Context(surface)
               rendering(k)
               PANGO_SCALE = pango.units_from_double(1)
               WIDTH=300
               HEIGHT=200
               layout = pangocairocffi.create_layout(context)
               layout.set_markup('<span font="10">'+j+'</span>')
               layout.set_width(300*1000)
               ink_box,log_box = layout.get_extents()
               text_width,text_height = (1.0*log_box.width/PANGO_SCALE,
                          1.0*log_box.height/PANGO_SCALE)
               context.move_to(WIDTH/2-text_width/2, HEIGHT/2-text_height/2)
               pangocairocffi.show_layout(context, layout)
               surface.write_to_png(filename)
               surface.finish()


#images to video

clips = []

for root, dirs, files in os.walk("newdata", topdown=False):
    for name in files:
        clip=os.path.join(root,name)
        clips.append(ImageClip(clip).set_duration(6))



video_clip = concatenate_videoclips(clips, method='compose')

#add audio in video
audio = AudioFileClip('bgm.mp3')
final_video = video_clip.set_audio(audio)

final_video.write_videofile("img_to_video.mp4", fps = 24, remove_temp = True, codec = "libx264", audio_codec = "aac")
