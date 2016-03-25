#encoding:utf-8
import template
import render
import analyzer
import req_maker
import stinger

stylet=r'zzz&*^%$#<>zzuf\u0023%23\035\x3b&#23;&lt;zzz'

template_obj = template.URLTemplate('http://www.sanchuanshouhui.com/show.php?filename=165')
template_list = template_obj.get_url_fuzz_template()

render_obj = render.StyletURLRender(stylet=r'zzz&*^%$#<>zzuf\u0023%23\035\x3b&#23;&lt;zzz')
render_list = render_obj.get_stylet_payload(template_list)

for i in render_list:
    print i
    
reqset = req_maker.MultiReqMaker(urls=render_list,stylet=stylet)
tmp =  reqset.get_reqs()
for i in tmp:
    print i.method, i.url, i.cookies, i.stylet, i.post_data, i.headers
    
ret = stinger.MultiStingerMaker(Req_list = tmp)
stingers = ret.get_stingers()

pool = stinger.StingerPool(stingers=stingers)
pool.execute()

while True:
    pass
#req_maker