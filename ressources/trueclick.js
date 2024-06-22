const cssStyle = `
    :root {
        --trueclick-text-color: #181818;
        --trueclick-border-color: #ccc;
        --trueclick-bg-color: #f2f2f2;
        --trueclick-link-color: #888;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --trueclick-text-color: #f2f2f2;
            --trueclick-border-color: #2e2e2e;
            --trueclick-bg-color: #121212;
            --trueclick-box-shadow-color: #2e2e2e;
            --trueclick-link-color: #999;
        }
    }

    .trueclick-blur {
        filter: blur(5px);
    }

    .trueclick {
        font-family: Segoe UI, monospace;
        letter-spacing: -0.05em;
        font-size: 0.9rem;
        color: var(--trueclick-text-color);
        border: 1px solid var(--trueclick-border-color);
        border-radius: 8px;
        background-color: var(--trueclick-bg-color);
        width: 280px;
        padding: 10px;
    }

    .trueclick .error {
        display: none;
        color: red;
    }

    .trueclick-content {
        text-align: center;
        display: flex;
        box-sizing: border-box;
        align-items: center;
        justify-content: space-between;
    }
        
    .trueclick-content svg {
        display: none;
        flex: 0 0 20px;
        fill: var(--trueclick-text-color);
        animation: rotate 1s linear infinite;
    }

    .trueclick-content input[type="checkbox"] {
        width: 20px;
        height: 20px;
        flex: 0 0 20px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .trueclick-content p {
        flex: 1;
        margin-left: 5px;
        display: flex;
        justify-content: flex-start;
        align-items: center;
    }

    .trueclick-content .logo-container {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }

    .trueclick-content .logo-container span {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        height: 30px;
        margin-left: 10px;
        font-size: 20px;
    }

    .trueclick-content .logo-container p {
        font-size: 12px;
        letter-spacing: 0em;
        color: var(--trueclick-link-color);
        text-align: center;
        width: max-content;
        margin: 0;
    }

    .trueclick-content .logo-container a {
        margin-left: 2.5px;
        color: var(--trueclick-link-color);
        text-decoration: none;
    }

    .trueclick-content .logo-container a:hover {
        text-decoration: underline;
    }

    @keyframes rotate {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
`;

const html = `
    <span class="error"></span>
    <div class="trueclick-content">
        <svg width="24px" height="24px" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M512 1024c-69.1 0-136.2-13.5-199.3-40.2C251.7 958 197 921 150 874c-47-47-84-101.7-109.8-162.7C13.5 648.2 0 581.1 0 512c0-19.9 16.1-36 36-36s36 16.1 36 36c0 59.4 11.6 117 34.6 171.3 22.2 52.4 53.9 99.5 94.3 139.9 40.4 40.4 87.5 72.2 139.9 94.3C395 940.4 452.6 952 512 952c59.4 0 117-11.6 171.3-34.6 52.4-22.2 99.5-53.9 139.9-94.3 40.4-40.4 72.2-87.5 94.3-139.9C940.4 629 952 571.4 952 512c0-59.4-11.6-117-34.6-171.3a440.45 440.45 0 0 0-94.3-139.9 437.71 437.71 0 0 0-139.9-94.3C629 83.6 571.4 72 512 72c-19.9 0-36-16.1-36-36s16.1-36 36-36c69.1 0 136.2 13.5 199.3 40.2C772.3 66 827 103 874 150c47 47 83.9 101.8 109.7 162.7 26.7 63.1 40.2 130.2 40.2 199.3s-13.5 136.2-40.2 199.3C958 772.3 921 827 874 874c-47 47-101.8 83.9-162.7 109.7-63.1 26.8-130.2 40.3-199.3 40.3z"/>
        </svg>
        <input type="checkbox">
        <p>I am not a robot.</p>
        <div class="logo-container">
            <span>𝐓𝐫𝐮𝐞𝐂𝐥𝐢𝐜𝐤</span>
            <p>Source code on <a href="https://github.com/tn3w/TrueClick" target="_blank">GitHub</a></p>
        </div>
    </div>
`;

