document.addEventListener('DOMContentLoaded', function () {
  const tabs = document.querySelectorAll('.day-tab');
  const contents = document.querySelectorAll('.day-content');

 
  const shortLabels = {
    monday: 'Mon',
    tuesday: 'Tue',
    wednesday: 'Wed',
    thursday: 'Thu',
    friday: 'Fri',
    saturday: 'Sat',
    sunday: 'Sun'
  };

  function showDay(dayName) {
    contents.forEach(c => c.classList.remove('visible'));
    const matched = document.querySelector(`.day-content[data-day="${dayName}"]`);
    if (matched) matched.classList.add('visible');
  }

  tabs.forEach(tab => {
    tab.addEventListener('click', function () {
     
      tabs.forEach(t => {
        t.classList.remove('active');
        t.textContent = shortLabels[t.getAttribute('data-day')];
      });

     
      tab.classList.add('active');
      tab.textContent = tab.getAttribute('data-full');

      showDay(tab.getAttribute('data-day'));
    });
  });


  const favModal = document.getElementById('fav-modal');
  const favModalHeading = document.getElementById('fav-modal-heading');
  const favModalCancel = document.getElementById('fav-modal-cancel');
  const favTriggers = document.querySelectorAll('.fav-star, .nav-star, .nav-account');

  function openFavModal(e) {
    e.preventDefault();
    e.stopPropagation();
    if (favModal) favModal.hidden = false;
    if (favModalHeading) {
      favModalHeading.textContent = e.currentTarget.getAttribute('data-modal-heading') || 'Save your favorite meals';
    }
  }

  function closeFavModal() {
    if (favModal) favModal.hidden = true;
  }

  favTriggers.forEach(btn => btn.addEventListener('click', openFavModal));

  if (favModalCancel) favModalCancel.addEventListener('click', closeFavModal);

  if (favModal) {
    favModal.addEventListener('click', function (e) {
      if (e.target === favModal) closeFavModal();
    });
  }


  const planReadyModal = document.getElementById('plan-ready-modal');
  const planReadySkip = document.getElementById('plan-ready-skip');

  function closePlanReadyModal() {
    if (planReadyModal) planReadyModal.hidden = true;
  }

  if (planReadySkip) planReadySkip.addEventListener('click', closePlanReadyModal);

  if (planReadyModal) {
    planReadyModal.addEventListener('click', function (e) {
      if (e.target === planReadyModal) closePlanReadyModal();
    });
  }
});