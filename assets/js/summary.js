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

var admo_noblock = function(target) {
    var html = target.innerHTML;
    let select = '';
    let query = '';
    const adm = ['note', 'seealso', 'abstract', 'summary', 'tldr', 'info',
        'todo', 'tip',
        'hint', 'important', 'success', 'check', 'done', 'question',
        'help', 'faq', 'warning',
        'caution', 'attention', 'failure', 'fail', 'missing', 'danger',
        'error', 'bug', 'example', 'exemple', "abstract",
        'quote', 'cite'
    ];
    const p_search = /<p>[?!]{3}ad-([A-Za-zÀ-ÖØ-öø-ÿ]+)/gi;
    const found_p = html.match(p_search);
    let select_html = ''
    if (found_p) {
        const p_len = found_p.length;
        for (var i = 0; i < p_len; i++) {
            select = found_p[i].replace("!!!ad-", '');
            select = select.replace("???ad-", '');
            select = select.replace('<p>', '')
            query = "<p class='admo-note'>";
            select_html = '.admo-note'
            const replaced = new RegExp(`<p>[!?]{3}ad-${select}`, 'gi')
            const replaceit = html.match(replaced)
            console.log(html)
            for (var j = 0; j < replaceit.length; j++) {
                html = html.replace(replaceit[j], query.replace('<br>', ''));
                console.log(html)
            }
        }
        target.innerHTML = html;

    }
}
admo_noblock(document.querySelector('.content'))