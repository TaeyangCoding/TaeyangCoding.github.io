#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the two static catalog entry points from the same reviewed app data."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'apps/apps.json').read_text())
APPS = DATA['apps']
e = lambda value: html.escape(str(value), quote=True)
APPLE = '<svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M13.7 4.1c.8-.9 1.2-2 1.1-3.1-1.1.1-2.4.7-3.1 1.6-.7.8-1.3 2-1.1 3.1 1.2.1 2.3-.6 3.1-1.6M16.7 10.5c0-2 1.7-3 1.8-3.1-1-1.4-2.5-1.6-3-1.6-1.3-.1-2.5.8-3.2.8-.6 0-1.6-.8-2.7-.7-1.4 0-2.7.8-3.4 2-1.4 2.4-.4 5.9.9 7.8.6.9 1.3 1.8 2.3 1.8 1 0 1.3-.6 2.6-.6 1.2 0 1.6.6 2.7.6s1.7-1 2.3-1.8c.7-1 1-1.9 1-2-1.1-.5-1.8-1.7-1.8-3.2"/></svg>'

def nav():
    return '<a class="skip" href="#content">본문으로 건너뛰기</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="/" aria-label="태양코딩 홈"><img src="/apps/sun.svg" width="35" height="35" alt="">태양코딩</a><nav aria-label="주요 메뉴"><a href="#apps">앱 둘러보기</a><a href="#support">고객지원</a><a class="nav-contact" href="mailto:taeyang1238@icloud.com">문의하기 ↗</a></nav></div></header>'

def footer():
    return '<footer class="wrap site-footer"><span>© 2026 태양코딩 · 작은 앱으로, 조금 더 편한 하루.</span><div class="footer-links"><a href="/apps/">다운로드 모음</a><a href="https://apps.apple.com/kr/developer/id6808828707">App Store 개발자 ↗</a><a href="/app-ads.txt">app-ads.txt</a></div></footer>'

def card(a):
    stores = ''
    if a['stores']['apple']['status'] == 'public':
        stores += '<a class="store-button apple-store" href="'+e(a['stores']['apple']['url'])+'" aria-label="'+e(a['name'])+' App Store에서 보기">'+APPLE+'App Store <span aria-hidden="true">↗</span></a>'
    else:
        stores += '<span class="store-button apple-store">App Store · 공개 준비 중</span>'
    google = a['stores'].get('google')
    if google and google['status'] == 'public':
        stores += '<a class="store-button" href="'+e(google['url'])+'" aria-label="'+e(a['name'])+' Google Play에서 보기">Google Play ↗</a>'
    if google and google['status'] != 'public': stores += '<span class="store-button google-pending" hidden>Google Play · 공개 준비 중</span>'
    notes = []
    if a['stores']['apple']['status'] != 'public': notes.append('공개되면 다운로드 링크를 안내할게요.')
    if google and google['status'] != 'public': notes.append('Android · Google Play 공개 준비 중')
    labels = {'ios':'iPhone · iPad','mac':'Mac'}
    platforms = ''.join('<span>'+labels[p]+'</span>' for p in a['platforms'] if p in labels)
    support = '<a href="'+e(a['support'])+'">고객지원 ↗</a>'
    if a.get('privacy'): support += '<a href="'+e(a['privacy'])+'">개인정보</a>'
    if a.get('androidPrivacy'): support += '<a href="'+e(a['androidPrivacy'])+'">Android 개인정보</a>'
    if a.get('terms'): support += '<a href="'+e(a['terms'])+'">이용약관</a>'
    search = (a['name']+a['category']+a['description']).lower().replace(' ','')
    return '<article class="app-card" data-platforms="'+e(' '.join(a['platforms']))+'" data-search="'+e(search)+'"><div class="card-head"><img class="app-icon" src="'+e(a['icon'])+'" width="64" height="64" alt="" loading="lazy"><span class="category">'+e(a['category'])+'</span></div><h3>'+e(a['name'])+'</h3><p class="app-desc">'+e(a['description'])+'</p><div class="platforms">'+platforms+'</div><div class="store-links">'+stores+'</div>'+(''.join('<p class="release-note">'+e(n)+'</p>' for n in notes))+'<div class="support-links">'+support+'</div></article>'

