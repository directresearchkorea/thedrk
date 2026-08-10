---
marp: true
theme: default
paginate: true
header: '<div class="header-inner"><span>Direct Research Korea (DRK)</span><div class="lang-selector"><button data-lang="en" onclick="setLanguage(&apos;en&apos;)">EN</button><button data-lang="ko" onclick="setLanguage(&apos;ko&apos;)">KO</button><button data-lang="ja" onclick="setLanguage(&apos;ja&apos;)">JA</button><button data-lang="cn" onclick="setLanguage(&apos;cn&apos;)">CN</button></div></div><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" onload="if(!window.setLanguage){window.setLanguage=function(lang){document.body.className=&apos;lang-active-&apos;+lang;window.dispatchEvent(new Event(&apos;resize&apos;));};var s=document.createElement(&apos;style&apos;);s.innerHTML=&apos;.lang-ko,.lang-ja,.lang-cn{display:none!important;}.lang-en{display:block!important;}span.lang-en,strong.lang-en,a.lang-en{display:inline!important;}body.lang-active-en .lang-ko,body.lang-active-en .lang-ja,body.lang-active-en .lang-cn{display:none!important;}body.lang-active-en .lang-en{display:block!important;}body.lang-active-en span.lang-en,body.lang-active-en strong.lang-en,body.lang-active-en a.lang-en{display:inline!important;}body.lang-active-ko .lang-en,body.lang-active-ko .lang-ja,body.lang-active-ko .lang-cn{display:none!important;}body.lang-active-ko .lang-ko{display:block!important;}body.lang-active-ko span.lang-ko,body.lang-active-ko strong.lang-ko,body.lang-active-ko a.lang-ko{display:inline!important;}body.lang-active-ja .lang-en,body.lang-active-ja .lang-ko,body.lang-active-ja .lang-cn{display:none!important;}body.lang-active-ja .lang-ja{display:block!important;}body.lang-active-ja span.lang-ja,body.lang-active-ja strong.lang-ja,body.lang-active-ja a.lang-ja{display:inline!important;}body.lang-active-cn .lang-en,body.lang-active-cn .lang-ko,body.lang-active-cn .lang-ja{display:none!important;}body.lang-active-cn .lang-cn{display:block!important;}body.lang-active-cn span.lang-cn,body.lang-active-cn strong.lang-cn,body.lang-active-cn a.lang-cn{display:inline!important;}.header-inner{display:flex!important;justify-content:space-between!important;align-items:center!important;width:100%!important;}.lang-selector{display:flex!important;flex-direction:row!important;flex-wrap:nowrap!important;gap:6px!important;background:#E2E2E2!important;padding:2px 4px!important;border-radius:6px!important;align-items:center!important;}section.dark .lang-selector{background:#333339!important;}.lang-selector button{background:transparent!important;border:none!important;padding:4px 10px!important;font-size:11px!important;font-weight:700!important;cursor:pointer!important;border-radius:4px!important;color:#555555!important;transition:all 0.2s ease!important;outline:none!important;display:inline-block!important;line-height:1.2!important;margin:0!important;}section.dark .lang-selector button{color:#CCCCCC!important;}body.lang-active-en button[data-lang=en],body.lang-active-ko button[data-lang=ko],body.lang-active-ja button[data-lang=ja],body.lang-active-cn button[data-lang=cn]{background:#111111!important;color:#FFFFFF!important;}body.lang-active-en section.dark button[data-lang=en],body.lang-active-ko section.dark button[data-lang=ko],body.lang-active-ja section.dark button[data-lang=ja],body.lang-active-cn section.dark button[data-lang=cn]{background:#FFFFFF!important;color:#111111!important;}&apos;;document.head.appendChild(s);document.body.className=&apos;lang-active-en&apos;;}" style="display:none;" />'
footer: 'Research 2 Action | Direct Research Korea'
style: |
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;700;900&display=swap');
  
  section {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #F5F6F8;
    color: #111111;
    padding: 55px 80px 45px 80px;
    font-size: 17px;
    line-height: 1.5;
  }
  
  h1, h2, h3, h4, h5 {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #111111;
    font-weight: 700;
  }
  
  h1 {
    font-size: 34px;
    margin-top: 5px;
    margin-bottom: 15px;
    letter-spacing: -1px;
    line-height: 1.25;
  }
  
  h2 {
    font-size: 26px;
    margin-top: 5px;
    margin-bottom: 12px;
    letter-spacing: -0.5px;
    border-bottom: 2px solid #C92A2A;
    padding-bottom: 4px;
    display: inline-block;
  }
  
  h3 {
    font-size: 19px;
    color: #555555;
    margin-top: 0;
    margin-bottom: 10px;
    font-weight: 500;
  }
  
  footer, header {
    color: #999999;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
  }
  
  footer {
    border-top: 1px solid #E2E2E2;
    padding-top: 8px;
  }
  
  a {
    color: #111111;
    text-decoration: underline;
    font-weight: 600;
  }
  
  ul {
    margin-top: 5px;
    padding-left: 20px;
  }
  
  li {
    margin-bottom: 6px;
  }
  
  strong {
    color: #C92A2A;
    font-weight: 700;
    background: transparent;
  }
  
  .highlight {
    background-color: #FFFFFF;
    padding: 15px 20px;
    border-left: 4px solid #C92A2A;
    font-size: 16px;
    font-weight: 500;
    margin-bottom: 15px;
    border-radius: 0 6px 6px 0;
    border-top: 1px solid #E5E8EB;
    border-right: 1px solid #E5E8EB;
    border-bottom: 1px solid #E5E8EB;
    box-shadow: 0 2px 6px rgba(0,0,0,0.02);
  }

  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    margin-top: 15px;
  }
  
  .grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 20px;
    margin-top: 15px;
  }
  
  .grid-4 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 15px;
    margin-top: 15px;
  }

  .card {
    background-color: #FFFFFF;
    padding: 20px;
    border: 1px solid #E5E8EB;
    border-radius: 6px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    border-top: 3px solid #C92A2A;
  }

  .card.neutral {
    border-top-color: #E2E2E2;
  }

  .card h4 {
    margin-top: 0;
    font-size: 16px;
    font-weight: 700;
    color: #111111;
    margin-bottom: 8px;
  }
  
  .card h3 {
    color: #111111;
    border-bottom: 1px solid #E5E8EB;
    padding-bottom: 6px;
    margin-bottom: 10px;
    font-size: 18px;
    font-weight: 700;
  }
  
  .chevron-flow {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 15px;
    margin-top: 15px;
  }
  
  .chevron-item {
    background: #FFFFFF;
    border: 1px solid #E5E8EB;
    border-radius: 6px;
    padding: 15px 20px;
    position: relative;
    box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    border-left: 4px solid #C92A2A;
  }
  
  .chevron-item h3 {
    font-size: 17px;
    color: #C92A2A;
    font-weight: 700;
    margin-bottom: 8px;
    border-bottom: none;
    padding-bottom: 0;
  }
  
  .chevron-item .step-num {
    font-family: 'Outfit', sans-serif;
    font-size: 24px;
    font-weight: 900;
    color: #E5E8EB;
    position: absolute;
    top: 10px;
    right: 15px;
  }
  
  /* Dark slide classes (Cover & Closing) */
  section.dark {
    background-color: #1E1E24;
    color: #FFFFFF;
  }
  
  section.dark h1, section.dark h2, section.dark h3, section.dark h4 {
    color: #FFFFFF;
  }
  
  section.dark h2 {
    border-bottom-color: #C92A2A;
  }
  
  section.dark footer {
    border-top-color: #333339;
  }
  
  section.dark a {
    color: #FFFFFF;
  }
  
  section.dark .highlight {
    background-color: #2A2A30;
    border-left-color: #C92A2A;
    border-color: #3E3E46;
  }
  
  section.dark .card {
    background-color: #2A2A30;
    border-color: #3E3E46;
  }
  
  section.dark .card h3, section.dark .card h4 {
    color: #FFFFFF;
  }
  
  section.dark .card h3 {
    border-bottom-color: #3E3E46;
  }
