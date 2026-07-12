document.addEventListener('DOMContentLoaded', function () {
  const tabs = document.querySelectorAll('.day-tab');
  const contents = document.querySelectorAll('.day-content');

  // short labels for the tabs when they are not active
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
      // collapse whichever tab was active back to its short label
      tabs.forEach(t => {
        t.classList.remove('active');
        t.textContent = shortLabels[t.getAttribute('data-day')];
      });

      // expand the tab that was clicked to its full label and show the matching content
      tab.classList.add('active');
      tab.textContent = tab.getAttribute('data-full');

      showDay(tab.getAttribute('data-day'));
    });
  });
});