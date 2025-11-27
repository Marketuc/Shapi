async function loadAuthHeader(path, title) {
    const container = document.querySelector('#auth-header-container');

    if (!container) return;

    // Fetch the header HTML
    const response = await fetch(path);
    const html = await response.text();

    container.innerHTML = html;

    const authTitle = document.querySelector('.auth-title');
    authTitle.textContent = title;
}