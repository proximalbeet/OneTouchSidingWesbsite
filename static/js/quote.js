 document.getElementById('photo-input').addEventListener('change', function () {
      const names = Array.from(this.files).map(f => f.name).join(', ');
      document.getElementById('file-names').textContent = names || '';
    });

    async function submitQuote() {
      const btn = document.getElementById('submitBtn');
      const name = document.getElementById('name').value.trim();
      const email = document.getElementById('email').value.trim();
      const phone = document.getElementById('phone').value.trim();
      const location = document.getElementById('location').value.trim();
      const service = document.getElementById('service').value;
      const details = document.getElementById('details').value.trim();
      const photos = document.getElementById('photo-input').files;

      if (!name || !email || !phone || !location || !service) {
        showToast('Please fill in all required fields.', 'error');
        return;
      }

      btn.disabled = true;
      btn.textContent = 'Sending…';

      const formData = new FormData();
      formData.append('name', name);
      formData.append('email', email);
      formData.append('phone', phone);
      formData.append('location', location);
      formData.append('service_type', service);
      formData.append('details', details);
      for (const photo of photos) {
        formData.append('photos', photo);
      }

      try {
        const res = await fetch('/submit-quote', {
          method: 'POST',
          body: formData
        });
        const data = await res.json();

        if (data.success) {
          showToast("We'll be in touch soon!", 'success');
          document.getElementById('name').value = '';
          document.getElementById('email').value = '';
          document.getElementById('phone').value = '';
          document.getElementById('location').value = '';
          document.getElementById('service').selectedIndex = 0;
          document.getElementById('details').value = '';
          document.getElementById('photo-input').value = '';
          document.getElementById('file-names').textContent = '';
          btn.textContent = 'Quote Sent ✓';
          setTimeout(() => {
            btn.disabled = false;
            btn.textContent = 'Request Quote →';
          }, 3000);
        } else {
          showToast(data.message || 'Something went wrong.', 'error');
          btn.disabled = false;
          btn.textContent = 'Request Quote →';
        }
      } catch (err) {
        showToast('Network error. Please try again.', 'error');
        btn.disabled = false;
        btn.textContent = 'Request Quote →';
      }
    }

    function openModal() {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const location = document.getElementById('location').value.trim();
    const service = document.getElementById('service').value;

    if (!name || !email || !phone || !location || !service) {
      showToast('Please fill in all required fields.', 'error');
      return;
    }

      document.getElementById('modalSummary').innerHTML = `
        <div class="modal-summary-row"><span>Name</span><span>${name}</span></div>
        <div class="modal-summary-row"><span>Email</span><span>${email}</span></div>
        <div class="modal-summary-row"><span>Phone</span><span>${phone}</span></div>
        <div class="modal-summary-row"><span>Location</span><span>${location}</span></div>
        <div class="modal-summary-row"><span>Service</span><span>${service}</span></div>
      `;

      document.getElementById('modalOverlay').classList.add('active');
    }

    function closeModal() {
      document.getElementById('modalOverlay').classList.remove('active');
    }

    function showToast(msg, type) {
      const toast = document.getElementById('toast');
      toast.textContent = msg;
      toast.className = `toast ${type} show`;
      setTimeout(() => { toast.className = 'toast'; }, 4000);
    }