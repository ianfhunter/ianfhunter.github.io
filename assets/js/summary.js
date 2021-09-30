details = document.querySelectorAll("details");
details.forEach((targetDetail) => {
    targetDetail.addEventListener("click", () => {
        details.forEach((detail) => {
            if (detail !== targetDetail) {
                detail.removeAttribute("open");
            }
        });
    });
});


var admo_title = function (select_html) {
    let html_truc = document.querySelector(select_html).innerHTML
    console.log(html_truc)
    const p_title = /title:(.*)/gi
    const adm_title = html_truc.match(p_title)
    if (adm_title) {
        for (var j = 0; j < adm_title.length; j++) {
            html_truc = html_truc.replace(adm_title[j],
                "<span class='title-" + select_html.replace('.', '') + "'>" +
                adm_title[j].replace('title:', '') + "</span><br>")
        }
        return html_truc
    }
}

var admo_noblock = function (target) {
    var html = target.innerHTML;
    let select = '';
    let query = '';
    const adm = ['note', 'seealso', 'abstract', 'summary', 'tldr', 'info',
                 'todo', 'tip',
                 'hint', 'important', 'success', 'check', 'done', 'question',
                 'help', 'faq', 'warning',
                 'caution', 'attention', 'failure', 'fail', 'missing', 'danger',
                 'error', 'bug', 'example', 'exemple', "abstract",
                 'quote', 'cite'];
    const p_search = /<p>[?!]{3}ad-([A-Za-zÀ-ÖØ-öø-ÿ]+)/gi;
    const found_p = html.match(p_search);
    let select_html = ''
    if (found_p) {
        const p_len = found_p.length;
        for (var i = 0; i < p_len; i++) {
            select = found_p[i].replace("!!!ad-", '');
            select = select.replace("???ad-", '');
            select = select.replace('<p>', '')
            if (adm.includes(select)) {
                query = "<p class = 'admo-" + select + "'>"
                select_html = '.admo-' + select
            } else {
                query = "<p class='admo-note'>";
                select_html = '.admo-note'
            }
            const replaced = new RegExp(`<p>[!?]{3}ad-${select}`)
            const replaceit = html.match(replaced)
            for (var j = 0; j < replaceit.length; j++) {
                html = html.replace('<br>', '')
                html = html.replace(replaceit[j], query);
                html = html.replace('<br>', '')
                target.innerHTML = html;
                const truc = admo_title(select_html)
                console.log(truc)
                document.querySelector(select_html).innerHTML = truc

            }

        }
    }
}
admo_noblock(document.querySelector('.content'))