def page(download=False):
    title = '태양코딩 · 앱 다운로드와 고객지원' if download else '태양코딩 · 일상을 밝히는 작은 앱들'
    canonical = 'https://taeyangcoding.github.io/apps/' if download else 'https://taeyangcoding.github.io/'
    hero_icons = [APPS[i] for i in [0,2,4,5,3]]
    artwork = '<div class="hero-art" aria-hidden="true"><div class="sun-disc"></div>'+''.join('<div class="float-icon"><img src="'+a['icon']+'" width="74" height="74" alt=""></div>' for a in hero_icons)+'<span class="art-spark">✳</span><span class="art-dot"></span><span class="art-label">A little brighter, every day.</span></div>'
    filters = ''.join('<button class="filter" type="button" data-filter="'+p+'" aria-pressed="'+('true' if p=='all' else 'false')+'">'+label+'</button>' for p,label in [('all','전체 11'),('ios','iPhone · iPad'),('mac','Mac'),('android','Android')])
    return '<!doctype html>\n<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f7f7f2"><title>'+title+'</title><meta name="description" content="태양코딩의 11개 앱을 만나보세요. 공식 App Store 다운로드, Android 공개 준비 안내와 앱별 고객지원을 한곳에서 확인하세요."><link rel="canonical" href="'+canonical+'"><link rel="icon" href="/apps/sun.svg" type="image/svg+xml"><meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:title" content="'+title+'"><meta property="og:description" content="작은 앱으로, 조금 더 편한 하루. 앱 다운로드와 고객지원을 한곳에서."><meta property="og:url" content="'+canonical+'"><meta property="og:image" content="https://taeyangcoding.github.io/apps/assets/social-refresh.jpg"><meta property="og:image:alt" content="태양코딩 · 일상을 밝히는 작은 앱들"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="/assets/site.css"><script src="/assets/site.js" defer></script></head><body>'+nav()+'<main id="content"><div class="wrap"><section class="hero" aria-labelledby="hero-title"><div><div class="eyebrow">SMALL APPS, EVERYDAY JOY</div><h1 id="hero-title">일상에 필요한<br><em>작은 도구들.</em></h1><p>말씀을 가까이 두고, 소중한 기록을 모으고,<br>매일의 일을 조금 더 가볍게.<br>태양코딩이 하나씩 만들고 다듬는 앱들입니다.</p><div class="hero-actions"><a class="primary" href="#apps">내게 맞는 앱 찾기 <span aria-hidden="true">↓</span></a><a class="text-link" href="#support">도움이 필요하신가요?</a></div><p class="hero-caption">MADE WITH CARE · TAEYANG CODING</p></div>'+artwork+'</section><div class="intro-line"><p><strong>11개의 앱, 저마다의 쓰임.</strong> &nbsp; 다운로드부터 고객지원까지 한곳에서 만나보세요.</p><span>iPhone · iPad · Mac · Android</span></div><section id="apps" class="catalog" aria-labelledby="apps-title"><div class="section-top"><div><div class="eyebrow">OUR APPS</div><h2 id="apps-title">어떤 하루를 만들고 싶으세요?</h2></div><p id="result-status" role="status" aria-live="polite">11개의 앱</p></div><div class="toolbar"><div class="filters" role="group" aria-label="플랫폼으로 앱 찾기">'+filters+'</div><label class="search" for="app-search"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg><input type="search" id="app-search" placeholder="앱 이름이나 용도로 검색" aria-label="앱 이름이나 용도로 검색"></label></div><div class="app-grid">'+''.join(card(a) for a in APPS)+'</div><p id="empty-state" class="empty" hidden>검색 결과가 없어요. 다른 이름이나 용도로 찾아보세요.</p><noscript><p class="catalog-note">전체 앱과 링크를 바로 이용할 수 있습니다. 검색과 플랫폼 필터는 JavaScript를 켜면 사용할 수 있어요.</p></noscript><p class="catalog-note">App Store 버튼은 현재 한국 스토어에서 공개된 앱으로 연결됩니다. 공개 준비 중인 앱은 다운로드 버튼 대신 상태를 안내해요. Google Play 공개 다운로드는 아직 제공하지 않으며, Android 필터에서 준비 중인 7개 앱과 개인정보 안내를 확인할 수 있어요. 제공 지역과 지원 기기는 각 스토어에서 확인해 주세요.</p></section><section class="tools" aria-labelledby="tools-title"><h2 id="tools-title" class="tools-head">함께 만드는 Mac 도구</h2><div class="tool-grid"><article class="tool-card"><span class="tool-letter" aria-hidden="true">ㅎ</span><div><h3>한글 플러스</h3><p>Mac용 한글 문서 작업을 돕는 도구</p></div><a href="mailto:taeyang1238@icloud.com?subject=%ED%95%9C%EA%B8%80%20%ED%94%8C%EB%9F%AC%EC%8A%A4%20%EB%AC%B8%EC%9D%98">이용 문의 ↗</a></article><article class="tool-card"><span class="tool-letter" aria-hidden="true">P</span><div><h3>Pages Plus</h3><p>Mac용 Pages 문서 작업을 돕는 도구</p></div><a href="mailto:taeyang1238@icloud.com?subject=Pages%20Plus%20%EB%AC%B8%EC%9D%98">이용 문의 ↗</a></article></div></section></div><section id="support" class="support" aria-labelledby="support-title"><div class="wrap support-inner"><div><div class="eyebrow">HERE TO HELP</div><h2 id="support-title">잘 쓰실 수 있도록,<br>함께 살펴볼게요.</h2><p>각 앱 카드의 고객지원에서 사용 방법을 찾아보세요.<br>해결되지 않는 문제가 있다면 이메일로 알려 주세요.</p><a class="email" href="mailto:taeyang1238@icloud.com">taeyang1238@icloud.com ↗</a></div><div class="help-steps"><h3>이렇게 알려주시면 도움이 돼요</h3><ol><li>이용 중인 앱 이름과 버전</li><li>기기 모델과 운영체제 버전</li><li>문제가 발생한 화면과 재현 순서</li></ol><p class="privacy-note">비밀번호·인증번호·개인 문서와 사진은 보내지 마세요.<br>화면을 첨부할 때는 개인정보를 가려 주세요.</p></div></div></section></main>'+footer()+'</body></html>\n'

if __name__ == '__main__':
    (ROOT / 'index.html').write_text(page())
    (ROOT / 'apps/index.html').write_text(page(True))
    print('Built homepage and download catalog: '+str(len(APPS))+' apps')