const captchaBoxCSS = `
    #ID-overlay {
        font-family: Segoe UI, Arial, sans-serif;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        background: rgba(0, 0, 0, 0.5);
        z-index: 9999;
        border-radius: 10px;
    }

    #ID-overlay .captcha-box  {
        padding: 10px;
        margin: 10px;
        max-width: 350px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        z-index: 10000;
        position: relative;
        text-align: center;
        color: var(--trueclick-text-color);
        border: 1px solid var(--trueclick-border-color);
        border-radius: 8px;
        background-color: var(--trueclick-bg-color);
    }

    #ID-overlay .captcha-box .square-image {
        width: 200px;
        height: 200px;
        display: block;
        margin: 0 auto;
        border-radius: 5px;
        box-shadow: 2px 2px 10px var(--trueclick-border-color);
    }

    #ID-overlay .captcha-box .error {
        display: none;
        font-size: 14px;
        color: #ff0000;
    }

    #ID-overlay .captcha-box .caption {
        font-size: 16px;
        margin: 0 auto;
        padding-top: 10px;
    }

    #ID-overlay .captcha-box .form-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    #ID-overlay .captcha-box .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-gap: 10px;
        padding: 10px;
    }

    #ID-overlay .captcha-box .grid-item {
        position: relative;
    }

    #ID-overlay .captcha-box .grid-item img {
        width: 100%;
        min-width: 75px;
        border-radius: 5px;
        box-shadow: 2px 2px 5px var(--border);
    }

    #ID-overlay .captcha-box .grid-item input[type="checkbox"] {
        position: absolute;
        transform: scale(1.5);
        margin: 5px;
        bottom: 8px;
        right: 5px;
    }

    #ID-overlay .captcha-box .submit-button {
        padding: 10px 20px;
        background-color: #0078FF;
        color: #f2f2f2;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        align-items: right;
    }

    #ID-overlay .captcha-box .submit-button:hover {
        background-color: #005ED3;
    }
`;

const captchaBoxHTML = `
    <div class="captcha-box">
        <img class="square-image" src="ORIGINAL_IMAGE">
        <p class="caption">CAPTION</p>
        <p class="error caption"></p>
        <div class="form-container">
            <div class="grid-container">
                GRIDS
            </div>
            <button class="submit-button">Submit</button>
        </div>
    </div>
`;

const captchaGridItemHTML = `
    <div class="grid-item">
        <img src="IMAGESRC">
        <input type="checkbox" name="IMAGEID" value="1">
    </div>
`;


function addStyles(css) {
    var styleElement = document.querySelector("head style") || document.createElement("style");
    
    if (styleElement.styleSheet) {
        styleElement.styleSheet.cssText += css;
    } else {
        styleElement.appendChild(document.createTextNode(css));
    }
    
    if (!styleElement.parentNode) {
        document.head.appendChild(styleElement);
    }

    return styleElement;
}

function removeStyles(css) {
    const styleSheets = document.querySelectorAll('style');

    styleSheets.forEach((styleElement) => {
        let cssText = '';
        if (styleElement.styleSheet) {
            cssText = styleElement.styleSheet.cssText;
        } else {
            cssText = styleElement.textContent;
        }

        if (cssText.includes(css)) {
            cssText = cssText.replace(css, '');
            if (styleElement.styleSheet) {
                styleElement.styleSheet.cssText = cssText;
            } else {
                styleElement.textContent = cssText;
            }

            if (cssText.trim() === '') {
                styleElement.remove();
            }
        }
    });
}

function showError(trueclick, error) {
    trueclick.getElementsByClassName('error')[0].innerHTML = error;
    trueclick.getElementsByClassName('error')[0].style.display = 'block';
}

function hideError(trueclick) {
    trueclick.getElementsByClassName('error')[0].style.display = 'none';
}

function showBoxError(box, error) {
    box.getElementsByClassName('error')[0].innerHTML = error;
    box.getElementsByClassName('error')[0].style.display = 'block';
}

function hideBoxError(box) {
    box.getElementsByClassName('error')[0].style.display = 'none';
}

