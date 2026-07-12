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


  const isAuthenticated =
  document.body.dataset.authenticated === 'true';
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

  if (!isAuthenticated) {
  favTriggers.forEach(btn => btn.addEventListener('click', openFavModal));
}
  if (isAuthenticated) {
  const recipeStars = document.querySelectorAll('.fav-star[data-name]');

  recipeStars.forEach(button => {
    button.addEventListener('click', async function (event) {
      event.preventDefault();
      event.stopPropagation();

      const recipe = {
        name: button.dataset.name,
        type: button.dataset.type,
        cuisine: button.dataset.cuisine,
        cost_range: button.dataset.costRange,
        ingredients: JSON.parse(button.dataset.ingredients),
        allergens: JSON.parse(button.dataset.allergens),
        steps: JSON.parse(button.dataset.steps)
      };

      try {
        const response = await fetch('/favorites/add', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(recipe)
        });

        const result = await response.json();

        if (result.status === 'saved' || result.status === 'duplicate') {
          button.classList.add('favorited');
          button.setAttribute('aria-label', 'Saved to favorites');
        }
      } catch (error) {
        console.error('Could not save favorite:', error);
      }
    });
  });
}

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

  const removeButtons = document.querySelectorAll(
  '.fav-star[data-favorite-id]'
);

removeButtons.forEach(button => {
  button.addEventListener('click', async function (event) {
    event.preventDefault();
    event.stopPropagation();

    const response = await fetch(
      `/favorites/${button.dataset.favoriteId}/remove`,
      { method: 'POST' }
    );

    const result = await response.json();

    if (result.status === 'removed') {
      button.closest('.meal-card').remove();
    }
  });
});

});