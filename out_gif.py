from PIL import Image, ImageDraw

s=24

st_list=['4005','4553','6758','7201','7309','8316','8411','9201','9202','9432','9437','9613','9983']
#st_list = ['AAL','AAPL','AMZN','FB','GOOG','ZM']
images = []
for i in st_list:
    st_name = i + '_trend_2020-06-11_'
    im = Image.open('./stock/stock0/{}.png'.format(st_name)) 
    im =im.resize(size=(2588, 1600), resample=Image.NEAREST)
    images.append(im)
    st_name = i + '_trend_2020-06-12_'
    im = Image.open('./stock/stock0/{}.png'.format(st_name)) 
    im =im.resize(size=(2588, 1600), resample=Image.NEAREST)
    images.append(im)
    
images[0].save('./stock/stock0/zm_T26.gif', save_all=True, append_images=images[1:s], duration=100*10, loop=0)
