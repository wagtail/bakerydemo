class LocationStatus extends HTMLElement {
  connectedCallback() {
    this.url = this.getAttribute('url');
    this.updateStatus();
  }

  async updateStatus() {
    const data = await this.fetchPage();
    if (!data || typeof data.is_open !== 'boolean') {
      this.textContent =
        "Sorry, we couldn't retrieve the status of this location.";
    } else if (data.is_open) {
      this.textContent = 'This location is currently open.';
    } else {
      this.textContent = 'Sorry, this location is currently closed.';
    }
  }

  fetchPage() {
    return fetch(this.url)
      .then((response) => response.json())
      .catch(() => null);
  }
}

window.customElements.define('location-status', LocationStatus);
