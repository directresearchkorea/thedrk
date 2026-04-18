"""
Direct Research Korea — Blog Post Builder
==========================================
마크다운 파일에서 블로그 포스트 HTML을 자동 생성하는 도구

사용법:
  1. tools/posts/ 폴더에 마크다운 파일을 작성합니다.
  2. 마크다운 파일 상단에 메타데이터를 포함합니다 (아래 형식 참고)
  3. 이 스크립트를 실행하면 insights/[slug]/index.html이 자동 생성됩니다.

마크다운 파일 형식 (tools/posts/my-post.md):
  ---
  title: 포스트 제목
  description: 검색 결과에 표시될 설명 (160자 이내)
  category: gaming
  date: 2026-04-18
  slug: my-post-url
  ---
  
  본문 내용을 여기에 작성...
  
  ## 소제목
  
  본문 내용...

실행:
  python tools/build_post.py                    # 모든 포스트 빌드
  python tools/build_post.py my-post.md         # 특정 포스트만 빌드
"""

import os
import re
import sys
import json
from datetime import datetime
from pathlib import Path

# 경로 설정
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
POSTS_DIR = SCRIPT_DIR / "posts"
TEMPLATE_PATH = SCRIPT_DIR / "post-template.html"
OUTPUT_DIR = PROJECT_ROOT / "insights"
SITEMAP_PATH = PROJECT_ROOT / "sitemap.xml"
INSIGHTS_PAGE = OUTPUT_DIR / "index.html"


def parse_frontmatter(content):
    """마크다운 파일에서 프론트매터(메타데이터)와 본문을 분리"""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        print("  ⚠️  프론트매터를 찾을 수 없습니다. ---로 감싸진 메타데이터가 필요합니다.")
        return None, content
    
    meta_text = match.group(1)
    body = match.group(2)
    
    meta = {}
    for line in meta_text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            meta[key.strip()] = value.strip()
    
    return meta, body


def markdown_to_html(md_text):
    """간단한 마크다운 → HTML 변환기"""
    lines = md_text.strip().split('\n')
    html_lines = []
    in_list = False
    in_blockquote = False
    paragraph = []
    
    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            text = ' '.join(paragraph)
            text = convert_inline(text)
            html_lines.append(f'<p>{text}</p>')
            paragraph = []
    
    def convert_inline(text):
        # Bold: **text** or __text__
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__(.*?)__', r'<strong>\1</strong>', text)
        # Italic: *text* or _text_
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        # Links: [text](url)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        # Inline code: `code`
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        return text
    
    for line in lines:
        stripped = line.strip()
        
        # Empty line
        if not stripped:
            flush_paragraph()
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False
            continue
        
        # Headers
        if stripped.startswith('### '):
            flush_paragraph()
            text = convert_inline(stripped[4:])
            html_lines.append(f'<h3>{text}</h3>')
            continue
        if stripped.startswith('## '):
            flush_paragraph()
            text = convert_inline(stripped[3:])
            html_lines.append(f'<h2>{text}</h2>')
            continue
        
        # Blockquote
        if stripped.startswith('> '):
            flush_paragraph()
            if not in_blockquote:
                html_lines.append('<blockquote>')
                in_blockquote = True
            text = convert_inline(stripped[2:])
            html_lines.append(f'<p>{text}</p>')
            continue
        
        # Unordered list
        if stripped.startswith('- ') or stripped.startswith('• '):
            flush_paragraph()
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            text = convert_inline(stripped[2:])
            html_lines.append(f'<li>{text}</li>')
            continue
        
        # Image: ![alt](src)
        img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', stripped)
        if img_match:
            flush_paragraph()
            alt = img_match.group(1)
            src = img_match.group(2)
            html_lines.append(f'<img src="{src}" alt="{alt}" loading="lazy">')
            continue
        
        # Horizontal rule
        if stripped in ('---', '***', '___'):
            flush_paragraph()
            html_lines.append('<hr class="divider">')
            continue
        
        # Regular paragraph
        paragraph.append(stripped)
    
    flush_paragraph()
    if in_list:
        html_lines.append('</ul>')
    if in_blockquote:
        html_lines.append('</blockquote>')
    
    return '\n      '.join(html_lines)


