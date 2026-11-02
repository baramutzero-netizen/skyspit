const CFG = {
  api: '__sky', title: '앙천이타', sub: '仰天而唾 · 누워서 침 뱉기', unit: '후련함', tapLabel: '퉤! 뱉기',
  icon: ['spit', { w: '#9fd2ee', W: '#e8f6ff' }],
  colors: { bg: '#14171c', band: '#0d1014', accent: '#7cc4e8', dim: '#9aa6b2', cream: '#eef2f5', leaf: '#7fb069', panel: '#1f242c', line: '#2f3742', faint: '#6c7884', gold: '#f3c34f', red: '#e5484d', ink: '#14171c', btnShade: '#3d7aa0' },
  stat: () => `구경꾼 ${fmt(window.__sky.D().mk)}명 · 체공 ${Math.round(window.__sky.D().hang * 10) / 10}초`,
  tap: J => J.spitTap(),
  endCard: [['仰天而唾', 560, 140, 'accent'], ['위로 뱉은 건,', 790, 60, 'cream'], ['결국 내게 돌아온다.', 870, 60, 'cream'], ['지금 누워서 뱉어 보기', 1060, 60, 'leaf'], ['baramutzero-netizen.github.io/skyspit', 1160, 40, 'cream', 'Galmuri11']],
  async play(h) {
    h.cap('누워서 위로 뱉으면', '속이 후련하다');
    await h.tapFor(2600, 5);
    h.cap('…그런데 전부 돌아온다', '철퍽');
    await h.tapFor(1800, 4);
    h.cap('더 세게, 더 높이 뱉었다', '돌아오는 데 오래 걸릴 뿐');
    { const tp = h.tapFor(2200, 5); await h.buyAll(0, 160); await tp; }
    h.cap('단톡방엔 뒷담화', '댓글창엔 악플');
    await h.venue(1, 20, 1100); await h.venue(2, 20, 1100);
    h.cap('방송엔 지라시, 토론회엔 막말', 'SNS엔 가짜뉴스');
    await h.venue(3, 15, 800); await h.venue(4, 15, 800); await h.venue(5, 15, 900);
    h.cap('그리고 AI로 무한 양산', '에이전트를 여러 개 병렬로');
    await h.venue(6, 30, 2000);
    h.cap('평생 누워서 뱉다가', '마침내 일어났다');
    window.__endK = 0.55; h.buy('end');
  },
};