---

<!-- 
_class: dark
_paginate: false 
_footer: ''
-->

<div class="lang-en" style="margin-top: 40px;">
  <h3>Direct Research Korea</h3>
  <h1 style="font-size: 44px; margin-bottom: 20px;">Decoding Korean Consumers</h1>
  <h3>User Insight & Qualitative Research Solutions</h3>
  <br>
  Presented by <strong>Jay Ahn</strong> (CEO & Project Director)
</div>

<div class="lang-ko" style="margin-top: 40px;">
  <h3>Direct Research Korea</h3>
  <h1 style="font-size: 44px; margin-bottom: 20px;">한국 소비자 디코딩</h1>
  <h3>소비자 인사이트 및 정성 리서치 솔루션</h3>
  <br>
  발표자: <strong>안재윤</strong> (CEO & 프로젝트 총괄 디렉터)
</div>

<div class="lang-ja" style="margin-top: 40px;">
  <h3>Direct Research Korea</h3>
  <h1 style="font-size: 44px; margin-bottom: 20px;">韓国消費者のデコーディング</h1>
  <h3>消費者インサイト＆定性調査ソリューション</h3>
  <br>
  発表者: <strong>ジェ이・アン</strong> (CEO & プロジェクト統括)
</div>

<div class="lang-cn" style="margin-top: 40px;">
  <h3>Direct Research Korea</h3>
  <h1 style="font-size: 44px; margin-bottom: 20px;">解码韩国消费者</h1>
  <h3>消费者洞察与定性研究解决方案</h3>
  <br>
  报告人: <strong>安杰伦</strong> (CEO & 项目总监)
</div>

---

## Presenter: Jay Ahn

<div class="lang-en">
  <h3>CEO & Project Management Director, DRK</h3>
  <div class="grid-2">
    <div>
      <h4><strong>Profile & Expertise</strong></h4>
      <ul>
        <li><strong>14+ Years</strong> of Marketing & Consumer Research experience</li>
        <li>Specializes in <strong>Qualitative-led Insight</strong> and <strong>UI/UX Usability Testing (UT)</strong></li>
        <li>Active contributor to the global research community (<strong>ESOMAR Speaker</strong>)</li>
        <li>Developer of advanced qualitative research workflows utilizing <strong>AI/Custom GPTs</strong></li>
      </ul>
    </div>
    <div class="card">
      <h4><strong>Education & Network</strong></h4>
      <ul>
        <li><strong>MBA</strong> | Kongju National University (Graduate School of Business)</li>
        <li><strong>B.S. in Business Marketing</strong> | Liberty University, USA</li>
        <li><strong>LinkedIn</strong>: <a href="https://www.linkedin.com/in/jayahn/" target="_blank">linkedin.com/in/jayahn</a></li>
      </ul>
    </div>
  </div>
</div>

