document.addEventListener('DOMContentLoaded', () => {
  const themeToggle = document.getElementById('theme-toggle');
  const root = document.documentElement;
  
  // Theme Toggle Logic
  themeToggle.addEventListener('click', () => {
    root.classList.toggle('dark-theme');
    const theme = root.classList.contains('dark-theme') ? 'dark' : 'light';
    localStorage.setItem('theme', theme);
    updateThemeIcon();
  });

  function updateThemeIcon() {
    const isDark = root.classList.contains('dark-theme');
    // Lucide-style icons: Moon and Sun
    themeToggle.innerHTML = isDark 
      ? `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sun"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M22 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>`
      : `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-moon"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>`;
  }

  updateThemeIcon();

  // Mobile Menu Toggle
  const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
  const navLinks = document.getElementById('nav-links');

  if (mobileMenuToggle && navLinks) {
    mobileMenuToggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
      const isActive = navLinks.classList.contains('active');
      mobileMenuToggle.innerHTML = isActive
        ? `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x"><line x1="18" x2="6" y1="6" y2="18"/><line x1="6" x2="18" y1="6" y2="18"/></svg>`
        : `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-menu"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>`;
    });

    // Close menu when a link is clicked
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        mobileMenuToggle.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-menu"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>`;
      });
    });
  }

  // Smooth scroll for internal links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        window.scrollTo({
          top: target.offsetTop - 100,
          behavior: 'smooth'
        });
      }
    });
  });

  // --- Search Modal Functionality ---
  const searchBtn = document.getElementById('search-btn');
  const searchModal = document.getElementById('search-modal');
  const globalSearchInput = document.getElementById('global-search');
  const globalResults = document.getElementById('global-search-results');

  // Pre-defined documentation pages
  const docPages = [
    'getting-started.html',
    'installation.html',
    'usage.html',
    'configuration.html',
    'faq.html'
  ];

  let searchIndex = [];
  let isIndexing = false;

  async function indexDocs() {
    if (isIndexing || searchIndex.length > 0) return;
    isIndexing = true;

    // Detect if we are in /docs/ or root
    const isDocsSubdir = window.location.pathname.includes('/docs/');
    const basePath = isDocsSubdir ? '' : 'docs/';

    try {
      const fetchPromises = docPages.map(async (page) => {
        const response = await fetch(basePath + page);
        const html = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const content = doc.querySelector('.docs-content');
        
        if (content) {
          const headings = Array.from(content.querySelectorAll('h2, h3'));
          const paragraphs = Array.from(content.querySelectorAll('p, li'));
          
          headings.forEach(h => {
            searchIndex.push({
              title: h.textContent,
              text: h.textContent,
              url: basePath + page + '#' + (h.id || ''),
              page: page.replace('.html', '').replace('-', ' ')
            });
          });

          paragraphs.forEach(p => {
            searchIndex.push({
              title: '', // We'll find nearest heading later
              text: p.textContent,
              url: basePath + page, // Could be more precise with IDs
              page: page.replace('.html', '').replace('-', ' '),
              element: p
            });
          });
        }
      });

      await Promise.all(fetchPromises);
    } catch (err) {
      console.error('Error indexing docs:', err);
    }
    isIndexing = false;
  }

  if (searchBtn && searchModal) {
    searchBtn.addEventListener('click', () => {
      searchModal.style.display = 'flex';
      globalSearchInput.focus();
      indexDocs(); // Index on first open
    });

    searchModal.addEventListener('click', (e) => {
      if (e.target === searchModal) {
        searchModal.style.display = 'none';
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && searchModal.style.display === 'flex') {
        searchModal.style.display = 'none';
      }
    });
  }

  if (globalSearchInput && globalResults) {
    globalSearchInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase();
      globalResults.innerHTML = '';

      if (query.length < 2) return;

      const matches = searchIndex.filter(item => 
        item.text.toLowerCase().includes(query) || 
        item.page.toLowerCase().includes(query)
      ).slice(0, 10);

      if (matches.length > 0) {
        matches.forEach(match => {
          const div = document.createElement('div');
          div.className = 'search-result-item';
          
          const displayTitle = match.title || 'Content match';
          const snippet = match.text.length > 120 ? match.text.substring(0, 120) + '...' : match.text;

          div.innerHTML = `
            <span class="search-result-page">${match.page}</span>
            <span class="search-result-title">${displayTitle}</span>
            <span class="search-result-snippet">${snippet}</span>
          `;

          div.addEventListener('click', () => {
            window.location.href = match.url;
            searchModal.style.display = 'none';
            globalSearchInput.value = '';
          });
          globalResults.appendChild(div);
        });
      } else {
        globalResults.innerHTML = '<div class="search-result-item"><span class="search-result-title">No results found</span></div>';
      }
    });
  }

  // --- Wiki Navigation ---
  const docsNav = document.getElementById('on-this-page');
  const docsContent = document.querySelector('.docs-content');
  if (docsNav && docsContent) {
    const headings = Array.from(docsContent.querySelectorAll('h2, h3'));
    headings.forEach((heading, index) => {
      if (!heading.id) heading.id = `section-${index}`;
      
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = `#${heading.id}`;
      a.textContent = heading.textContent;
      if (heading.tagName === 'H3') a.style.paddingLeft = '1.5rem';
      
      li.appendChild(a);
      docsNav.appendChild(li);
    });

    window.addEventListener('scroll', () => {
      let current = '';
      headings.forEach(heading => {
        const sectionTop = heading.offsetTop;
        if (pageYOffset >= sectionTop - 150) {
          current = heading.getAttribute('id');
        }
      });

      docsNav.querySelectorAll('a').forEach(a => {
        a.classList.remove('active');
        if (a.getAttribute('href') === `#${current}`) {
          a.classList.add('active');
        }
      });
    });
  }
});