window.onload = function() {
    const trueclickBoxes = document.getElementsByClassName('trueclick');

    if (trueclickBoxes.length > 0) {
        addStyles(cssStyle);
    }

    for (var i = 0; i < trueclickBoxes.length; i++) {
        let trueclick = trueclickBoxes[i];
        trueclick.innerHTML = html;

        let checkbox = trueclick.querySelector('input[type="checkbox"]');
        let svg = trueclick.querySelector('svg');

        function hideLoading() {
            checkbox.style.display = 'block';
            svg.style.display = 'none';
        }

        function showLoading() {
            checkbox.style.display = 'none';
            svg.style.display = 'block';
        }

        let isVerified = false;
        let newData = null;
        let newError = null;
        let canContinue = false;

        function displayCaptcha(data) {
            if (newData != null) {
                data = newData;
            }

            var challenge = data.challenge;
            var original_image = challenge.original;
            var images = challenge.images;
            var dataset = data.dataset;

            var randomID = 'i' + Math.random().toString(36).substring(2, 15);
            var styles = captchaBoxCSS.replaceAll('ID', randomID);
            addStyles(styles);

            let overlay = document.createElement('div')
            overlay.id = randomID + '-overlay';
            
            let captchaBox = captchaBoxHTML;
            captchaBox = captchaBox.replaceAll('ORIGINAL_IMAGE', original_image);

            let caption = dataset == 'ai-dogs' ? 'Choose the smiling dogs:' : 'Select all images that contain the same motif:';
            captchaBox = captchaBox.replaceAll('CAPTION', caption);

            let grids = '';
            for (var i = 0; i < images.length; i++) {
                let gridItem = captchaGridItemHTML;
                let image = images[i];
                gridItem = gridItem.replaceAll('IMAGESRC', image.src);
                gridItem = gridItem.replaceAll('IMAGEID', image.id);
                grids += gridItem;
            }
            captchaBox = captchaBox.replaceAll('GRIDS', grids);

            overlay.innerHTML = captchaBox;

            document.body.appendChild(overlay);

            if (!(newError == null)) {
                showBoxError(overlay, newError);
                newError = null;
            }

            Array.from(document.body.children).forEach(child => {
                if (child !== overlay) {
                    child.classList.add('trueclick-blur');
                    child.addEventListener('click', function() {
                        overlay.remove();
                        Array.from(document.body.children).forEach(c => c.classList.remove('trueclick-blur'));
                        removeStyles(styles);
                    });
                }
            });
    
            overlay.addEventListener('click', function(event) {
                if (event.target === overlay) {
                    overlay.remove();
                    Array.from(document.body.children).forEach(child => child.classList.remove('trueclick-blur'));
                    removeStyles(styles);
                }
            });

            document.addEventListener('keydown', function(event) {
                if (event.key === 'Escape') {
                    overlay.remove();
                    Array.from(document.body.children).forEach(child => child.classList.remove('trueclick-blur'));
                    removeStyles(styles);
                }
            });

            let button = overlay.querySelector('.submit-button');
            button.addEventListener('click', function() {
                showLoading();
                let selected = Array.from(overlay.querySelectorAll('input[type="checkbox"]:checked'));
                selected = selected.map((checkbox) => checkbox.name);

                if (selected.length == 0) {
                    showBoxError(overlay.getElementsByClassName('captcha-box')[0], 'You must select at least one image.');
                } else if (selected.length < 2) {
                    showBoxError(overlay.getElementsByClassName('captcha-box')[0], 'You have not selected all images.');
                } else if (selected.length > 4) {
                    showBoxError(overlay.getElementsByClassName('captcha-box')[0], 'You have selected too many images.');
                } else {
                    hideBoxError(overlay.getElementsByClassName('captcha-box')[0]);
                    overlay.remove();
                    Array.from(document.body.children).forEach(c => c.classList.remove('trueclick-blur'));
                    removeStyles(styles);

                    fetch('/verify_trueclick_challenge', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            'id': challenge.id,
                            'token': challenge.token,
                            'selected': selected.join('')
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'ok') {
                            isVerified = true;

                            let form = trueclick.closest('form') || document.forms[0];

                            let input = document.createElement('input');
                            input.type = 'hidden';
                            input.name = 'trueclick_response';
                            input.value = challenge.id + challenge.token;
                            form.appendChild(input);

                        } else if (data.status === 'error') {
                            newData = data;
                            newError = 'That was not the correct answer.';
                        }

                        canContinue = true;
                        hideLoading();
                    });
                }
            });
        }

        checkbox.addEventListener('change', function() {
            if (this.checked) {
                showLoading();
                fetch('/create_trueclick_challenge', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(async data => {
                    if (data.status === 'ok') {
                        hideLoading();

                        while (!isVerified) {
                            displayCaptcha(data);

                            while (!canContinue) {
                                await new Promise(r => setTimeout(r, 100));
                            }
                            canContinue = false;
                        }
                        this.checked = true;
                        this.disabled = true;
                        return;
                    } else if (data.status === 'error') {
                        showError(trueclick, data.error);
                    }
                    hideLoading();
                });
                this.checked = false;
            } else {
                hideLoading();
            }
        });
    }
}