<div class="lang-ko">
  <h3>DRK 대표 및 프로젝트 총괄 디렉터</h3>
  <div class="grid-2">
    <div>
      <h4><strong>프로필 및 전문 분야</strong></h4>
      <ul>
        <li><strong>14년 이상</strong>의 마케팅 및 소비자 리서치 경력</li>
        <li>정성 조사 기반의 <strong>인사이트 발굴</strong> 및 <strong>UI/UX 사용성 테스트(UT)</strong> 전문</li>
        <li>글로벌 리서치 학회 활발한 참여 (<strong>ESOMAR 발표자</strong>)</li>
        <li>AI 및 커스텀 GPT를 활용한 선진 정성 조사 워크플로우 개발</li>
      </ul>
    </div>
    <div class="card">
      <h4><strong>학력 및 네트워크</strong></h4>
      <ul>
        <li><strong>경영학 석사 (MBA)</strong> | 공주대학교 경영대학원</li>
        <li><strong>경영마케팅 학사 (B.S.)</strong> | 미국 리버티 대학교</li>
        <li><strong>LinkedIn</strong>: <a href="https://www.linkedin.com/in/jayahn/" target="_blank">linkedin.com/in/jayahn</a></li>
      </ul>
    </div>
  </div>
</div>

<div class="lang-ja">
  <h3>DRK 대표 兼 プロジェクト統括</h3>
  <div class="grid-2">
    <div>
      <h4><strong>プロフィールと専門性</strong></h4>
      <ul>
        <li><strong>14年以上</strong>のマーケティング＆消費者調査の経歴</li>
        <li>定性調査主導의 <strong>インサイト発掘</strong>および<strong>UI/UXユーザビリティテスト(UT)</strong>専門</li>
        <li>グローバル調査学会への活発な参画 (<strong>ESOMAR スピーカー</strong>)</li>
        <li>AIおよびカスタムGPTを活用した高度な定性調査ワークフローの開発</li>
      </ul>
    </div>
    <div class="card">
      <h4><strong>学歴およびネットワーク</strong></h4>
      <ul>
        <li><strong>経営学修士 (MBA)</strong> | 公州大学校経営大学院</li>
        <li><strong>経営マーケティング学士 (B.S.)</strong> | 米国リバティ大学</li>
        <li><strong>LinkedIn</strong>: <a href="https://www.linkedin.com/in/jayahn/" target="_blank">linkedin.com/in/jayahn</a></li>
      </ul>
    </div>
  </div>
</div>

<div class="lang-cn">
  <h3>DRK 总裁兼项目总监</h3>
  <div class="grid-2">
    <div>
      <h4><strong>个人简介与专业领域</strong></h4>
      <ul>
        <li><strong>14年以上</strong>市场与消费者研究经验</li>
        <li>专注于定性研究导向的<strong>洞察</strong>与 <strong>UI/UX 可用性测试(UT)</strong></li>
        <li>积极参与全球研究社群 (<strong>ESOMAR 发言人</strong>)</li>
        <li>结合 AI/定制化 GPT 开发先进的定性研究工作流</li>
      </ul>
    </div>
    <div class="card">
      <h4><strong>教育背景与人脉网络</strong></h4>
      <ul>
        <li><strong>工商管理硕士 (MBA)</strong> | 公州大学研究生院</li>
        <li><strong>商业营销学士 (B.S.)</strong> | 美国自由大学</li>
        <li><strong>LinkedIn</strong>: <a href="https://www.linkedin.com/in/jayahn/" target="_blank">linkedin.com/in/jayahn</a></li>
      </ul>
    </div>
  </div>
</div>

---

## Direct Research Korea (DRK)

<div class="lang-en">
  <h3>Connecting Global Brands with Korean Consumers</h3>
  <div class="grid-2">
    <div>
      <h4><strong>Who We Are</strong></h4>
      <ul>
        <li>Founded in <strong>2015</strong> as an independent consumer insight & UX research agency.</li>
        <li>Led by senior researchers with backgrounds from global firms (<strong>Nielsen, Ipsos, Kantar</strong>).</li>
        <li>Specialized in decoding local culture to guide global brand strategies in South Korea.</li>
      </ul>
    </div>
    <div class="card">
      <h4><strong>Industry Experience</strong></h4>
      <ul>
        <li><strong>FMCG & Retail</strong>: Trend analysis & concept tests</li>
        <li><strong>Gaming & Tech</strong>: Playtesting & UI/UX UT</li>
        <li><strong>Fashion & Beauty</strong>: Digital culture & persona mapping</li>
        <li><strong>Sports & Lifestyle</strong>: Tailored insights for global brands</li>
      </ul>
    </div>
  </div>
</div>

<div class="lang-ko">
  <h3>글로벌 브랜드와 한국 소비자의 연결</h3>
  <div class="grid-2">
    <div>
      <h4><strong>회사 소개</strong></h4>
      <ul>
        <li><strong>2015년</strong> 설립된 독립 소비자 인사이트 및 UX 리서치 전문 에이전시</li>
        <li>글로벌 조사 기관(<strong>Nielsen, Ipsos, Kantar</strong>) 출신의 시니어 연구원들로 구성</li>
        <li>한국 시장에 진출하는 글로벌 브랜드의 전략 수립을 위한 현지 문화 디코딩 전문</li>
      </ul>
    </div>
    <div class="card">
      <h4><strong>산업 영역 경험</strong></h4>
      <ul>
        <li><strong>FMCG 및 리테일</strong>: 트렌드 분석 및 컨셉 테스트</li>
        <li><strong>게임 및 IT 기술</strong>: 플레이테스트 및 UI/UX UT</li>
        <li><strong>패션 및 뷰티</strong>: 디지털 문화 및 페르소나 매핑</li>
        <li><strong>스포츠 및 라이프스타일</strong>: 글로벌 브랜드를 위한 맞춤형 인사이트 제공</li>
      </ul>
    </div>
  </div>
</div>