def build_post(md_path):
    """마크다운 파일 → HTML 블로그 포스트 생성"""
    print(f"\n📝 빌드 중: {md_path.name}")
    
    content = md_path.read_text(encoding='utf-8')
    meta, body = parse_frontmatter(content)
    
    if not meta:
        print("  ❌ 메타데이터 없음 — 건너뜁니다.")
        return None
    
    # 필수 필드 확인
    required = ['title', 'description', 'category', 'date', 'slug']
    for field in required:
        if field not in meta:
            print(f"  ❌ 필수 필드 누락: {field}")
            return None
    
    # 본문을 HTML로 변환
    html_body = markdown_to_html(body)
    
    # 템플릿 로드
    template = TEMPLATE_PATH.read_text(encoding='utf-8')
    
    # 플레이스홀더 치환
    html = template.replace('%%TITLE%%', meta['title'])
    html = html.replace('%%DESCRIPTION%%', meta['description'])
    html = html.replace('%%SLUG%%', meta['slug'])
    html = html.replace('%%DATE%%', meta['date'])
    html = html.replace('%%CATEGORY%%', meta['category'].capitalize())
    html = html.replace('%%CONTENT%%', html_body)
    
    # 출력 디렉토리 생성
    output_dir = OUTPUT_DIR / meta['slug']
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'index.html'
    output_file.write_text(html, encoding='utf-8')
    
    print(f"  ✅ 생성: insights/{meta['slug']}/index.html")
    return meta


def update_sitemap(posts_meta):
    """sitemap.xml에 새 포스트 URL 추가"""
    if not posts_meta:
        return
    
    sitemap = SITEMAP_PATH.read_text(encoding='utf-8')
    
    for meta in posts_meta:
        url = f"https://thedrk.com/insights/{meta['slug']}/"
        if url not in sitemap:
            entry = f"""  <url>
    <loc>{url}</loc>
    <lastmod>{meta['date']}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>"""
            sitemap = sitemap.replace('</urlset>', f'{entry}\n</urlset>')
    
    SITEMAP_PATH.write_text(sitemap, encoding='utf-8')
    print(f"\n🗺️  sitemap.xml 업데이트 완료 ({len(posts_meta)}개 URL 추가)")


def main():
    print("=" * 50)
    print("🔨 Direct Research Korea — Blog Post Builder")
    print("=" * 50)
    
    # posts 디렉토리 확인
    if not POSTS_DIR.exists():
        POSTS_DIR.mkdir(parents=True)
        # 샘플 포스트 생성
        sample = POSTS_DIR / "sample-post.md"
        sample.write_text("""---
title: Sample Blog Post Title
description: This is a sample blog post for Direct Research Korea. Replace with your content.
category: gaming
date: 2026-04-18
slug: sample-post
---

This is your blog post content. Write in **markdown** format.

## Introduction

Start with an engaging introduction to your research topic.

## Key Findings

- Finding 1: Describe your first key finding
- Finding 2: Another important discovery
- Finding 3: Data-driven insight

## Analysis

Detailed analysis goes here. You can use **bold text** for emphasis, *italic* for nuance, and [links](https://thedrk.com) to reference sources.

> Important quotes or callouts can be formatted as blockquotes.

## Conclusion

Wrap up with actionable insights and next steps.
""", encoding='utf-8')
        print(f"\n📁 posts 디렉토리 생성: {POSTS_DIR}")
        print(f"📄 샘플 포스트 생성: sample-post.md")
        print(f"\n💡 사용법:")
        print(f"   1. {POSTS_DIR} 에 .md 파일을 작성하세요")
        print(f"   2. python tools/build_post.py 를 실행하세요")
        return
    
    # 특정 파일만 빌드하거나 전체 빌드
    if len(sys.argv) > 1:
        md_files = [POSTS_DIR / sys.argv[1]]
    else:
        md_files = sorted(POSTS_DIR.glob('*.md'))
    
    if not md_files:
        print("\n⚠️  포스트 파일이 없습니다.")
        print(f"   {POSTS_DIR} 에 .md 파일을 추가하세요.")
        return
    
    print(f"\n📂 {len(md_files)}개 파일 발견")
    
    built = []
    for md_path in md_files:
        if md_path.exists():
            meta = build_post(md_path)
            if meta:
                built.append(meta)
        else:
            print(f"\n❌ 파일 없음: {md_path}")
    
    # sitemap 업데이트
    if built:
        update_sitemap(built)
    
    print(f"\n{'=' * 50}")
    print(f"✨ 완료! {len(built)}개 포스트 빌드됨")
    print(f"{'=' * 50}")


if __name__ == '__main__':
    main()
