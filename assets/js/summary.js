details = document.querySelectorAll("details.second");
details.forEach((targetDetail) => {
    targetDetail.addEventListener("click", () => {
        details.forEach((detail) => {
            if (detail !== targetDetail && targetDetail.className == "second") {
                detail.removeAttribute("open");
            }
        });
    });
});

detailsF = document.querySelectorAll("details.first");
detailsF.forEach((targetDetailF) => {
    targetDetailF.addEventListener("click", () => {
        detailsF.forEach((detailF) => {
            if (detailF !== targetDetailF && targetDetailF.className == "first") {
                detailF.removeAttribute("open");
            }
        });
    });
});

var admo_noblock = function(target) {
    var html = target.innerHTML;
    let select = '';
    let query = '';
    const p_search = /<p>[?!]{3}ad-([A-Za-zÀ-ÖØ-öø-ÿ]+)/gi;
    const found_p = html.match(p_search);
    let select_html = '';
    if (found_p) {
        const p_len = found_p.length;
        for (var i = 0; i < p_len; i++) {
            select = found_p[i].replace("!!!ad-", '');
            select = select.replace("???ad-", '');
            select = select.replace('<p>', '')
            console.log(select);
            query = "<p class='admo-note'>";
            select_html = '.admo-note'
            const replaced = /<p>[?!]{3}ad-([A-Za-zÀ-ÖØ-öø-ÿ]+)/gi
            const replaceit = html.match(/<p>[?!]{3}ad-([A-Za-zÀ-ÖØ-öø-ÿ]+)/gi)
            if (replaceit) {
                 for (var j = 0; j < replaceit.length; j++) {
                    html = html.replace(replaceit[j], query.replace('<br>', ''));
                 }
            }

        }
        target.innerHTML = html;

    }
}
admo_noblock(document.querySelector('.content'))