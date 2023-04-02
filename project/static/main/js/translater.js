async function myTranslate(text, elementId) {
    let headers = {
        'X-Requested-Whit': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    }

    const csrf = document.querySelector("input[name=csrfmiddlewaretoken]").value;
    headers['X-CSRFToken'] = csrf

    let response = await fetch('../my-translate/', {
        method: 'post',
        headers: headers,
        body: JSON.stringify(text),
    })

    let translateText = await response.json()
    let translateTextBlock = document.createElement("div");
    translateTextBlock.className = 'translate-text-block';
    translateTextBlock.innerHTML = "<br><span>" + "Translate:<br><br>" + await translateText['text'] + "</span>";

    openModal = document.getElementById("open-modal-" + elementId);
    openModal.appendChild(translateTextBlock);
    document.getElementById("button-translator").remove();
}
