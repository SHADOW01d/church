  const nav = document.getElementById('mainNav');
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 60);
    document.getElementById('btt').classList.toggle('show', window.scrollY > 300);
  });
  function openMobile() { document.getElementById('mobileMenu').classList.add('open'); document.body.style.overflow='hidden'; }
  function closeMobile() { document.getElementById('mobileMenu').classList.remove('open'); document.body.style.overflow=''; }

  let currentSlide = 0;
  const slides = document.querySelectorAll('.slide');
  const dotsEl = document.getElementById('dots');
  slides.forEach((_, i) => {
    const d = document.createElement('button');
    d.className = 'dot' + (i===0?' active':'');
    d.setAttribute('role', 'tab');
    d.setAttribute('aria-label', 'Slidi ' + (i+1));
    d.addEventListener('click', () => goSlide(i));
    dotsEl.appendChild(d);
  });
  function goSlide(n) {
    slides[currentSlide].classList.remove('active');
    dotsEl.children[currentSlide].classList.remove('active');
    currentSlide = (n + slides.length) % slides.length;
    slides[currentSlide].classList.add('active');
    dotsEl.children[currentSlide].classList.add('active');
  }
  function changeSlide(dir) { goSlide(currentSlide + dir); }
  setInterval(() => changeSlide(1), 6000);

  function openLightbox(el) {
    const img = el.querySelector('img');
    document.getElementById('lightboxImg').src = img.src;
    document.getElementById('lightboxImg').alt = img.alt;
    document.getElementById('lightbox').classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeLightbox() {
    document.getElementById('lightbox').classList.remove('open');
    document.body.style.overflow = '';
  }
  document.getElementById('lightbox').addEventListener('click', function(e) { if(e.target===this) closeLightbox(); });
  document.addEventListener('keydown', e => { if(e.key==='Escape') closeLightbox(); });

  const fadeEls = document.querySelectorAll('.fade-up');
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if(e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); } });
  }, { threshold: 0.12 });
  fadeEls.forEach(el => obs.observe(el));

  function handleSubmit(e) {
    e.preventDefault();
    const msg = document.getElementById('formMsg');
    msg.style.display = 'block';
    msg.textContent = '🙏 Asante! Ujumbe wako umepokelewa. Tutawasiliana nawe hivi karibuni. Mungu akubariki!';
    e.target.reset();
    setTimeout(() => { msg.style.display='none'; }, 6000);
  }
