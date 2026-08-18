class LocationStatus extends HTMLElement {
  connectedCallback() {
    this.url = this.getAttribute('url');
    this.updateStatus();
  }

  async updateStatus() {
    const data = await this.fetchPage();
    if (!data || typeof data.is_open !== 'boolean') {
      this.textContent = this.dataset.unavailableLabel;
    } else if (data.is_open) {
      this.textContent = this.dataset.availableLabel;
    } else {
      this.textContent = this.dataset.closedLabel;
    }
  }

  fetchPage() {
    return fetch(this.url)
      .then((response) => response.json())
      .catch(() => null);
  }
}

window.customElements.define('location-status', LocationStatus);
