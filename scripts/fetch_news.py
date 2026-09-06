#!/usr/bin/env python3
import json, datetime, hashlib, re, urllib.request
import xml.etree.ElementTree as ET

FEEDS=[
('Anthropic News','https://www.anthropic.com/news/rss.xml'),
('Anthropic Engineering','https://www.anthropic.com/engineering/rss.xml'),
('OpenAI Blog','https://openai.com/news/rss.xml'),
('Google DeepMind','https://deepmind.google/blog/rss.xml'),
('Simon Willison (LLM/agents)','https://simonwillison.net/atom/everything/'),
('Hacker News - AI','https://hnrss.org/newest?q=Claude+Code+OR+agent+harness+OR+subagent&count=25')]
KEYWORDS=['claude code','subagent','sub-agent','harness','agent','mcp','llm','anthropic','openai','gemini','model context protocol','prompt','ai agent','coding agent','orquestra','orchestration']

def strip_html(text):
    text=re.sub(r'<[^>]+>','',text or '')
    return re.sub(r'\\s+',' ',text).strip()[:280]

def fetch_feed(name,url):
    items=[]
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (ia-diario-bot)'})
        root=ET.fromstring(urllib.request.urlopen(req,timeout=20).read())
        for item in root.findall('.//item')[:8]:
            title=(item.findtext('title') or '').strip();link=(item.findtext('link') or '').strip()
            if title and link: items.append({'source':name,'title':title,'link':link,'summary':strip_html(item.findtext('description')),'published':(item.findtext('pubDate') or '').strip()})
        ns={'a':'http://www.w3.org/2005/Atom'}
        for entry in root.findall('.//a:entry',ns)[:8]:
            title=(entry.findtext('a:title',namespaces=ns) or '').strip();el=entry.find('a:link',ns);link=el.get('href') if el is not None else ''
            if title and link: items.append({'source':name,'title':title,'link':link,'summary':strip_html(entry.findtext('a:summary',namespaces=ns) or entry.findtext('a:content',namespaces=ns)),'published':(entry.findtext('a:updated',namespaces=ns) or '').strip()})
    except Exception as e: items.append({'source':name,'title':f'[Falha ao buscar feed: {e}]','link':url,'summary':'','published':''})
    return items

def main():
    items=[];seen=set()
    for n,u in FEEDS: items.extend(fetch_feed(n,u))
    unique=[]
    for item in items:
        key=hashlib.sha1(item['title'].lower().encode()).hexdigest()
        if key not in seen: seen.add(key);unique.append(item)
    unique.sort(key=lambda x:sum(k in (x['title']+' '+x['summary']).lower() for k in KEYWORDS),reverse=True)
    now=datetime.datetime.now(datetime.timezone.utc)
    payload={'generated_at_utc':now.isoformat(),'generated_at_display':now.strftime('%d/%m/%Y %H:%M UTC'),'total_items':len(unique[:40]),'items':unique[:40]}
    with open('data/news.json','w',encoding='utf-8') as f: json.dump(payload,f,ensure_ascii=False,indent=2)
    print(f'OK: {payload["total_items"]} itens salvos em data/news.json')
if __name__=='__main__': main()
