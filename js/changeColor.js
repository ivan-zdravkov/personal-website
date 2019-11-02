function changeCSS(cssFile) {
    var styles = document.getElementsByTagName("link");
    var style = null;

    for (st of styles) {
        if (st && st.href && st.href.includes("freelancer"))
            style = st;
    }

    if (style != null) {
        var newlink = document.createElement("link");
        var newHref = style.href.substring(0, style.href.lastIndexOf('/') + 1);

        newHref += cssFile;

        newlink.setAttribute("rel", "stylesheet");
        newlink.setAttribute("type", "text/css");
        newlink.setAttribute("href", newHref);

        document.getElementsByTagName("head").item(0).replaceChild(newlink, style);
    }
}