<div class="lang-ja">
  <h3>グローバルブランドと韓国消費者の架け橋</h3>
  <div class="grid-2">
    <div>
      <h4><strong>会社概要</strong></h4>
      <ul>
        <li><strong>2015년</strong>에 설립された独立系消費者インサイト＆UXリサーチ専門エージェンシー</li>
        <li>グローバル調査会社(<strong>Nielsen, Ipsos, Kantar</strong>)出身のシニア研究員が主導</li>
        <li>韓国市場におけるグローバルブランドの戦略立案に向けた現地文化のデコーディング専門</li>
      </ul>
    </div>
    <div class="card">
      <h4><strong>業界実績</strong></h4>
      <ul>
        <li><strong>FMCG＆リテール</strong>: トレンド分析およびコンセプトテスト</li>
        <li><strong>ゲーム＆テック</strong>: プレイテストおよびUI/UX UT</li>
        <li><strong>ファッション＆ビューティー</strong>: デジタルカルチャーおよびペルソナマッピング</li>
        <li><strong>スポーツ＆ライフスタイル</strong>: グローバルアパレルブランド向けの最適化インサイト</li>
      </ul>
    </div>
  </div>
</div>

<div class="lang-cn">
  <h3>连接全球品牌与韩国消费者</h3>
  <div class="grid-2">
    <div>
      <h4><strong>公司简介</strong></h4>
      <ul>
        <li>成立于<strong>2015年</strong>的独立消费者洞察与UX研究机构</li>
        <li>由来自全球知名研究公司(<strong>尼尔森、益谱索、凯度</strong>)的资深研究员领导</li>
        <li>专注于解码本土文化，为全球品牌在韩国的市场策略提供指引</li>
      </ul>
    </div>
    <div class="card">
      <h4><strong>行业经验</strong></h4>
      <ul>
        <li><strong>快速消费品与零售</strong>: 趋势分析与概念测试</li>
        <li><strong>游戏与科技</strong>: 游戏测试与 UI/UX 可用性测试</li>
        <li><strong>时尚与美容</strong>: 数字文化与画像描绘</li>
        <li><strong>运动与生活方式</strong>: 为全球服饰品牌量身定制的洞察</li>
      </ul>
    </div>
  </div>
</div>

---

## State-of-the-Art Research Facilities

<div class="lang-en">
  <h3>In-House Facilities in the Heart of Seoul (Gangnam & Yongsan)</h3>
  <div class="grid-2">
    <div>
      <ul>
        <li><strong>Focus Group Discussion (FGD) Rooms</strong>
          <ul>
            <li>Equipped with spacious <strong>one-way observation mirrors</strong>.</li>
            <li>High-definition screen/voice recording & live translation booth.</li>
          </ul>
        </li>
        <li><strong>In-Depth Interview (IDI) Rooms</strong>
          <ul>
            <li>Cozy environments optimized for intimate consumer dialogues and deep-dive diaries.</li>
          </ul>
        </li>
      </ul>
    </div>
    <div class="card">
      <h4><strong>UX/UI Usability Testing Lab (UT Lab)</strong></h4>
      <ul>
        <li>Device-agnostic mobile, web, and console testing setup.</li>
        <li><strong>Remote Streaming Capabilities</strong>: Global headquarters & local teams can view live sessions anywhere in the world.</li>
      </ul>
    </div>
  </div>
</div>

<div class="lang-ko">
  <h3>서울 중심가(강남 및 용산)의 자체 상설 조사실 운영</h3>
  <div class="grid-2">
    <div>
      <ul>
        <li><strong>표적집단면접(FGD) 룸</strong>
          <ul>
            <li>넓고 쾌적한 <strong>일방경(One-way mirror) 관찰실</strong> 구비.</li>
            <li>고화질 녹화/녹음 시스템 및 동시통역 부스 지원.</li>
          </ul>
        </li>
        <li><strong>개별심층면접(IDI) 룸</strong>
          <ul>
            <li>프라이빗하고 편안한 인터뷰 분위기 조성, 종단 다이어리 조사 최적화.</li>
          </ul>
        </li>
      </ul>
    </div>
    <div class="card">
      <h4><strong>UX/UI 사용성 테스트 랩 (UT Lab)</strong></h4>
      <ul>
        <li>모바일, 웹, 콘솔 기기 등 멀티 디바이스 테스트 환경 구축.</li>
        <li><strong>실시간 원격 스트리밍</strong>: 전 세계 어디서나 본사 및 로컬 팀이 라이브로 참관 가능.</li>
      </ul>
    </div>
  </div>
</div>

<div class="lang-ja">
  <h3>ソウル中心部(江南＆龍山)のインハウス常設調査室</h3>
  <div class="grid-2">
    <div>
      <ul>
        <li><strong>フォーカスグループインタビュー(FGD)ルーム</strong>
          <ul>
            <li>広々とした<strong>ワンウェイミラー(マジックミラー)観察室</strong>を完備。</li>
            <li>高画質録画・録音システムおよび同時通訳ブース設置。</li>
          </ul>
        </li>
        <li><strong>デプスインタビュー(IDI)ルーム</strong>
          <ul>
            <li>プライベートでリラックスできる空間、縦断的ダイアリー調査に最適化。</li>
          </ul>
        </li>
      </ul>
    </div>
    <div class="card">
      <h4><strong>UX/UIユーザビリティテストラボ (UT Lab)</strong></h4>
      <ul>
        <li>モバイル、Web、コンソールなどマルチデバイスのテスト環境。</li>
        <li><strong>リモートストリーミング機能</strong>: 世界中のどこからでも本社やローカルチームがライブで参観可能。</li>
      </ul>
    </div>
  </div>
</div>

