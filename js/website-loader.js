function loadWebsite() {
    let urlParams = new URLSearchParams(location.search);
    let project = urlParams.get('project');

    if (project)
        $(`a[href='#${project}']`).click();

    clearUrl();
}

function clearUrl() {
    let clean_uri = location.protocol + "//" + location.host + location.pathname;

    window.history.replaceState({}, document.title, clean_uri);
}