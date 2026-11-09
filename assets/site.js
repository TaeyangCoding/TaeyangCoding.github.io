(() => {
  const cards = [...document.querySelectorAll('.app-card')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  const search = document.getElementById('app-search');
  const status = document.getElementById('result-status');
  if (!search || !status) return;
  let platform = 'all';
  function update() {
    document.documentElement.dataset.platform = platform;
    document.querySelectorAll('.apple-store').forEach(item => { item.hidden = platform === 'android'; });
    document.querySelectorAll('.google-pending').forEach(item => { item.hidden = platform !== 'android'; });
    const query = search.value.normalize('NFKC').toLocaleLowerCase('ko').replace(/\s/g, '');
    let count = 0;
    cards.forEach(card => {
      const matches = (platform === 'all' || card.dataset.platforms.split(' ').includes(platform)) && card.dataset.search.includes(query);
      card.hidden = !matches;
      count += Number(matches);
    });
    document.getElementById('empty-state').hidden = count !== 0;
    status.textContent = `${count}개의 앱`;
  }
  filters.forEach(button => button.addEventListener('click', () => {
    platform = button.dataset.filter;
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    update();
  }));
  search.addEventListener('input', update);
})();
