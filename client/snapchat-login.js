window.snapKitInit = function () {
    var loginButtonIconId = 'snapchat-login';
    // Mount Login Button
    snap.loginkit.mountButton(loginButtonIconId, {
        clientId: 'e4642342-b846-4564-8218-72a301acfe59',
        redirectURI: 'file:///home/ivan/Documents/HackCambridge/start.html',
        scopeList: [
            'user.display_name',
            'user.bitmoji.avatar',
        ],
        handleResponseCallback: function () {
            console.log("hello");
            clicked = true;
            document.getElementById("snapchat-login").style("display","hidden");
            snap.loginkit.fetchUserInfo()
                .then(
                    data => console.log('User info:', data));
        },
    });
};

// Load the SDK asynchronously
(function (d, s, id) {
    var js, sjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s);
    js.id = id;
    js.src = "https://sdk.snapkit.com/js/v1/login.js";
    sjs.parentNode.insertBefore(js, sjs);
}(document, 'script', 'loginkit-sdk'));