<div class="lang-cn">
  <h3>位于首尔核心区域（江南与龙山）的自营研究室</h3>
  <div class="grid-2">
    <div>
      <ul>
        <li><strong>焦点小组座谈会 (FGD) 室</strong>
          <ul>
            <li>配备宽敞的<strong>单向观察镜</strong>。</li>
            <li>高清音视频录制及同声传译间。</li>
          </ul>
        </li>
        <li><strong>深度访谈 (IDI) 室</strong>
          <ul>
            <li>舒适私密的环境，针对个人对话和深度日记研究进行优化。</li>
          </ul>
        </li>
      </ul>
    </div>
    <div class="card">
      <h4><strong>UX/UI 可用性测试实验室 (UT Lab)</strong></h4>
      <ul>
        <li>支持移动端、网页端和主机端的跨设备测试环境。</li>
        <li><strong>远程直播参观</strong>: 全球总部和本地团队可随时随地在线实时观看测试过程。</li>
      </ul>
    </div>
  </div>
</div>

---

## Qualitative User Research Services

<div class="lang-en">
  <h3>Tailored Approaches for Modern Brands</h3>
  <div class="grid-4">
    <div class="card">
      <h4><strong>FGD</strong></h4>
      Group dynamics to reveal shared lifestyle perceptions, brand affinity, and social trends.
    </div>
    <div class="card">
      <h4><strong>IDI</strong></h4>
      Exploring individual purchase drivers, lifestyle habits, and digital brand experiences.
    </div>
    <div class="card">
      <h4><strong>Observation</strong></h4>
      Shadowing consumers in their natural retail environments and daily routines.
    </div>
    <div class="card">
      <h4><strong>Diary Study</strong></h4>
      Longitudinal tracking of day-to-day choices and mobile app interactions.
    </div>
  </div>
</div>

<div class="lang-ko">
  <h3>현대 브랜드를 위한 맞춤형 접근 방식</h3>
  <div class="grid-4">
    <div class="card">
      <h4><strong>표적집단면접 (FGD)</strong></h4>
      그룹 다이내믹스를 통해 공유된 라이프스타일 인식, 브랜드 친밀도, 트렌드 파악.
    </div>
    <div class="card">
      <h4><strong>개별심층면접 (IDI)</strong></h4>
      개인의 구매 동기, 라이프스타일 습관 및 디지털 브랜드 경험 탐색.
    </div>
    <div class="card">
      <h4><strong>에스노그라피 (관찰)</strong></h4>
      실제 매장 환경 및 일상생활 속에서 소비자의 자연스러운 행동 관찰.
    </div>
    <div class="card">
      <h4><strong>다이어리 연구</strong></h4>
      소비자들의 일상적인 선택과 모바일 앱 이용 행태를 종단적으로 추적 조사.
    </div>
  </div>
</div>

<div class="lang-ja">
  <h3>現代のブランドに最適化されたアプローチ</h3>
  <div class="grid-4">
    <div class="card">
      <h4><strong>FGD (グループインタビュー)</strong></h4>
      グループダイナミクスを通じて、ライフスタイル、ブランド親和性、トレンドを解明。
    </div>
    <div class="card">
      <h4><strong>IDI (デプスインタビュー)</strong></h4>
      個人の購買要因、ライフスタイルの習慣、デジタルブランド体験의 探索。
    </div>
    <div class="card">
      <h4><strong>行動観察</strong></h4>
      実際の購買環境や日常生活の中での消費者のリアルな行動観察.
    </div>
    <div class="card">
      <h4><strong>ダイアリー調査</strong></h4>
      日常の選択やモバイルアプリ内行動を継続的・縦断的に追跡。
    </div>
  </div>
</div>

<div class="lang-cn">
  <h3>专为现代品牌定制的研究方法</h3>
  <div class="grid-4">
    <div class="card">
      <h4><strong>焦点小组 (FGD)</strong></h4>
      利用群体动力学揭示共同的生活方式认知、品牌亲和力及社交趋势。
    </div>
    <div class="card">
      <h4><strong>深度访谈 (IDI)</strong></h4>
      探索个人的购买驱动力、生活习惯及数字品牌体验。
    </div>
    <div class="card">
      <h4><strong>民族志观察</strong></h4>
      在真实的零售环境和日常生活中实地观察消费者行为。
    </div>
    <div class="card">
      <h4><strong>移动日记研究</strong></h4>
      长期追踪消费者的日常选择与移动应用程序交互行为。
    </div>
  </div>
</div>

---

## Delta Code™ (Proprietary Framework 1)

<div class="lang-en">
  <h3>Decoding the Cultural Context of Korean Consumers</h3>
  <div class="highlight">
    "To understand how Koreans buy, we must first understand how they live."
  </div>
  <div class="grid-2">
    <div class="card">
      <h3>Key Elements</h3>
      <ul>
        <li><strong>Subcultural Analysis</strong>: Uncovering subcultures of youth, fashion, and lifestyle.</li>
        <li><strong>Trend Evolution</strong>: Decoding macro shifts (e.g., hyper-convenience, sustainable lifestyle, "healthy pleasure").</li>
      </ul>
    </div>
    <div class="card">
      <h3>Strategic Value</h3>
      <ul>
        <li>Translating global brand campaigns into local cultural contexts.</li>
        <li>Identifying high-potential niche communities.</li>
      </ul>
    </div>
  </div>
</div>

