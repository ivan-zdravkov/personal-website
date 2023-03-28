function loadWebsite() {
    let urlParams = new URLSearchParams(location.search);
    let project = urlParams.get('p');
    let leadership = urlParams.get('leadership');
    
    if (project) {
        project = project.replace('/', '');
    
        if (project)
            $(`a[href='#${project}']`).click();
    }

    if (leadership !== 'show') {
        $(`a[href='#leadership']`).show();
        $(`section[id='leadership']`).show();
        $(`a[href='#leadership']`).click();
    }
    else {
        $(`a[href='#leadership']`).hide();
        $(`section[id='leadership']`).hide();
    }
    
    clearUrl();
}

function clearUrl() {
    let clean_uri = location.protocol + "//" + location.host + location.pathname;

    window.history.replaceState({}, document.title, clean_uri);
}