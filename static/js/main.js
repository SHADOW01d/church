  function selectCategory(card, name) {
    document.querySelectorAll('.give-cat-card').forEach(c => c.classList.remove('active-cat'));
    card.classList.add('active-cat');
    document.getElementById('selectedFund').textContent = name;
  }

  // ── Slideshow ──
  let currentSlide = 0;
  const slides = document.querySelectorAll('.slide');
  const dots = document.querySelectorAll('.slide-dot');
  let slideTimer = null;

  function showSlide(n) {
    slides[currentSlide].classList.remove('active');
    dots[currentSlide].classList.remove('active');
    currentSlide = (n + slides.length) % slides.length;
    slides[currentSlide].classList.add('active');
    dots[currentSlide].classList.add('active');
  }

  function changeSlide(dir) {
    clearInterval(slideTimer);
    showSlide(currentSlide + dir);
    startAuto();
  }

  function goToSlide(n) {
    clearInterval(slideTimer);
    showSlide(n);
    startAuto();
  }

  function startAuto() {
    slideTimer = setInterval(() => showSlide(currentSlide + 1), 5000);
  }

  startAuto();

  function toggleMenu() {
    const links = document.getElementById('navLinks');
    links.classList.toggle('open');
  }

  function handleSubmit(btn) {
    btn.textContent = 'Message Sent! God Bless You ✦';
    btn.style.background = '#1a6fa8';
    btn.style.color = '#fff';
    btn.disabled = true;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.classList.add('visible');
        }, 80);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
      document.getElementById('navLinks').classList.remove('open');
    });
  });

  window.addEventListener('scroll', () => {
    const nav = document.querySelector('nav');
    if (window.scrollY > 60) {
      nav.style.background = 'rgba(10,61,107,0.99)';
    } else {
      nav.style.background = 'rgba(10,61,107,0.97)';
    }
  });
  // ── Page Overlay System ──
  function openPage(id) {
    document.getElementById(id).classList.add('page-open');
    document.body.style.overflow = 'hidden';
  }

  function closePage(id) {
    document.getElementById(id).classList.remove('page-open');
    document.body.style.overflow = '';
  }

  // Give amount selector
  document.querySelectorAll('.amount-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.amount-btn').forEach(b => b.classList.remove('selected'));
      this.classList.add('selected');
      const custom = document.getElementById('customAmount');
      if (this.dataset.amount === 'custom') {
        custom.style.display = 'block';
        custom.focus();
      } else {
        custom.style.display = 'none';
        custom.value = '';
      }
    });
  });

  // Join Us step system
  let joinStep = 1;
  function nextJoinStep(n) {
    document.getElementById('joinStep' + joinStep).style.display = 'none';
    joinStep = n;
    document.getElementById('joinStep' + joinStep).style.display = 'block';
    document.querySelectorAll('.step-indicator').forEach((el, i) => {
      el.classList.toggle('active', i + 1 <= joinStep);
    });
  }

  function submitGive(btn) {
    const selected = document.querySelector('.amount-btn.selected');
    if (!selected) { alert('Please select a giving amount.'); return; }
    btn.textContent = '✦ Thank You! God Bless You ✦';
    btn.style.background = '#1a6fa8';
    btn.style.color = '#fff';
    btn.disabled = true;
    setTimeout(() => {
      btn.textContent = 'Give Now ✦';
      btn.style.background = '';
      btn.style.color = '';
      btn.disabled = false;
      document.querySelectorAll('.amount-btn').forEach(b => b.classList.remove('selected'));
    }, 4000);
  }

  function submitJoin(btn) {
    btn.textContent = 'Welcome to the Family! ✦';
    btn.style.background = '#1a6fa8';
    btn.style.color = '#fff';
    btn.disabled = true;
    setTimeout(() => nextJoinStep(4), 800);
  }