<div class="lang-ko">
  <h3>한국 소비자의 문화적 맥락 디코딩</h3>
  <div class="highlight">
    "한국 소비자가 구매하는 방식을 이해하려면, 먼저 그들의 삶을 이해해야 합니다."
  </div>
  <div class="grid-2">
    <div class="card">
      <h3>핵심 요소</h3>
      <ul>
        <li><strong>하위문화 분석</strong>: 청년층, 패션, 라이프스타일의 다양한 하위문화 분석.</li>
        <li><strong>트렌드 진화 추적</strong>: 매크로 트렌드 변화 디코딩 (예: 극대화된 편리성, 지속 가능한 삶, "헬시 플레저").</li>
      </ul>
    </div>
    <div class="card">
      <h3>전략적 가치</h3>
      <ul>
        <li>글로벌 브랜드 캠페인을 한국의 로컬 문화 맥락에 맞게 로컬라이징.</li>
        <li>고성장 잠재력을 지닌 틈새(Niche) 커뮤니티 발굴.</li>
      </ul>
    </div>
  </div>
</div>

<div class="lang-ja">
  <h3>韓国消費者の文化的文脈のデコーディング</h3>
  <div class="highlight">
    「韓国人がどのように買うかを理解するには、まず彼らがどのように生きているかを理解しなければなりません」
  </div>
  <div class="grid-2">
    <div class="card">
      <h3>主要要素</h3>
      <ul>
        <li><strong>サブカルチャー分析</strong>: 若者、ファッション、ライフスタイルの多様なサブカルチャーの掘り下げ。</li>
        <li><strong>トレンドの進化</strong>: マクロトレンドの変化を解読 (例: 極限の利便性、サステナブルライフ、"ヘルシープラジャー")。</li>
      </ul>
    </div>
    <div class="card">
      <h3>戦略적 価値</h3>
      <ul>
        <li>グローバルキャンペーンを現地の文化的文脈に合わせたローカライズ。</li>
        <li>高い成長可能性を持つニッチコミュニティの特定。</li>
      </ul>
    </div>
  </div>
</div>

<div class="lang-cn">
  <h3>解码韩国消费者的文化背景</h3>
  <div class="highlight">
    “要了解韩国人的购买方式，首先必须了解他们的生活方式。”
  </div>
  <div class="grid-2">
    <div class="card">
      <h3>核心要素</h3>
      <ul>
        <li><strong>亚文化分析</strong>: 深入探究青年、时尚和生活方式的多元亚文化。</li>
        <li><strong>趋势演变</strong>: 解码宏观趋势变化（如极致便利、可持续生活方式、“健康愉悦”）。</li>
      </ul>
    </div>
    <div class="card">
      <h3>战略价值</h3>
      <ul>
        <li>将全球品牌活动转化为契合本土文化背景的传播方案。</li>
        <li>识别具有高增长潜力的细分社区。</li>
      </ul>
    </div>
  </div>
</div>

---

## Deep Persona™ (Proprietary Framework 2)

<div class="lang-en">
  <h3>Going Beyond Demographics to Emotional Drivers</h3>
  <div class="highlight">
    <strong>Traditional Persona</strong>: Age 25, lives in Seoul, runs 3 times a week.<br>
    <strong>Deep Persona™</strong>: Maps psychological barriers, emotional payoffs, and cultural micro-triggers.
  </div>
  <div class="grid-2">
    <div class="card">
      <h3>1. Psychological Drivers</h3>
      What makes a consumer choose premium over mass? How does peer influence affect daily choices in Korea?
    </div>
    <div class="card">
      <h3>2. Digital Touchpoints</h3>
      Mapping the exact journey through Kakao, Instagram, local community hubs, and e-commerce platforms.
    </div>
  </div>
</div>

<div class="lang-ko">
  <h3>인구통계학적 정보를 넘어선 감정적 핵심 동기 분석</h3>
  <div class="highlight">
    <strong>일반적인 페르소나</strong>: 서울에 거주하는 25세 여성, 주 3회 피트니스 수행.<br>
    <strong>Deep Persona™</strong>: 소비자의 심리적 장벽, 감정적 보상, 그리고 문화적 미세 유발 요인을 매핑합니다.
  </div>
  <div class="grid-2">
    <div class="card">
      <h3>1. 심리적 드라이버</h3>
      소비자가 대중적인 제품 대신 프리미엄 제품을 선택하게 만드는 숨은 심리는 무엇인가? 한국 시장의 동료(Peer) 압력이 일상적 선택에 미치는 영향은?
    </div>
    <div class="card">
      <h3>2. 디지털 터치포인트</h3>
      카카오, 인스타그램, 로컬 커뮤니티, 이커머스 채널 등을 통한 실제 유저 저니(Journey) 매핑.
    </div>
  </div>
</div>

<div class="lang-ja">
  <h3>デモグラフィックスを超えた「感情的ドライバー」の特定</h3>
  <div class="highlight">
    <strong>一般的なペルソナ</strong>: ソウル在住の25歳、週3回ランニング。<br>
    <strong>Deep Persona™</strong>: 心理的障壁、感情的ベネフィット、および文化的マイクロトリガーをマッピングします。
  </div>
  <div class="grid-2">
    <div class="card">
      <h3>1. 心理的ドライバー</h3>
      消費者がコモディティではなくプレミアムを選ぶ理由は何か？韓国における同調圧力が日常の選択に与える影響は？
    </div>
    <div class="card">
      <h3>2. デジタルタッチポイント</h3>
      Kakao、Instagram、ローカルコミュニティ、ECプラットフォームを経由する詳細なジャーニーの可視化。
    </div>
  </div>
</div>

<div class="lang-cn">
  <h3>超越人口统计学，探索情感驱动力</h3>
  <div class="highlight">
    <strong>传统画像</strong>: 25岁，居住于首尔，每周跑步3次。<br>
    <strong>Deep Persona™</strong>: 描绘消费者的心理壁垒、情感回报以及文化微触发因素。
  </div>
  <div class="grid-2">
    <div class="card">
      <h3>1. 心理驱动因素</h3>
      是什么让消费者选择高端而非大众产品？同伴影响如何作用于韩国消费者的日常选择？
    </div>
    <div class="card">
      <h3>2. 数字触点</h3>
      绘制贯穿 Kakao、Instagram、本土社区中心及电商平台的精准路径图。
    </div>
  </div>
