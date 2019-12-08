from util_ptt import*
import re
postfix = []
# domain = 'https://www.ptt.cc/bbs/baseball/search'
default_url = 'http://i.imgur.com/CJ0YWZ3.jpg'

def get_recommend_link(domain,rank):
    desire_article_num = rank
    return 'link has been deleted' if postfix[desire_article_num]=='been deleted' else urllib.parse.urljoin(domain, postfix[desire_article_num])
def get_recommend_title(domain,pn):
    push_num = pn
    string = ''
    postfix.clear()
    res = requests.get(domain, params={'q':'recommend:'+str(push_num)}, cookies={'over18': '1'})
    #print(res.text)
    post_entries = parse_article_entries(res.text,'div.r-ent')

    metadata = [parse_article_meta(entry) for entry in post_entries]

    for meta in metadata:
        # meta is dictionary
        string += '['+meta['push']+'] '+meta['title']+'\n'
        postfix.append(meta['link'])
    return string
def get_beauty_url(domain,push_n,link_i,img_i):
    link_index = 0
    push_num = push_n
    link_index = link_i
    post_url = []
    li = []
    res = requests.get(domain, params={'q':'recommend:'+str(push_num)}, cookies={'over18': '1'})
    post_entries = parse_article_entries(res.text,'div.r-ent')
    metadata = [parse_article_meta(entry) for entry in post_entries]
    for meta in metadata:
        post_url.append(meta['link'])
    # error index, return defualt url
    if link_index > len(post_url):
        li.append(default_url)
        return li
    # get url, start to find image
    while post_url[link_index] == "been deleted":
        link_index += 1
    res = fetch(urllib.parse.urljoin(domain,post_url[link_index]))
    metap = parse_article_entries(res.text,'a')
    for i in metap:
        tmp = re.findall('https://imgur.com/.*|https://i.imgur.com/.*',i.attrs['href'])
        if tmp:
            li.extend(tmp)
    #print(li)
    return li[img_i]
    #return 'link has been deleted' if postfix[link_index]=='been deleted' else urllib.parse.urljoin(domain, postfix[link_index])
if __name__ == "__main__":
    url = get_beauty_url('https://www.ptt.cc/bbs/Beauty/search',50,0,0)
    l = url.split('/')
    print(l[-1])
    #print(get_recommend_title('https://www.ptt.cc/bbs/Beauty/search',50))
    #print(get_recommend_link('https://www.ptt.cc/bbs/baseball/search',0))
    #print(get_beauty_url('https://www.ptt.cc/bbs/Beauty/search',50,0))
    #print(get_recommend_title())
    #print(get_recommend_link(1))
    # rec_url = get_recommend_link(2)