</div>

---

## Research 2 Action

<div class="lang-en">
  <h3>Supporting the Transition from Insight to Concrete Action</h3>
  <div class="chevron-flow">
    <div class="chevron-item">
      <div class="step-num">01</div>
      <h3>Fieldwork Visualization</h3>
      We visually document and present fieldwork (video, photos) so that clients can intuitively understand the real-world consumer context.
    </div>
    <div class="chevron-item">
      <div class="step-num">02</div>
      <h3>Real-Time Result Sharing</h3>
      Findings and raw sessions are shared in real-time, allowing client feedback to be integrated instantly into subsequent research iterations.
    </div>
    <div class="chevron-item">
      <div class="step-num">03</div>
      <h3>Korea Market Knowledge Asset</h3>
      We ensure that the client accumulates structured, reusable knowledge and experience regarding the South Korean market.
    </div>
  </div>
</div>

<div class="lang-ko">
  <h3>단순 리서치를 넘어 구체적 실행(Action)으로 이어지는 지원 솔루션</h3>
  <div class="chevron-flow">
    <div class="chevron-item">
      <div class="step-num">01</div>
      <h3>필드웍 시각화 지원</h3>
      현장 인터뷰 및 사용자 행동을 사진/영상 등으로 시각화하여, 현지 소비자의 생생한 맥락(Context)을 완벽하게 이해할 수 있도록 돕습니다.
    </div>
    <div class="chevron-item">
      <div class="step-num">02</div>
      <h3>실시간 조사 결과 공유</h3>
      조사 진행 과정과 리포트 초기 결과를 실시간으로 공유하여, 고객사 피드백을 즉각 다음 조사 단계에 반영합니다.
    </div>
    <div class="chevron-item">
      <div class="step-num">03</div>
      <h3>한국 시장 조사 경험의 자산화</h3>
      단 1개의 프로젝트를 진행하더라도, 고객사가 일회성 결과물에 그치지 않고 한국 시장에 대한 지식과 경험을 자산으로 축적할 수 있도록 지원합니다.
    </div>
  </div>
</div>

<div class="lang-ja">
  <h3>単なる調査を超えて、具体的な実行(Action)へつなげる支援</h3>
  <div class="chevron-flow">
    <div class="chevron-item">
      <div class="step-num">01</div>
      <h3>フィールドワークの視覚化</h3>
      現地の消費者行動やインタビューを写真・映像等で視覚的に記録・提示し、リアルな文脈(Context)を直感的に深く理解できるようサポートします。
    </div>
    <div class="chevron-item">
      <div class="step-num">02</div>
      <h3>調査結果のリアルタイム共有</h3>
      プロジェクトの進行状況と初期結果をリアルタイムで共有し、クライアントのフィードバックを即座に次のリサーチに反映します。
    </div>
    <div class="chevron-item">
      <div class="step-num">03</div>
      <h3>韓国市場調査経験の資産化</h3>
      たった一つのプロジェクトであっても、一回限りの調査で終わらせず、韓国市場に関する深いナレッジと経験を顧客社内に蓄積できるよう支援します。
    </div>
  </div>
</div>

<div class="lang-cn">
  <h3>跨越单纯研究，助力向具体行动（Action）转化</h3>
  <div class="chevron-flow">
    <div class="chevron-item">
      <div class="step-num">01</div>
      <h3>实地调研可视化</h3>
      通过图片、视频等方式将实地访谈和用户行为进行可视化呈现，帮助客户直观、透彻地理解本土消费者的真实生活场景与语境（Context）。
    </div>
    <div class="chevron-item">
      <div class="step-num">02</div>
      <h3>调研结果实时共享</h3>
      在项目执行过程中实时共享进度与初步发现，确保客户的反馈能够即时融入下一步的调研迭代中。
    </div>
    <div class="chevron-item">
      <div class="step-num">03</div>
      <h3>韩国市场研究经验 of 资产化</h3>
      即使只合作一个项目，也致力于协助客户在企业内部沉淀并积累关于韩国市场的系统化知识与调研经验，而非一次性交付物。
    </div>
  </div>
</div>

---

## AI & Advanced Tech Integration

<div class="lang-en">
  <h3>Driving Efficiency and Deep Insights</h3>
  <div class="grid-2">
    <div class="card">
      <h3>AI-Enabled Workflows</h3>
      <ul>
        <li><strong>ESOMAR Speaker</strong>: Jay Ahn presents on using Custom GPTs in marketing research.</li>
        <li><strong>Rapid Analysis</strong>: Custom AI agents for transcribing, translation, and initial semantic coding.</li>
        <li><strong>Fast Turnaround</strong>: Speeds up reporting for quick-to-market decisions.</li>
      </ul>
    </div>
    <div class="card">
      <h3>Advanced UT Capabilities</h3>
      <ul>
        <li><strong>Eye-Tracking & Screen Recording</strong>: See exactly where users look on mobile or web interfaces.</li>
        <li><strong>Biometric Integration</strong>: Option for facial expression analysis and GSR (emotional engagement metrics).</li>
      </ul>
    </div>
  </div>
</div>

<div class="lang-ko">
  <h3>리서치 효율성 극대화와 심층적 인사이트 도출</h3>
  <div class="grid-2">
    <div class="card">
      <h3>AI 기반 워크플로우</h3>
      <ul>
        <li><strong>ESOMAR 발표자</strong>: 마케팅 리서치 내 Custom GPT 활용 방안에 대한 스피커 참여.</li>
        <li><strong>분석 효율화</strong>: 전사, 번역, 초기 의미론적 코딩을 처리하는 맞춤형 AI 에이전트 도입.</li>
        <li><strong>신속한 대응</strong>: 결과 도출 시간을 단축하여 빠른 비즈니스 의사결정 지원.</li>
      </ul>
    </div>
    <div class="card">
      <h3>첨단 UT(사용성 테스트) 역량</h3>
      <ul>
        <li><strong>시선 추적(Eye-tracking) 및 화면 녹화</strong>: 앱/웹 상에서 사용자의 시선 집중도와 행동을 정밀 관측.</li>
        <li><strong>바이오메트릭 통합</strong>: 얼굴 표정 분석 및 피부 전도도(GSR) 측정을 통한 정서적 몰입도 분석.</li>
      </ul>
    </div>
  </div>
</div>

<div class="lang-ja">
  <h3>調査の効率化とディープなインサイトの導出</h3>
  <div class="grid-2">
    <div class="card">
      <h3>AIを活用したワークフロー</h3>
      <ul>
        <li><strong>ESOMAR スピーカー</strong>: マーケティング調査におけるカスタムGPTの活用に関する発表。</li>
        <li><strong>分析の高速化</strong>: 文字起こし、翻訳、初期セマンティックコーディングを行う独自AIエージェント。</li>
        <li><strong>迅速なレポーティング</strong>: 意思決定を加速するための素早いアウトプット。</li>
      </ul>
    </div>
    <div class="card">
      <h3>高度なUT機能</h3>
      <ul>
        <li><strong>アイトラッキング＆画面記録</strong>: アプリやWeb上でユーザーの視線と操作挙動を正確に追跡。</li>
        <li><strong>バイオメトリクス統合</strong>: 表情分析や皮膚電気活動(GSR)の測定による感情エンゲージメントの数値化。</li>
      </ul>
    </div>
  </div>
</div>

<div class="lang-cn">
  <h3>提升调研效率，发掘深层洞察</h3>
  <div class="grid-2">
    <div class="card">
      <h3>赋能 AI 的工作流程</h3>
      <ul>
        <li><strong>ESOMAR 发言人</strong>: 分享在市场研究中应用定制化 GPT 的前沿实践。</li>
        <li><strong>快速分析</strong>: 采用定制 AI 代理处理转录、翻译和初步语义编码。</li>
        <li><strong>缩短周期</strong>: 缩短报告交付周期，支持敏捷的市场决策。</li>
      </ul>
    </div>
    <div class="card">
      <h3>先进的可用性测试 (UT) 能力</h3>
      <ul>
        <li><strong>眼动追踪与屏幕录制</strong>: 精准捕捉用户在应用/网页上的视觉焦点和操作行为。</li>
        <li><strong>生物识别技术整合</strong>: 可选面部表情分析和皮电反应(GSR)测量，量化情感交互深度。</li>
      </ul>
    </div>
  </div>
</div>

---

<!-- 
_class: dark
_paginate: false 
_footer: ''
-->

<div class="lang-en" style="margin-top: 60px;">
  <h3>THANK YOU</h3>
  <h1 style="font-size: 40px; margin-bottom: 25px;">Let’s Connect with Korean Consumers Together.</h1>
  <br>
  <ul>
    <li><strong>CEO & Project Director</strong>: Jay Ahn (안재윤)</li>
    <li><strong>LinkedIn</strong>: <a href="https://www.linkedin.com/in/jayahn/" style="color: #ffffff;">linkedin.com/in/jayahn</a></li>
    <li><strong>Address</strong>: Gangnam & Yongsan Facilities, Seoul, Korea</li>
  </ul>
</div>

<div class="lang-ko" style="margin-top: 60px;">
  <h3>THANK YOU</h3>
  <h1 style="font-size: 40px; margin-bottom: 25px;">한국 소비자를 향한 깊이 있는 이해, DRK가 함께 합니다.</h1>
  <br>
  <ul>
    <li><strong>대표 및 프로젝트 총괄</strong>: 안재윤 (Jay Ahn)</li>
    <li><strong>LinkedIn</strong>: <a href="https://www.linkedin.com/in/jayahn/" style="color: #ffffff;">linkedin.com/in/jayahn</a></li>
    <li><strong>주소</strong>: 서울 강남 및 용산 센터</li>
  </ul>
</div>

<div class="lang-ja" style="margin-top: 60px;">
  <h3>THANK YOU</h3>
  <h1 style="font-size: 40px; margin-bottom: 25px;">韓国消費者との深いつながりを、DRKと共に。</h1>
  <br>
  <ul>
    <li><strong>代表 兼 プロジェクト統括</strong>: ジェイ・アン (Jay Ahn)</li>
    <li><strong>LinkedIn</strong>: <a href="https://www.linkedin.com/in/jayahn/" style="color: #ffffff;">linkedin.com/in/jayahn</a></li>
    <li><strong>住所</strong>: ソウル江南・龍山センター</li>
  </ul>
</div>

<div class="lang-cn" style="margin-top: 60px;">
  <h3>THANK YOU</h3>
  <h1 style="font-size: 40px; margin-bottom: 25px;">携手 DRK，深度连接韩国消费者。</h1>
  <br>
  <ul>
    <li><strong>总裁兼项目总监</strong>: 安杰伦 (Jay Ahn)</li>
    <li><strong>LinkedIn</strong>: <a href="https://www.linkedin.com/in/jayahn/" style="color: #ffffff;">linkedin.com/in/jayahn</a></li>
    <li><strong>地址</strong>: 首尔江南及龙山研究中心</li>
  </ul>
</div>
